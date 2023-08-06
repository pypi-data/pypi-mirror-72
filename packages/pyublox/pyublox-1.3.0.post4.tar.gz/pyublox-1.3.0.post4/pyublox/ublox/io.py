import collections
import os.path
import struct
import serial
import time
import threading
import tempfile
import shutil
import queue

from roktools import logger

from . import core
from . import constants
from . import helpers
from . import SERIAL_PORT_STR

CONFIG_GROUPS_DEFAULT = [constants.CONSTELLATIONS_STR, constants.SIGNALS_STR, 
                            constants.RATES_STR, constants.MEAS_PROP_STR]

# ------------------------------------------------------------------------------

class UbloxRecorder(threading.Thread):

    def __init__(self, serial_port=None, slice_period=helpers.SlicePeriodicity.DAILY,
                 output_dir=".", receiver_name="UBLX"):
        threading.Thread.__init__(self)

        self.slice = slice_period

        self.output_dir = os.path.abspath(output_dir)
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        self.serial_port = serial_port
        if not self.serial_port:
            logger.info('Serial port not defined, autodetecting')
            connection_config = detect_connection()
            self.serial_port = connection_config.pop(SERIAL_PORT_STR)

        self.serial_stream = serial.Serial(self.serial_port)

        if not self.serial_stream.is_open:
            logger.critical(f'Could not open serial stream [ {self.serial_port} ]')

        self.receiver_name = receiver_name

        self.tempdir = tempfile.mkdtemp(prefix="pyublox_")

        self.current_epoch_suffix = None

        self.fout = None

        logger.info("Writing ubx data from _serial_stream [ {} ] for receiver [ {} ] to files "
                    "in folder [ {} ], with [ {} ] periodicity".format(
                           self.serial_port, self.receiver_name, self.output_dir, self.slice.name))

        logger.debug('Partial files will be written in this temporary folder [ {} ]'.format(self.tempdir))

    # ---

    def run(self):

        incoming_epoch_suffix = None
        for packet in core.ublox_packets(self.serial_stream):

            try:
                packet_type, parsed_packet = core.parse(packet)
            except KeyError:
                packet_type = None
            
            if packet_type == core.PacketType.RXM_RAWX:
                tow = getattr(parsed_packet, 'rcvTow')
                week = getattr(parsed_packet, 'week')
                epoch = helpers.weektow_to_datetime(tow, week)

                incoming_epoch_suffix = self.slice.build_rinex3_epoch(epoch)

            if not incoming_epoch_suffix:
                continue

            if not self.current_epoch_suffix or self.current_epoch_suffix != incoming_epoch_suffix:

                self.__close_and_save_partial_file__()

                self.current_epoch_suffix = incoming_epoch_suffix

                filename = os.path.join(self.tempdir,'{}_{}.ubx'.format(self.receiver_name, self.current_epoch_suffix))
                self.fout = open(filename, 'wb')
                logger.info("Created new data file [ {} ]".format(os.path.basename(filename)))

            self.fout.write(core.PREAMBLE)
            self.fout.write(packet)

    # ---

    def stop(self):

        if self.serial_stream:
            self.serial_stream.close()
            logger.info('Closed serial stream from [ {} ]'.format(self.serial_port))

        self.__close_and_save_partial_file__()

        if self.tempdir:
            shutil.rmtree(self.tempdir)

    # ---

    def __close_and_save_partial_file__(self):

        if self.fout:
            filename = self.fout.name

            self.fout.close()

            src = filename
            dst = os.path.join(self.output_dir, os.path.basename(filename))

            logger.debug('Moving [ {} ] -> [ {} ]'.format(src, dst))

            shutil.move(src, dst)

def detect():

    try:
        config = detect_connection()
    except Exception as e:
        logger.critical('Could not detect connection: {}'.format(str(e)))
        return None

    serial_port = config.pop(SERIAL_PORT_STR)

    serial_stream = serial.Serial(serial_port, **config)

    try:
        config = get_config(serial_stream)
        config[SERIAL_PORT_STR] = serial_port
    except:
        logger.critical('Unable to get receiver parameters. Re-launch the command')
        config = None

    serial_stream.close()

    return config


