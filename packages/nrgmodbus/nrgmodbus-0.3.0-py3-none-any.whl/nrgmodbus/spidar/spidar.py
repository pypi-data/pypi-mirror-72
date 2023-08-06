#!/bin/usr/python
try:
    from nrgmodbus import logger
except ImportError:
    pass
from .registers import spidar_registers


class spidar_v1(object):
    """
    class for handling modbus connections to Spidar V1 systems

    parameters
    ----------
        ip : string
            ip address or domain name of spidar
        port : int
            port for modbus access (default 502)
        unit : int
            slave number on bus (default 1)
    """
    def __init__(self, ip='', port=502, unit=1, connect=False):
        self.ip = ip
        self.port = port
        self.unit = unit
        self.init_registers()
        self.e = ''

        if connect is True:
            self.connect()

    def init_registers(self):
        self.hr = spidar_registers()

    def connect(self):
        """
        initialize self.ip, self.port, self.unit
        """
        from pymodbus.client.sync import ModbusTcpClient as ModbusClient

        self.client = ModbusClient(host=self.ip, port=self.port, unit=self.unit)
        logger.info("Connecting to {0}".format(self.ip))
        try:
            self.client.connect()
            if self.client.is_socket_open() is True:
                logger.info("Connected to Spidar OK")
            else:
                self.client.connect()
                if self.client.is_socket_open is not True:
                    logger.error('Could Not Connect to {0}'.format(self.ip))
                    raise ValueError('Could Not Connect to {0}'.format(self.ip))
        except Exception as e:
            self.e = e
            logger.error("Connection failed")
            logger.debug(self.e)

    def disconnect(self):
        logger.info("Disconnecting from {0}".format(self.ip))
        try:
            self.client.close()
            logger.info("Closed connection")
        except Exception as e:
            logger.error("Error closing connection")
            logger.debug(e)

    def return_rt_data_readings(self):
        """ refresh all registers """
        start_reg = 0
        length = 105

        self.read_result = self.read_single_register([start_reg, length], singles=True)

        self.hr.met_data['pressure']['value'] = self.read_result[1] * self.hr.met_data['pressure']['scaling']

        self.hr.met_data['temperature']['value'] = self.read_result[2] * self.hr.met_data['temperature']['scaling']
        if self.hr.met_data['temperature']['scaling'] > 100:
            self.hr.met_data['temperature']['value'] -= 656

        self.hr.met_data['humidity']['value'] = self.read_result[3] * self.hr.met_data['humidity']['scaling']
        self.hr.met_data['precipitation']['value'] = self.read_result[4] * self.hr.met_data['precipitation']['scaling']

        n = 5

        for gate in range(1, 10 + 1):
            self.hr.wind_data_gate[gate]['height']['value'] = self.read_result[n]
            self.hr.wind_data_gate[gate]['speed']['min']['value'] = self.read_result[n+1] * self.hr.wind_data_gate[gate]['speed']['min']['scaling']
            self.hr.wind_data_gate[gate]['speed']['max']['value'] = self.read_result[n+2] * self.hr.wind_data_gate[gate]['speed']['max']['scaling']
            self.hr.wind_data_gate[gate]['speed']['avg']['value'] = self.read_result[n+3] * self.hr.wind_data_gate[gate]['speed']['avg']['scaling']
            self.hr.wind_data_gate[gate]['speed']['sd']['value'] = self.read_result[n+4] * self.hr.wind_data_gate[gate]['speed']['sd']['scaling']
            self.hr.wind_data_gate[gate]['dir']['min']['value'] = self.read_result[n+5] * self.hr.wind_data_gate[gate]['dir']['min']['scaling']
            self.hr.wind_data_gate[gate]['dir']['max']['value'] = self.read_result[n+6] * self.hr.wind_data_gate[gate]['dir']['max']['scaling']
            self.hr.wind_data_gate[gate]['dir']['avg']['value'] = self.read_result[n+7] * self.hr.wind_data_gate[gate]['dir']['avg']['scaling']
            self.hr.wind_data_gate[gate]['dir']['sd']['value'] = self.read_result[n+8] * self.hr.wind_data_gate[gate]['dir']['sd']['scaling']
            self.hr.wind_data_gate[gate]['quality']['value'] = self.read_result[n+9]

            n += 10


    def read_single_register(self, register, singles=False):
        """
        wrapper for pymodbus, returns single value
        """

        try:
            rr = self.client.read_holding_registers(register[0], register[1], unit=1)
            self.rr = rr

            if register[1] > 2 and singles is True:
                flo = rr.registers

            else:
                flo = rr.registers[0]

            return flo

        except Exception as e:
            self.e = e
            self.rr = rr
            return 9999
