package pl.client.monitor;

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

    public void loadMonitors(JwtString jwtString) {
        RestTemplate rt = new RestTemplate();
        rt.getMessageConverters().add(new MappingJacksonHttpMessageConverter());
        rt.getMessageConverters().add(new StringHttpMessageConverter());
        String uri = new Utils().getAuthAddress() + "monitors";
        MultiValueMap<String, String> params = new LinkedMultiValueMap<String, String>();
        params.add("Authorization", jwtString.getJwt());
        try {
            ResponseEntity<Monitors> monitors = rt.getForEntity(uri, Monitors.class, params);
            Monitors body = monitors.getBody();
            body.size();
        } catch (RestClientException e) {
            e.printStackTrace();
        }
    }
}
