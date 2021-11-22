#!/usr/bin/env python3
#
#  export smartmeter (dsmr) data to elasticsearch
#
# Copyright (C) 2021 Philip Vanmontfort
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import sys
import os
import argparse
import logging
import socket
import re
import time
import datetime
import select

try:
    import elasticsearch
except ModuleNotFoundError:
    print("ERROR: elasticsearch library not found, please install by typing 'pip3 install elasticsearch'")
    sys.exit(1)

try:
    import serial
except ModuleNotFoundError:
    print("ERROR: pyserial library not found, please install by typing 'pip3 install pyserial'")
    sys.exit(1)

__version__ = '0.0.1'

"""
#TODO: conversion names
convert_map = {
    "0-0:96.1.1.255": "electricity.identifier",
    "1-0:1.8.(\d+).255": "electricity.meter_reading.to_client.tarrif.{}",
    "1-0:2.8.(\d+).255": "electricity.meter_reading.by_client.tarrif.{}",
}

# text, keyword, boolean, long, double, histogram, ip, date,
elastic_template = {
    "index_patterns": ["test-*"],
    "settings": {},
    "mappings": {
        "dsmr": {
            "timestamp": {"type": "date"},
            "electricity.identifier": {"type": "keyword"},  # 0-0:96.1.1.255
            "electricity.meter_reading.to_client.tarrif.1": {"type": "float"},  # 1-0:1.8.1.255
            "electricity.meter_reading.to_client.tarrif.2": {"type": "float"},  # 1-0:1.8.2.255
            "electricity.meter_reading.to_client.tarrif.3": {"type": "float"},  # 1-0:1.8.3.255
            "electricity.meter_reading.to_client.tarrif.4": {"type": "float"},  # 1-0:1.8.4.255
            "electricity.meter_reading.to_client.tarrif.5": {"type": "float"},  # 1-0:1.8.5.255
            "electricity.meter_reading.to_client.tarrif.6": {"type": "float"},  # 1-0:1.8.6.255
            "electricity.meter_reading.to_client.tarrif.7": {"type": "float"},  # 1-0:1.8.7.255
            "electricity.meter_reading.to_client.tarrif.8": {"type": "float"},  # 1-0:1.8.8.255
            "electricity.meter_reading.to_client.tarrif.9": {"type": "float"},  # 1-0:1.8.9.255
            "electricity.meter_reading.to_client.tarrif.10": {"type": "float"},  # 1-0:1.8.10.255
            "electricity.meter_reading.to_client.tarrif.11": {"type": "float"},  # 1-0:1.8.11.255
            "electricity.meter_reading.to_client.tarrif.12": {"type": "float"},  # 1-0:1.8.12.255
            "electricity.meter_reading.to_client.tarrif.13": {"type": "float"},  # 1-0:1.8.13.255
            "electricity.meter_reading.to_client.tarrif.14": {"type": "float"},  # 1-0:1.8.14.255
            "electricity.meter_reading.to_client.tarrif.15": {"type": "float"},  # 1-0:1.8.15.255
            "electricity.meter_reading.to_client.tarrif.16": {"type": "float"},  # 1-0:1.8.16.255
            "electricity.meter_reading.by_client.tarrif.1": {"type": "float"},  # 1-0:2.8.1.255
            "electricity.meter_reading.by_client.tarrif.2": {"type": "float"},  # 1-0:2.8.2.255
            "electricity.meter_reading.by_client.tarrif.3": {"type": "float"},  # 1-0:2.8.3.255
            "electricity.meter_reading.by_client.tarrif.4": {"type": "float"},  # 1-0:2.8.4.255
            "electricity.meter_reading.by_client.tarrif.5": {"type": "float"},  # 1-0:2.8.5.255
            "electricity.meter_reading.by_client.tarrif.6": {"type": "float"},  # 1-0:2.8.6.255
            "electricity.meter_reading.by_client.tarrif.7": {"type": "float"},  # 1-0:2.8.7.255
            "electricity.meter_reading.by_client.tarrif.8": {"type": "float"},  # 1-0:2.8.8.255
            "electricity.meter_reading.by_client.tarrif.9": {"type": "float"},  # 1-0:2.8.9.255
            "electricity.meter_reading.by_client.tarrif.10": {"type": "float"},  # 1-0:2.8.10.255
            "electricity.meter_reading.by_client.tarrif.11": {"type": "float"},  # 1-0:2.8.11.255
            "electricity.meter_reading.by_client.tarrif.12": {"type": "float"},  # 1-0:2.8.12.255
            "electricity.meter_reading.by_client.tarrif.13": {"type": "float"},  # 1-0:2.8.13.255
            "electricity.meter_reading.by_client.tarrif.14": {"type": "float"},  # 1-0:2.8.14.255
            "electricity.meter_reading.by_client.tarrif.15": {"type": "float"},  # 1-0:2.8.15.255
            "electricity.meter_reading.by_client.tarrif.16": {"type": "float"},  # 1-0:2.8.16.255
            "electricity.tarrif.indicator": {"type": "text"},  # 0-0:96.14.0.255
            "electricity.voltage.sags.l1": {"type": "long"},  # 1-0:32.32.0.255
            "electricity.voltage.sags.l2": {"type": "long"},  # 1-0:52.32.0.255
            "electricity.voltage.sags.l3": {"type": "long"},  # 1-0:72.32.0.255
            "electricity.voltage.swells.l1": {"type": "long"},  # 1-0:32.36.0.255
            "electricity.voltage.swells.l2": {"type": "long"},  # 1-0:52.36.0.255
            "electricity.voltage.swells.l3": {"type": "long"},  # 1-0:72.36.0.255
            "electricity.voltage.l1": {"type": "float"},  # 1-0:32.7.0.255
            "electricity.voltage.l2": {"type": "float"},  # 1-0:52.7.0.255
            "electricity.voltage.l3   ": {"type": "float"},  # 1-0:72.7.0.255
            "electricity.current.l1   ": {"type": "float"},  # 1-0:31.7.0.255
            "electricity.current.l2   ": {"type": "float"},  # 1-0:51.7.0.255
            "electricity.current.l3   ": {"type": "float"},  # 1-0:71.7.0.255
            "electricity.power.to_client.l1   ": {"type": "float"},  # 1-0:21.7.0.255
            "electricity.power.to_client.l2   ": {"type": "float"},  # 1-0:41.7.0.255
            "electricity.power.to_client.l3   ": {"type": "float"},  # 1-0:61.7.0.255
            "electricity.power.by_client.l1   ": {"type": "float"},  # 1-0:22.7.0.255
            "electricity.power.by_client.l2   ": {"type": "float"},  # 1-0:42.7.0.255
            "electricity.power.by_client.l3   ": {"type": "float"},  # 1-0:62.7.0.255
            "electricity.power.failures.any_fase": {"type": "long"},  # 0-0:96.7.21.255
            "electricity.power.failures.long.any_fase": {"type": "long"},  # 0-0:96.7. 9.255
            "electricity.power.failures.log": {"type": "text"},  # 1-0:99:97.0.255
            "electricity.power.to_client.total": {"type": "long"},  # 1-0:1.7.0.255
            "electricity.power.by_client.total": {"type": "long"},  # 1-0:2.7.0.255
            "electricity.breaker.state": {"type": "keyword"},  # 0-0:96.3.10.255
        }
    }
}
"""


