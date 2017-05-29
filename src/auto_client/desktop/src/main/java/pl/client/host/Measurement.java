package pl.client.host;

import java.net.DatagramPacket;

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
    public void setId(String host_name) {
        this.host_name = host_name;
    }

    public Long getMeasurementId() { return this.measurement_id;}
    public void setMeasurementId(Long measurement_id ) { this.measurement_id = measurement_id; }

    public Double getValue() { return this.value;}
    public void setValue(Double value ) { this.value = value; }

    public String getDate() { return this.date;}
    public void setDate(String date) { this.date = date; }

}