def detect_connection(serial_port=None):

    if not serial_port:
        logger.debug('No serial port specified, attempting to find one')

        for port in serial.tools.list_ports.comports():
            if 'u-blox GNSS receiver' in port:
                serial_port = port.device
    
    logger.debug(f'Attempting to open [ {serial_port} ]')
    stream = serial.Serial(serial_port)

    config = {SERIAL_PORT_STR: serial_port}

    KEY_IDS = [core.KeyId.CFG_UART1_BAUDRATE, core.KeyId.CFG_UART1_STOPBITS, 
                core.KeyId.CFG_UART1_PARITY, core.KeyId.CFG_UART1_DATABITS]

    key_values = core.get_config(KEY_IDS, stream)

    key_id = core.KeyId.CFG_UART1_BAUDRATE
    if key_id in key_values:
        value = key_values[key_id]
        config['baudrate'] = core.parse_key_id_value(key_id, value)

    key_id = core.KeyId.CFG_UART1_STOPBITS
    if key_id in key_values:
        value = key_values[key_id]
        stopbits = core.parse_key_id_value(key_id, value)
        if stopbits == 1:
            config['stopbits'] = serial.STOPBITS_ONE
        elif stopbits == 2:
            config['stopbits'] = serial.STOPBITS_ONE_POINT_FIVE
        elif stopbits == 3:
            config['stopbits'] = serial.STOPBITS_TWO
        else:
            raise ValueError('Half bit not supported by pyserial')

    key_id = core.KeyId.CFG_UART1_PARITY
    if key_id in key_values:
        value = key_values[key_id]
        parity = core.parse_key_id_value(key_id, value)
        if parity == 0:
            config['parity'] = serial.PARITY_NONE
        elif parity == 1:
            config['parity'] = serial.PARITY_ODD
        elif parity == 2:
            config['parity'] = serial.PARITY_EVEN

    key_id = core.KeyId.CFG_UART1_DATABITS
    if key_id in key_values:
        value = key_values[key_id]
        bytesize = core.parse_key_id_value(key_id, value)
        if bytesize == 0:
            config['bytesize'] = serial.EIGHTBITS
        elif bytesize == 1:
            config['bytesize'] = serial.SEVENBITS
        
    stream.close()

    return config


def set_baudrate(baudrate, serial_stream):

    kwargs = {
        core.KeyId.CFG_UART1_BAUDRATE: baudrate,
        core.KeyId.CFG_UART2_BAUDRATE: baudrate
    }

    core.set_config(kwargs, serial_stream)



def get_config(serial_stream, config_groups=CONFIG_GROUPS_DEFAULT):

    key_ids = []

    for config_group in config_groups:
        key_ids += getattr(CONFIG_OPTIONS[config_group], 'key_ids')

    config = {}

    try:
        key_values = core.get_config(key_ids, serial_stream)

        for config_group in config_groups:
            config_builder = getattr(CONFIG_OPTIONS[config_group], 'config_builder')
            config[config_group] = config_builder(key_values)
    except:
        pass

    return config

def set_config(serial_stream, config_dict=None, ucenter_config_filename=None):

    res = False

    if ucenter_config_filename:
        res = set_config_from_ucenter_file(serial_stream, ucenter_config_filename)

    if config_dict:
        res = set_config_from_dict(serial_stream, config_dict)

    return res

def set_config_from_ucenter_file(serial_stream, fh):

    res = False

    if fh.readable():
        for line in fh:
            submit_res = core.submit_valset_from_valget_line(line, serial_stream)
            if submit_res:
                logger.info('Applied config line [ {} ]'.format(line))
            else:
                logger.warning('Could not apply config line [ {} ]'.format(line))

            res = res or submit_res
            time.sleep(0.2)

    return res

