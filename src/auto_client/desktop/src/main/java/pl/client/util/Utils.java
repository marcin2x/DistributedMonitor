package pl.client.util;

import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

/**
 * Created by Trillon on 2017-05-27.
 */
public class Utils {

    public String getAuthAddress() {
        Properties prop = new Properties();
        InputStream stream = getClass().getResourceAsStream("../config.properties");
        try {
            prop.load(stream);
        } catch (IOException e) {
            return null;
        }
        return prop.getProperty("auth.address");
    }
}
