

- pip3
- setup.py
- licentie
- config file
- systemd service
- elastic template
- grafana dashboard
- dashboards kibana
- screenshots
- deb
- docker
- windows package



todo:

option                      |    var                | -
---------------------------|--------------------|----------
`--elastic-user`           | `ELASTIC_USER`     | <not impemented>
`--elastic-password`       | `ELASTIC_PASSWORD` | <not impemented>
`--elastic-interval`, `-i` | `ELASTIC_INTERVAL` | <not impemented>
`--elastic-create-dashboards` |                 | <not impemented>


# error

    WARNING| host <socket.socket fd=9, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('192.168.82.1', 57552), raddr=('192.168.82.58', 8089)> timeout, reconnecting
    Traceback (most recent call last):
      File "./dsmr_exporter.py", line 445, in <module>
        main()
      File "./dsmr_exporter.py", line 435, in main
        de.run()
      File "./dsmr_exporter.py", line 224, in run
        self.check_p1host_timeout()
      File "./dsmr_exporter.py", line 234, in check_p1host_timeout
        self.connect_tcp_input(s.getpeername()[0], s.getpeername()[1])
      File "./dsmr_exporter.py", line 129, in connect_tcp_input
        s.connect((host, port))
    OSError: [Errno 113] No route to host
