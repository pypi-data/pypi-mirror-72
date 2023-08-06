import datetime
import enum


_GPS_TIME_START = datetime.datetime(1980, 1, 6, 0, 0, 0)

class SlicePeriodicity(enum.Enum):
    
    DAILY = 86400
    HOURLY = 3600
    QUARTERLY = 900
    UNDEFINED = 0

    @staticmethod
    def from_string(string):
        """
        Get the SlicePeriodicity from a string

        >>> SlicePeriodicity.from_string('daily')
        SlicePeriodicity.DAILY

        >>> SlicePeriodicity.from_string('DAILY')
        SlicePeriodicity.DAILY
        """

        if (string.lower() == 'daily'): return SlicePeriodicity.DAILY
        elif (string.lower() == 'quarterly'): return SlicePeriodicity.QUARTERLY
        elif (string.lower() == 'hourly'): return SlicePeriodicity.HOURLY
        else: return SlicePeriodicity.UNDEFINED

    @staticmethod
    def list():
        """ Return a list of the available valid periodicities """
        return list([v.name for v in SlicePeriodicity if v.value > 0])

    def build_rinex3_epoch(self, epoch):
        """
        Construct a Rinex-3-like epoch string

        >>> epoch = datetime.datetime(2020, 5, 8, 9, 29, 20)
        >>> SlicePeriodicity.QUARTERLY.build_rinex3_epoch_stream(epoch)
        '20201290915_15M'

        >>> SlicePeriodicity.HOURLY.build_rinex3_epoch_stream(epoch)
        '20201290900_01H'

        >>> SlicePeriodicity.DAILY.build_rinex3_epoch_stream(epoch)
        '20201290000_01D'
        """

        hour = epoch.hour if self != SlicePeriodicity.DAILY else 0

        day_seconds = (epoch - epoch.combine(epoch, datetime.time())).total_seconds()

        minute = get_quarter_str(day_seconds) if self == SlicePeriodicity.QUARTERLY else 0

        date_str = epoch.strftime('%Y%j')

        return '{}{:02d}{:02d}_{}'.format(date_str, hour, minute, self)


    def __str__(self):

        if self.value == SlicePeriodicity.DAILY.value: return '01D'
        elif self.value == SlicePeriodicity.QUARTERLY.value: return '15M'
        elif self.value == SlicePeriodicity.HOURLY.value: return '01H'
        else:
            raise ValueError('Undefined SlicePeriodicity value')


# ------------------------------------------------------------------------------

def get_quarter_str(seconds):
    """
    Get the Rinex quarter string ("00", "15", "30", "45") for a given number of seconds
    
    >>> get_quarter_str(100)
    0
    >>> get_quarter_str(920)
    15
    >>> get_quarter_str(1800)
    30
    >>> get_quarter_str(2900)
    45
    >>> get_quarter_str(3600 + 900)
    15
    """
    
    mod_seconds = seconds % 3600
    
    if mod_seconds < 900: return 0
    elif mod_seconds < 1800: return 15
    elif mod_seconds < 2700: return 30
    else: return 45

# ------------------------------------------------------------------------------

def weektow_to_datetime(tow, week):

    delta = datetime.timedelta(weeks=week, seconds=tow)

    return _GPS_TIME_START + delta


def print_bytes(byte_collection, delimiter=" "):
    """
    Output a human readable string (with spaces) of a byte list

    >>> print_bytes(b'\x02\x65)
    '02 65'

    >>> print_bytes(b'\xff\xaa', delimiter"-")
    'ff-aa'
    """

    byte_list = [bytes([b]).hex() for b in byte_collection]
    bytes_str = delimiter.join(byte_list)

    return bytes_str
