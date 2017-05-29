package pl.client.monitor;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableRow;
import javafx.scene.control.TableView;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.scene.input.MouseButton;
import javafx.stage.Stage;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.StringHttpMessageConverter;
import org.springframework.http.converter.json.MappingJacksonHttpMessageConverter;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;
import pl.client.login.JwtString;
import pl.client.util.Utils;
import pl.client.host.HostsController;

import java.io.IOException;

/**
 * Created by Trillon on 2017-05-27.
 */
public class MonitorsController {

    ObservableList<Monitor> monitorData = FXCollections.observableArrayList();
    @FXML
    public TableColumn<Monitor, Long> monitorId;
    @FXML
    public TableColumn<Monitor, Long> userId;
    @FXML
    public TableColumn<Monitor, String> monitorName;
    @FXML
    public TableColumn<Monitor, String> monitorAddress;
    @FXML
    public TableColumn<Monitor, String> monitorPort;
    @FXML
    public TableView<Monitor> monitors;

    private Stage stage;
    private JwtString jwtString;

    public void initialize() {
        monitorId.setCellValueFactory(new PropertyValueFactory<Monitor, Long>("id"));
        userId.setCellValueFactory(new PropertyValueFactory<Monitor, Long>("user_id"));
        monitorName.setCellValueFactory(new PropertyValueFactory<Monitor, String>("name"));
        monitorAddress.setCellValueFactory(new PropertyValueFactory<Monitor, String>("address"));
        monitorPort.setCellValueFactory(new PropertyValueFactory<Monitor, String>("port"));

        monitors.setRowFactory(tv -> {
            TableRow<Monitor> row = new TableRow<>();
            row.setOnMouseClicked(event -> {
                if (! row.isEmpty() && event.getButton()== MouseButton.PRIMARY) {

                    Monitor clickedRow = row.getItem();
                    goToHosts(clickedRow);
                }
            });
            return row ;
        });

        new java.util.Timer().schedule(
                new java.util.TimerTask() {
                    @Override
                    public void run() {
                        reload();
                    }
                },
                5000,
                60000
        );
    }

    public void loadMonitors(JwtString jwtString) {
        this.jwtString = jwtString;
        reload();
    }

    private void reload() {
        monitorData.clear();
        RestTemplate rt = new RestTemplate();
        rt.getMessageConverters().add(new MappingJacksonHttpMessageConverter());
        rt.getMessageConverters().add(new StringHttpMessageConverter());
        String uri = new Utils().getAuthAddress() + "monitors";
        HttpHeaders headers = new HttpHeaders();
        headers.set("Authorization", jwtString.getJwt());
        HttpEntity entity = new HttpEntity(headers);

        try {
            ResponseEntity<Monitors> responseEntity = rt.exchange(uri, HttpMethod.GET, entity, Monitors.class);
            Monitors monitors = responseEntity.getBody();
            monitorData.addAll(monitors);
        } catch (RestClientException e) {
            e.printStackTrace();
        }
        reloadData();
    }

    private void reloadData() {
        monitors.setItems(monitorData);
    }

    private void goToHosts(Monitor monitor){

        try {
            FXMLLoader fxmlLoader = new FXMLLoader(getClass().getResource("../host/hosts.fxml"));
            Parent root = fxmlLoader.load();
            HostsController controller = fxmlLoader.getController();
            controller.loadHosts(jwtString, monitor.getAddress(), monitor.getPort());
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
