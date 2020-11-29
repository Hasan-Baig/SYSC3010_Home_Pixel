"""
Purpose - Storing all constants for TempSensor node
"""
from logging import DEBUG, INFO

#ThingSpeak Channel for HomePixel TempSensor
WRITE_KEY_D1 = "IJTZGO1YU2WN8EXU"
READ_KEY_D1 = "LBMYHOFDUR5RGS35"
FEED_D1 = "1155221"

#ThingSpeak Channel for Testing TempSensor
WRITE_KEY_D2 = "UCIILDDZUN1STTZ7"
READ_KEY_D2 = "7NNEIYEELFKI1DDX"
FEED_D2 = "1227948"

#ThingSpeak Field Constants
LOCATION_FIELD = 'field1'
NODE_ID_FIELD = 'field2'
FAN_STATUS_FIELD = 'field3'
TEMP_VAL_FIELD = 'field4'
TEST_FIELD = 'field1'

#URL Syntax for TempSensor
READ_URL = "https://api.thingspeak.com/channels/" + \
	   "{CHANNEL_FEED}/fields/1.json?api_key=" + \
	   "{READ_KEY}"
READ_URL_LIMITED = 'https://api.thingspeak.com/channels/' + \
                   '{CHANNEL_FEED}/fields/1.json?results={RESULTS}'

#TempSensor Constants
TEMP_DETECTED = True
TEMP_NOT_DETECTED = False
FAN_ON = True
FAN_OFF = False
ON_INT = 1
OFF_INT = 0
TEMP_SENSOR_NAME = 'tempsensor'

#TempSensor DB constants
TEMP_SENSOR_DB_FILE = 'tempsensor.db'
TEMP_SENSOR_TABLE = 'TempSensor'

#Logging Constants
LOGGING_FORMAT  = '%(asctime)s - %(levelname)s - %(message)s'
LOGGING_DEFAULT_LEVEL = DEBUG
LOGGING_TEST_LEVEL = INFO

#Other Constants
GOOD_STATUS = 200
