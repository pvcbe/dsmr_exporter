# dsmr exporter

dsmr exporter is a daemon that reads smart meter P1 data (dsmr) and converts it to an elastic search document.

dsmr_exporter can read data from:
- multiple serial ports
- multiple esp8266's

This software needs hardware to work. To find out more about the supported hardware, check out [`docs/hardware.md`](docs/hardware.md).


# Installation

## From source

    sudo pip3 install pyserial
    sudo pip3 install elasticsearch
    git clone https://github.com/pvcbe/dsmr_exporter.git
    
## pip

TODO

     
# Using

This example reads data from the *ttyUSB0* serial port and exports the data to host *192.168.0.103*

     ./dsmr_exporter.py --serial /dev/ttyUSB0 --elastic-host 192.168.0.103

- Attention: Your user needs read access to the serial device


      export P1_SERIAL=/dev/ttyUSB0
      export P1_HOST=10.0.0.16:5678,172.16.0.2:8898
      export ELASTIC_HOST=192.168.0.103:1234
      ./dsmr_exporter.py

    
This example uses environment variables to read its config:
- serial input on `/dev/ttyUSB0`
- TCP host `10.0.0.16` on port `5678` and TCP host `172.16.0.2` on port `8898`
- elastic search host on IP `192.168.0.103` and port `1234`

## Options

option                     |environment variable| default |
---------------------------|--------------------|----------
`--p1-serial`              | `P1_SERIAL`        | -
`--p1-host`                | `P1_HOST`          | -
`--elastic-host`           | `ELASTIC_HOST`     | localhost:9200
`--elastic-index`          | `ELASTIC_INDEX`    | dsmr-%Y.%m


# Example dashboard

![grafana dashboard](docs/dashboards/grafana_dashboard.png)

There is an example dashboard for **elasticserach** and one for **grafana**.  They are located under [`docs/dashboards`](docs/dashboards).
The grafana source name is **elasticsearch-dsmr**. Don't forget to create a datasource with that name (or change the dashboard).


# Elasticsearch

It is wise to create a rollup job or delete old dsmr indexes. Or to buy more storage as time passes :)


# Reference

[dsmr standard document](https://www.netbeheernederland.nl/_upload/Files/Slimme_meter_15_a727fce1f1.pdf)