class DsmrExporter:
    def __init__(self):
        self.socket_stall_detect_timeout = 10
        self.logger = None
        self.p1serial_ports = []
        self.p1hosts = []
        self.p1host_last_data_time = {}
        self.tcp_buffer_size = 8000
        self.re_validate_telegram_line = re.compile("^(\d-\d:\d+?\.\d+?\.\d+?)\((.*)\)")
        self.elastic_host = None
        self.elastic_index = ''
        self.elastic_backlog = []

    def set_logger(self, logger):
        self.logger = logger

    def connect_serial_input(self, serial_port_input):
        serial_port = serial.Serial(serial_port_input, 115200, timeout=1)
        self.p1serial_ports.append(serial_port)

    def connect_tcp_input(self, host, port):
        port = int(port)
        if port < 1 or port > 65535:
            raise ValueError("not a valid port: {}".format(port))
        s = socket.socket()
        s.settimeout(self.socket_stall_detect_timeout)
        s.connect((host, port))
        self.p1hosts.append(s)
        self.p1host_last_data_time[(s.getpeername()[0], s.getpeername()[1])] = datetime.datetime.now()

    def reconnect_tcp_input(self, existing_socket):
        (existing_host, existing_port) = existing_socket.getpeername()
        s = socket.socket()
        s.settimeout(self.socket_stall_detect_timeout)
        try:
            s.connect((existing_host, existing_port))
        except socket.timeout:
            del s
            return
        except OSError:
            del s
            return

        for sock in self.p1hosts:
            if sock.getpeername()[0] == existing_host and sock.getpeername()[1] == existing_port:
                self.logger.debug("Socket already exists, deleting before reconnecting")
                self.p1hosts.remove(sock)
        self.p1hosts.append(s)
        self.p1host_last_data_time[(s.getpeername()[0], s.getpeername()[1])] = datetime.datetime.now()

    def connect_elastic_output(self, host, port):
        port = int(port)
        if port < 1 or port > 65535:
            raise ValueError("elastic host port {} is not a valid port ".format(port))
        try:
            socket.gethostbyname(host)
            # TODO: sniffing doesn't work on servers with multiple ip's
            # self.elastic_host = elasticsearch.Elasticsearch([host + ':' + str(port)], sniff_on_start=True)
            self.elastic_host = elasticsearch.Elasticsearch([host + ':' + str(port)])
        except elasticsearch.exceptions.TransportError:
            self.logger.info("warning: elasticsearch not sniffable, continuing without sniffing")
            self.elastic_host = elasticsearch.Elasticsearch([host + ':' + str(port)])
        # todo: index template upload

    def telegram_to_json(self, telegram):
        # todo: detect if input is ok
        doc = {'@timestamp': datetime.datetime.now(datetime.timezone.utc)}
        self.logger.debug("DEBUG| telegram {}".format(telegram))
        for item in telegram:
            validated_data = self.re_validate_telegram_line.search(item)
            if validated_data:
                key, value = validated_data.groups()
                value = value.split('*')[0]
                try:
                    value = float(value)
                except ValueError:
                    pass
                doc[key] = value
        self.logger.debug("DEBUG| doc={}".format(doc))
        self.logger.debug("DEBUG| telegram_to_json --------------------------------------------")
        return doc

    def doc_put(self, doc):
        index_and_date = datetime.datetime.now(datetime.timezone.utc).strftime(self.elastic_index)
        self.logger.debug("DEBUG| index_and_date: {}".format(index_and_date))
        try:
            res = self.elastic_host.index(index=str(index_and_date), body=doc)
        except elasticsearch.exceptions.ConnectionError as e:
            self.logger.error("elastic connection error: {}".format(e))
            res = None
            # todo: with backlog buffer
        if res:
            result = res.get("result")
            if result != "created":
                print(result)
        else:
            print('!', end='')

    def run(self):
        while 1:
            read_sockets = select.select(self.p1hosts + self.p1serial_ports, [], [], self.socket_stall_detect_timeout)[
                0]
            self.logger.debug("DEBUG| read_sockets: {}".format(read_sockets))
            if read_sockets:
                for s in read_sockets:
                    try:
                        if type(s).__name__ == "Serial":
                            input_buffer = s.read(self.tcp_buffer_size).decode()
                            self.logger.debug("DEBUG| serial data for port {}\n{}".format(s.port, input_buffer))
                        else:
                            input_buffer = s.recv(self.tcp_buffer_size).decode()
                            # todo: rate limit wrong data?
                            self.logger.debug("DEBUG| read_sockets: {}".format(read_sockets))
                            self.reset_p1host_timeout(s)
                    except TimeoutError:
                        if type(s).__name__ == "Serial":
                            self.logger.debug("DEBUG| serial timeout for port {}".format(s.port))
                        else:
                            self.reconnect_tcp_input(s)
                        continue
                    except UnicodeDecodeError:
                        if type(s).__name__ == "Serial":
                            self.logger.debug("DEBUG| decode error for serial port {}".format(s.port))
                        else:
                            self.logger.debug("DEBUG| decode error for host {}:{}".format(s.getpeername()[0], s.getpeername()[1]))
                        continue
                    telegram = []
                    for line in input_buffer.split():
                        if line.startswith('/'):
                            telegram = []
                        elif line.startswith('!'):
                            doc = self.telegram_to_json(telegram)
                            if doc is not None:
                                if type(s).__name__ == "Serial":
                                    doc["serial.port"] = s.port
                                else:
                                    doc["host.name"] = s.getpeername()[0]
                                    doc["host.port"] = s.getpeername()[1]
                                try:
                                    self.doc_put(doc)
                                except elasticsearch.exceptions.TransportError:
                                    self.logger.error("elastic backpressure 429 NOT_IMPLEMENTED")
                                    # TransportError(429
                            telegram = []
                        elif "(" in line and ")" in line:
                            telegram.append(line)

            else:
                self.logger.warning("WARNING| run didn't receive data in a timely fassion")
            self.check_p1host_timeout()
            time.sleep(1)

    def check_p1host_timeout(self):
        socket_stall_detect_timeout = datetime.timedelta(seconds=self.socket_stall_detect_timeout)
        for s in self.p1hosts:
            self.logger.debug(
                "DEBUG| check_p1host_timeout[{}:{}]: delta {}".format(s.getpeername()[0], s.getpeername()[1],
                                                                      self.p1host_last_data_time[
                                                                          (s.getpeername()[0],s.getpeername()[1])]
                                                                      + socket_stall_detect_timeout)
            )
            if (self.p1host_last_data_time[(s.getpeername()[0],s.getpeername()[1])] + socket_stall_detect_timeout) < datetime.datetime.now():
                self.logger.warning("WARNING| host {} timeout, reconnecting".format(s))
                self.reconnect_tcp_input(s)

    def reset_p1host_timeout(self, peer_socket):
        (host, port) = peer_socket.getpeername()
        self.p1host_last_data_time[(host, port)] = datetime.datetime.now()
        self.logger.debug("DEBUG| reset_p1host_timeout reset for {}".format((host, port)))

    def stop(self):
        for s in self.p1hosts:
            try:
                s.close()
            except:
                pass
        for sp in self.p1serial_ports:
            try:
                sp.close()
            except:
                pass
        try:
            self.elastic_host.close()
        except:
            pass


