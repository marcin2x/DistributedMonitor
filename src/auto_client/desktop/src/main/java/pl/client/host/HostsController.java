package pl.client.host;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.ComboBox;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.stage.Stage;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.StringHttpMessageConverter;
import org.springframework.http.converter.json.MappingJacksonHttpMessageConverter;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;
import pl.client.login.JwtString;
import pl.client.monitor.MonitorsController;
import pl.client.util.Utils;

import java.io.IOException;
import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/**
 * Created by djana on 2017-05-29.
 */
public class HostsController {

    @FXML
    public ComboBox<Long> intervalComboBox;
    ObservableList<Measurement> cpuData = FXCollections.observableArrayList();
    @FXML
    public TableColumn<Measurement, Double> cpuValue;
    @FXML
    public TableView<Measurement> cpuMeasurements;
    ObservableList<Long> options = FXCollections.observableArrayList(15L, 30L, 45L, 60L);
    ObservableList<Measurement> ramData = FXCollections.observableArrayList();
    @FXML
    public TableColumn<Measurement, Double> ramValue;
    @FXML
    public TableView<Measurement> ramMeasurements;

    @FXML
    private Button backButton;

    private Timer timer;

    @FXML
    public void onBack(ActionEvent ae) {
        backToMonitors();
    }

    private Stage stage;
    private JwtString jwtString;
    private String monitorAddress;
    private String monitorPort;

    public void initialize() {
        cpuValue.setCellValueFactory(new PropertyValueFactory<Measurement, Double>("value"));
        ramValue.setCellValueFactory(new PropertyValueFactory<Measurement, Double>("value"));
        intervalComboBox.setItems(options);
        timer = new Timer();

        intervalComboBox.valueProperty().addListener((observable, oldValue, newValue) -> {
            timer.cancel();
            timer = new Timer();
            timer.schedule(new java.util.TimerTask() {
                               @Override
                               public void run() {
                                   reload();
                               }
                           },
                    5000,
                    newValue * 1000);
        });
        intervalComboBox.setValue(15L);
    }

    public void loadHosts(JwtString jwtString, String monitorAddress, String monitorPort) {
        this.jwtString = jwtString;
        this.monitorAddress = monitorAddress;
        this.monitorPort = monitorPort;
        reload();
    }

    private void reload() {
        cpuData.clear();
        ramData.clear();
        RestTemplate rt = new RestTemplate();
        rt.getMessageConverters().add(new MappingJacksonHttpMessageConverter());
        rt.getMessageConverters().add(new StringHttpMessageConverter());

        HttpHeaders headers = new HttpHeaders();
        headers.set("Authorization", jwtString.getJwt());
        HttpEntity entity = new HttpEntity(headers);
        Utils utils = new Utils();

        try {
            ResponseEntity<Hosts> hostsResponseEntity = rt.exchange(utils.getHostsAddress(monitorAddress, monitorPort), HttpMethod.GET, entity, Hosts.class);
            Hosts hosts = hostsResponseEntity.getBody();

            ResponseEntity<Measurements> measurementsResponseEntity = rt.exchange(utils.getMesurementsValues(monitorAddress, monitorPort), HttpMethod.GET, entity, Measurements.class);
            Measurements measurements = measurementsResponseEntity.getBody();

            List<Measurement> lastHostValues = measurements
                    .stream()
                    .collect(Collectors.groupingBy(e -> e.getHostName()))
                    .entrySet()
                    .stream()
                    .flatMap(e -> Stream.of(e.getValue().get(0)))
                    .collect(Collectors.toList());

            List<HostMeasurement> hostMeasurements = hosts
                    .stream()
                    .flatMap(e -> e.getMeasurements().stream())
                    .collect(Collectors.toList());

            Map<String, List<Measurement>> metricMeasurements = lastHostValues
                    .stream()
                    .collect(Collectors.groupingBy(e ->
                            hostMeasurements
                                    .stream()
                                    .filter(x -> x.getId() == e.getMeasurementId())
                                    .findFirst()
                                    .get()
                                    .getDescription()));

            cpuData.addAll(metricMeasurements.getOrDefault("CPU", Collections.emptyList()));
            ramData.addAll(metricMeasurements.getOrDefault("RAM", Collections.emptyList()));
        } catch (RestClientException e) {
            e.printStackTrace();
        }
        reloadData();
    }

    private void reloadData() {
        cpuMeasurements.setItems(cpuData);
        ramMeasurements.setItems(ramData);
    }

    private void backToMonitors() {
        try {
            FXMLLoader fxmlLoader = new FXMLLoader(getClass().getResource("../monitor/monitors.fxml"));
            Parent root = fxmlLoader.load();
            MonitorsController controller = fxmlLoader.getController();
            controller.loadMonitors(jwtString);
            controller.setStage(stage);
            stage.setScene(new Scene(root));
        } catch (IOException e) {
            e.printStackTrace();
        }

    }

    public void setStage(Stage stage) {
        this.stage = stage;
    }
}
