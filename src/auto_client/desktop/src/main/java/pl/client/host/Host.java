package pl.client.host;

import org.codehaus.jackson.annotate.JsonIgnoreProperties;

import java.util.ArrayList;

/**
 * Created by djana on 2017-05-29.
 */
@JsonIgnoreProperties(ignoreUnknown = true)
public class Host {
    private Long id;
    private String name;
    private ArrayList<HostMeasurement> measurements;

    public Long getId() {
        return id;
    }
    public void setId(Long id) {
        this.id = id;
    }

    public String getName() {
        return this.name;
    }
    public void setName(String name) {
        this.name = name;
    }

    public ArrayList<HostMeasurement> getMeasurements() {
        return measurements;
    }
    public void setMeasurements(ArrayList<HostMeasurement> measurements) {
        this.measurements = measurements;
    }

}
