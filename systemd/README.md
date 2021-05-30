# systemd service

you can use the `dsmr-exporter.service` file as a starting point.

change the `ExecStart=/usr/local/bin/dsmr_exporter.py` line to the path where you cloned dsmr-exporter.

Don't forget to add the correct command line options.

Example:

    ExecStart=/home/username/bin/dsmr_exporter/dsmr_exporter.py --serial /dev/ttyUSB0 --elastic-host 192.168.0.103  