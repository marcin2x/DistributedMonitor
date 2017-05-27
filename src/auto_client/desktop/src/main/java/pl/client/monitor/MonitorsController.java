package pl.client.monitor;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.fxml.FXML;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.cell.PropertyValueFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.StringHttpMessageConverter;
import org.springframework.http.converter.json.MappingJacksonHttpMessageConverter;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;
import pl.client.login.JwtString;
import pl.client.util.Utils;

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

    private JwtString jwtString;

    public void initialize() {
        monitorId.setCellValueFactory(new PropertyValueFactory<>("id"));
        userId.setCellValueFactory(new PropertyValueFactory<>("user_id"));
        monitorName.setCellValueFactory(new PropertyValueFactory<>("name"));
        monitorAddress.setCellValueFactory(new PropertyValueFactory<>("address"));
        monitorPort.setCellValueFactory(new PropertyValueFactory<>("port"));
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
        MultiValueMap<String, String> params = new LinkedMultiValueMap<String, String>();
        params.add("Authorization", jwtString.getJwt());
        try {
            ResponseEntity<Monitors> responseEntity = rt.getForEntity(uri, Monitors.class, params);
            Monitors monitors = responseEntity.getBody();
            monitorData.addAll(monitors);
        } catch (RestClientException e) {
            e.printStackTrace();
            Monitor monitor = new Monitor();
            monitor.setId(1L);
            monitor.setUser_id(2L);
            monitor.setAddress("Stub Address");
            monitor.setName("Stub Name");
            monitor.setPort("Stub Port");
            monitorData.add(monitor);
        }
        reloadData();
    }

    private void reloadData() {
        monitors.setItems(monitorData);
    }
}