def set_config_from_dict(serial_stream, config_dict):

    logger.debug(f'Incoming configuration parameters {config_dict}')
    config = {}

    for config_group, config_values in config_dict.items():

        if config_group == constants.CONSTELLATIONS_STR:
            for key_id, constellation in KEY_ID_TO_CONSTELLATION.items():
                if constellation in config_values:
                    config[key_id] = constants.BYTE_TRUE
                else:
                    config[key_id] = constants.BYTE_FALSE

        elif config_group == constants.SIGNALS_STR:
            for key_id, signal_props in SIGNAL_PROPERTIES.items():
                constellation = getattr(signal_props, 'constellation')
                channel = getattr(signal_props, 'channel')
                if constellation in config_values and channel in config_values[constellation]:
                    enable = constants.BYTE_TRUE
                else:
                    enable = constants.BYTE_FALSE

                config[key_id] = enable

        elif config_group == constants.RATES_STR:

            min_meas_rate_s = None

            if constants.SOLUTION_STR in config_values:
                key_id = core.KeyId.CFG_RATE_NAV
                solution_rate_s = config_values[constants.SOLUTION_STR]
                min_meas_rate_s = solution_rate_s / 5 # as per Section 7.8.16 of ICD
                config[key_id] = int(solution_rate_s)

            if constants.MEASUREMENTS_STR in config_values:
                key_id = core.KeyId.CFG_RATE_MEAS
                value = config_values[constants.MEASUREMENTS_STR]
                value = max(value, min_meas_rate_s) if min_meas_rate_s else value
                config[key_id] = int(value * 1000) # s -> ms

        elif config_group == constants.MEAS_PROP_STR:
            if 'smoothing' in config_group:
                config[core.KeyId.CFG_NAVSPG_USE_PPP] = constants.BYTE_TRUE
                
        else:
            logger.warning('Unrecognized configuration group [ {} ]. Skipping'.format(config_group))

    if config:
        core.set_config(config, serial_stream)
        return True
    
    else:
        logger.warning('No configuration has been applied')
        return False


def __build_constellation__(key_values):

    constellations = []

    keys = key_values.keys()
    config_key_ids = getattr(CONFIG_OPTIONS[constants.CONSTELLATIONS_STR], 'key_ids')
    for key_id in list(set(keys) & set(config_key_ids)):
        value = key_values[key_id]
        constellation_enabled = core.parse_key_id_value(key_id, value)

        if constellation_enabled:
            constellations.append(KEY_ID_TO_CONSTELLATION[key_id])

    return constellations


def __build_signals__(key_values):

    signals = {}

    keys = key_values.keys()
    config_key_ids = getattr(CONFIG_OPTIONS[constants.SIGNALS_STR], 'key_ids')
    for key_id in list(set(keys) & set(config_key_ids)):

        active = core.parse_key_id_value(key_id, key_values[key_id])
        if active:
            signal_properties = SIGNAL_PROPERTIES[key_id]
            constellation = getattr(signal_properties, 'constellation')
            channel = getattr(signal_properties, 'channel')

            if constellation not in signals:
                signals[constellation] = []

            signals[constellation].append(channel)
            
    return signals


def __build_rates__(key_values):

    meas_rate = None

    rates = {}

    for key_id in [core.KeyId.CFG_RATE_MEAS, core.KeyId.CFG_RATE_NAV]:

        value = core.parse_key_id_value(key_id, key_values[key_id])

        if key_id == core.KeyId.CFG_RATE_MEAS:
            meas_rate = value / 1.0e3 # ms to seconds
            rates[constants.MEASUREMENTS_STR] = meas_rate 
 
        elif key_id == core.KeyId.CFG_RATE_NAV:
            rates[constants.SOLUTION_STR] = meas_rate / value 

    return rates


def __build_meas_prop__(key_values):

    props = {}

    keys = key_values.keys()
    config_key_ids = getattr(CONFIG_OPTIONS[constants.MEAS_PROP_STR], 'key_ids')
    for key_id in list(set(keys) & set(config_key_ids)):
        if key_id == core.KeyId.CFG_NAVSPG_USE_PPP:
            props['smoothing'] = core.parse_key_id_value(key_id, key_values[key_id]) 

    return props

#def get_constellations(serial_stream):
#
#    key_ids = CONSTELLATION_KEY_IDS
#
#    config_constellations = core.get_config(key_ids, serial_stream)
#
#    config_signals = get_signals(serial_stream)
#
#    return __
#
#
#    for key_id in key_ids:
#        value = config_constellations[key_id]
#        constellation_enabled = core.parse_key_id_value(key_id, value)
#
#        constellation = KEY_ID_TO_CONSTELLATION[key_id]
#
#        if constellation_enabled and constellation in config_signals:
#            constellations.append(constellation)
#
#    return constellations