def die(text=""):
    sys.stderr.write("ERROR| {}\nexiting.".format(text))
    sys.exit(1)


def main():
    appname = os.path.splitext(os.path.basename(__file__))[0]
    logger = logging.getLogger(appname)
    logger.setLevel(logging.INFO)
    # formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s %(message)s', datefmt='%Y-%m-%d_%H:%M:%S')
    console = logging.StreamHandler()
    # console.setFormatter(formatter)
    logger.addHandler(console)
    # log.addHandler(logging.handlers.RotatingFileHandler('/var/log/{}.log'.format(progname), maxBytes=100000))

    ap = argparse.ArgumentParser(description='dsmr p1 data exporter to elasticsearch')
    ap.add_argument('--p1-host',
                    action='append',
                    default=[os.getenv('P1_HOST')],
                    help="p1 source hosts in a host<:port> (multiple times possible, comma separated)\n Environment "
                         "var: P1_HOST"
                    )
    ap.add_argument('--p1-serial',
                    action='append',
                    default=[os.getenv('P1_SERIAL')],
                    help="serial ports used as p1 data source (multiple times possible)\nEnvironment var: P1_SERIAL"
                    )
    ap.add_argument('--elastic-host',
                    default=[os.getenv('ELASTIC_HOST', 'localhost:9200')],
                    help="elasticsearch_host<:port>\nEnvironment var: ELASTIC_HOST"
                    )
    ap.add_argument('--elastic-user',
                    default=os.getenv('ELASTIC_USER'),
                    help="elasticsearch host default auth username\nEnvironment var: ELASTIC_USER NOT_IMPLEMENTED",
                    )
    ap.add_argument('--elastic-password',
                    default=os.getenv('ELASTIC_PASSWORD'),
                    help="elasticsearch host auth password\nEnvironment var: ELASTIC_PASSWORD NOT_IMPLEMENTED",
                    )
    ap.add_argument('--elastic-interval', '-i',
                    type=int,
                    default=os.getenv('ELASTIC_INTERVAL'),
                    help="elasticsearch publish interval, minimal is 1\nEnvironment var: ELASTIC_INTERVAL "
                         "NOT_IMPLEMENTED"
                    )
    ap.add_argument('--elastic-index', '--index',
                    default=os.getenv('ELASTIC_INDEX', 'dsmr-%Y.%m'),
                    help="elasticsearch index name.  Default is 'dsmr-%%Y.%%m', will be parsed with python strftime("
                         "'%%Y.%%m') Environment var: ELASTIC_INDEX"
                    )
    ap.add_argument('--elastic-create-dashboards', '-c',
                    action='store_true',
                    help="uploads the default dashboards into elasticsearch TODO"
                    )
    ap_logging_group = ap.add_mutually_exclusive_group()
    ap_logging_group.add_argument(
        '--quiet', '-q',
        action="store_true",
        default=os.getenv('DSMR_QUIET'),
        help="silence output"
    )
    ap_logging_group.add_argument(
        '--debug',
        action="store_true",
        default=os.getenv('DSMR_DEBUG'),
        help="debug output"
    )
    options = ap.parse_args()

    if options.debug and options.quiet:
        die('FATAL| log option --debug and --quiet can not be used together')
    if options.quiet:
        logger.setLevel(logging.ERROR)
    elif options.debug:
        logger.setLevel(logging.DEBUG)

    de = DsmrExporter()
    de.set_logger(logger)
    logger.info("starting {} {}".format(appname, __version__))

    # SERIAL INPUT
    import serial.tools.list_ports
    detected_ports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
    available_serial = {}

    # filter port path
    for detected_port in detected_ports:
        available_serial[detected_port[0]] = detected_port[1:]

    p1_serial = {}
    for ports in options.p1_serial:
        if ports is not None:
            for port in ports.split(','):
                if port not in available_serial:
                    ap.print_usage()
                    valid_serial = ""
                    for detected_port in detected_ports:
                        valid_serial += "    {}{}{}\n".format(detected_port[0].ljust(20), detected_port[1].ljust(20),
                                                              detected_port[2])
                    die("FATAL| port {} is not a valid com port\nvalid ports are:\n{}".format(port, valid_serial))
                else:
                    p1_serial[port] = available_serial[port]

    # TCP INPUT
    # TODO ipv6 ip's
    # TODO https://docs.python.org/3.6/library/selectors.html#module-selectors
    p1_hosts = {}
    for hosts in options.p1_host:
        if hosts is not None:
            for host in hosts.split(','):
                # logger.debug("host={}".format(host))
                if host == '':
                    continue
                try:
                    # TODO: regex instead split, create more robust input checking
                    host, port = host.split(':')
                    p1_hosts[(host, port)] = None
                except ValueError:
                    die("FATAL| host not parsable {}".format(host))
            break

    if p1_hosts == {} and p1_serial == {}:
        ap.print_usage()
        die("FATAL| no valid p1-host or serial inputs defined")

    # connect serial input
    for serial_port in p1_serial.keys():
        try:
            de.connect_serial_input(serial_port)
        except serial.serialutil.SerialException as e:
            logger.error("ERROR| when opening serial input")
            die("FATAL | {}".format(e))
        except PermissionError as e:
            logger.error("ERROR| serial premission denied for port {}".format(serial_port))
            die("FATAL | {}".format(e))

    # connect input tcp host
    for host, port in p1_hosts.keys():
        try:
            de.connect_tcp_input(host, port)
        except socket.gaierror:
            die("FATAL| dsmr host not resolvable: {}:{}".format(host, port))
        except TimeoutError:
            die("FATAL| timeout for input host {}:{}".format(host, port))
        except Exception as e:
            die("FATAL| error while connecting input host {}:{}.\nERROR| {}".format(host, port, e))

    # elastic output
    # todo regex parse hostname with capture group to make it more robust
    # todo: elastic connect faster detect faults
    if type(options.elastic_host) is type([]):
        options.elastic_host = options.elastic_host[0]
    if ':' in options.elastic_host:
        elastic_host, elastic_port = options.elastic_host.split(':')
    else:
        elastic_host = options.elastic_host
        elastic_port = 9200

    try:
        de.connect_elastic_output(elastic_host, elastic_port)
        logger.debug("DEBUG| elastic output ready")
    except ValueError:
        die("FATAL| elastic port '{}' is not a valid port".format(elastic_port))
    except socket.gaierror:
        die("FATAL| elasticsearch hostname '{}' not resolvable".format(elastic_host))
    except elasticsearch.exceptions.ConnectionError:
        die("FATAL| elasticsearch not reachable")

    de.elastic_index = options.elastic_index

    serial_ports_string = ", ".join(map(str, p1_serial.keys()))
    hosts = ", ".join(["{}:{}".format(host, port) for host, port in p1_hosts.keys()])

    logger.info("- serial inputs are: '{}'".format(serial_ports_string))
    logger.info("- tcp inputs are:    '{}'".format(hosts))
    logger.info("- output host:       '{}' on port:{}, with user:'{}' and index pattern:'{}'".format(elastic_host,
                                                                                                     elastic_port,
                                                                                                     options.elastic_user,
                                                                                                     options.elastic_index))
    # main loop
    try:
        de.run()
    except elasticsearch.exceptions.RequestError as e:
        # RequestError(400, 'mapper_parsing_exception', 'Could not dynamically add mapping for field [host.name]. Existing mapping for [host] must be of type object but found [text].')
        die("FATAL ERROR| {}".format(e))
    except KeyboardInterrupt:
        de.stop()
        logger.info("stopping {} by user request".format(appname))


if __name__ == "__main__":
    main()
