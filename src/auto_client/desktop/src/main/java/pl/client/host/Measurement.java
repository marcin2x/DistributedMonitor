package pl.client.host;

import org.codehaus.jackson.annotate.JsonProperty;

/**
 * Created by djana on 2017-05-29.
 */

public class Measurement {
    private String host_name;
    private Long measurement_id;
    private Double value;
    private String date;


    public String getHostName() {
        return this.host_name;
    }

    @JsonProperty(value = "host_name")
    public void setHostName(String host_name) {
        this.host_name = host_name;
    }

    public Long getMeasurementId() { return this.measurement_id;}

    @JsonProperty(value = "measurement_id")
    public void setMeasurementId(Long measurement_id ) { this.measurement_id = measurement_id; }

    public Double getValue() { return this.value;}
    public void setValue(Double value ) { this.value = value; }

    public String getDate() { return this.date;}
    public void setDate(String date) { this.date = date; }

}