ConfigOptions = collections.namedtuple('ConfigOptions', ['key_ids', 'config_builder'])
CONFIG_OPTIONS = {
    constants.CONSTELLATIONS_STR : ConfigOptions([
        core.KeyId.CFG_SIGNAL_GPS_ENA,
        core.KeyId.CFG_SIGNAL_GAL_ENA,
        core.KeyId.CFG_SIGNAL_BDS_ENA,
        core.KeyId.CFG_SIGNAL_QZSS_ENA,
        core.KeyId.CFG_SIGNAL_GLO_ENA
    ], __build_constellation__),

    constants.SIGNALS_STR : ConfigOptions([
        core.KeyId.CFG_SIGNAL_GPS_L1CA_ENA,  core.KeyId.CFG_SIGNAL_GPS_L2C_ENA,   
        core.KeyId.CFG_SIGNAL_GAL_E1_ENA,    core.KeyId.CFG_SIGNAL_GAL_E5B_ENA,   
        core.KeyId.CFG_SIGNAL_BDS_B1_ENA,    core.KeyId.CFG_SIGNAL_BDS_B2_ENA,    
        core.KeyId.CFG_SIGNAL_QZSS_L1CA_ENA, core.KeyId.CFG_SIGNAL_QZSS_L2C_ENA,  
        core.KeyId.CFG_SIGNAL_GLO_L1_ENA,    core.KeyId.CFG_SIGNAL_GLO_L2_ENA,    
    ], __build_signals__),

    constants.RATES_STR : ConfigOptions([
        core.KeyId.CFG_RATE_MEAS, 
        core.KeyId.CFG_RATE_NAV 
    ], __build_rates__),

    constants.MEAS_PROP_STR : ConfigOptions([
        core.KeyId.CFG_NAVSPG_USE_PPP
    ], __build_meas_prop__)

}


SignalProperties = collections.namedtuple('SignalProperties', ['constellation', 'channel'])
SIGNAL_PROPERTIES = {
    core.KeyId.CFG_SIGNAL_GPS_L1CA_ENA: SignalProperties(constants.GPS_STR, '1C'),
    core.KeyId.CFG_SIGNAL_GPS_L2C_ENA: SignalProperties(constants.GPS_STR,'2C'),
    core.KeyId.CFG_SIGNAL_GAL_E1_ENA: SignalProperties(constants.GAL_STR,'1C'),
    core.KeyId.CFG_SIGNAL_GAL_E5B_ENA: SignalProperties(constants.GAL_STR,'7B'),   
    core.KeyId.CFG_SIGNAL_BDS_B1_ENA: SignalProperties(constants.BDS_STR,'2I'),
    core.KeyId.CFG_SIGNAL_BDS_B2_ENA: SignalProperties(constants.BDS_STR,'7I'),    
    core.KeyId.CFG_SIGNAL_QZSS_L1CA_ENA: SignalProperties(constants.QZSS_STR,'1C'),
    core.KeyId.CFG_SIGNAL_QZSS_L2C_ENA: SignalProperties(constants.QZSS_STR,'2L'),  
    core.KeyId.CFG_SIGNAL_GLO_L1_ENA: SignalProperties(constants.GLO_STR,'1C'),
    core.KeyId.CFG_SIGNAL_GLO_L2_ENA: SignalProperties(constants.GLO_STR,'2C'),
}

KEY_ID_TO_CONSTELLATION = {
    core.KeyId.CFG_SIGNAL_GPS_ENA:  constants.GPS_STR,
    core.KeyId.CFG_SIGNAL_GAL_ENA:  constants.GAL_STR,
    core.KeyId.CFG_SIGNAL_BDS_ENA:  constants.BDS_STR,
    core.KeyId.CFG_SIGNAL_QZSS_ENA: constants.QZSS_STR,
    core.KeyId.CFG_SIGNAL_GLO_ENA:  constants.GLO_STR 
}
