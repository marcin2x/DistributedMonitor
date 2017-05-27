package pl.client.login;

import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.PasswordField;
import javafx.scene.control.TextField;
import javafx.stage.Stage;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.StringHttpMessageConverter;
import org.springframework.http.converter.json.MappingJacksonHttpMessageConverter;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;
import pl.client.monitor.MonitorsController;
import pl.client.util.Utils;

import java.io.IOException;


public class LoginController {

    @FXML
    private Button loginButton;
    @FXML
    private PasswordField password;
    @FXML
    private TextField login;

    private Stage stage;

    @FXML
    private void login() {
        RestTemplate rt = new RestTemplate();
        rt.getMessageConverters().add(new MappingJacksonHttpMessageConverter());
        rt.getMessageConverters().add(new StringHttpMessageConverter());
        String uri = new Utils().getAuthAddress() + "login";
        User user = new User();
        user.setLogin(login.getText());
        user.setPassword(password.getText());
        try {
            ResponseEntity<JwtString> responseEntity = rt.postForEntity(uri, user, JwtString.class);
            JwtString body = responseEntity.getBody();
            FXMLLoader fxmlLoader = new FXMLLoader(getClass().getResource("../monitor/monitors.fxml"));
            Parent root = fxmlLoader.load();
            MonitorsController controller = fxmlLoader.getController();
            controller.loadMonitors(body);
            stage.setScene(new Scene(root));
        } catch (RestClientException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void setStage(Stage stage) {
        this.stage = stage;
    }
}
