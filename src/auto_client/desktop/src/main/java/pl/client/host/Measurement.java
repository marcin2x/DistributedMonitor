package pl.client.host;

import org.codehaus.jackson.annotate.JsonProperty;

/**
 * Created by djana on 2017-05-29.
 */

public class Measurement {
    private String hostName;
    private Long measurement_id;
    private Double value;
    private String date;


    public String getHostName() {
        return this.hostName;
    }

    @JsonProperty(value = "host_name")
    public void setHostName(String hostName) {
        this.hostName = hostName;
    }

    public Long getMeasurementId() { return this.measurement_id;}

    @JsonProperty(value = "measurement_id")
    public void setMeasurementId(Long measurement_id ) { this.measurement_id = measurement_id; }

    public Double getValue() { return this.value;}
    public void setValue(Double value ) { this.value = value; }

    public String getDate() { return this.date;}
    public void setDate(String date) { this.date = date; }

}
