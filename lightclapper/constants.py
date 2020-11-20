"""
constants.py
"""
from logging import DEBUG, INFO

# ThingSpeak Channel for HomePixel LightClapper
L2_M_5C1_WRITE_KEY = 'NA12OT85I0GT61HO'
L2_M_5C1_READ_KEY = 'YHMOLLMTKT2ENCK9'
L2_M_5C1_FEED = '1150656'

# ThingSpeak Channel for LightClapper testing
L2_M_5C2_WRITE_KEY = 'L8I9PFNVXGV9K5DX'
L2_M_5C2_READ_KEY = '1FN82DN1D6QAOIR2'
L2_M_5C2_FEED = '1208490'

# ThingSpeak Field Constants
LOCATION_FIELD = 'field1'
NODE_ID_FIELD = 'field2'
LIGHT_STATUS_FIELD = 'field3'
TEST_FIELD = 'field1'

# URL Syntax for LightClapper
READ_URL = 'https://api.thingspeak.com/channels/' + \
           '{CHANNEL_FEED}/feeds.json?api_key=' + \
           '{READ_KEY}'
READ_URL_LIMITED = 'https://api.thingspeak.com/channels/' + \
                   '{CHANNEL_FEED}/fields/1.json?results={RESULTS}'

# LightClapper constants
SOUND_DETECTED = True
SOUND_NOT_DETECTED = False
LED_ON = True
LED_OFF = False
LIGHT_CLAPPER_NAME = 'lightclapper'

# LightClapper DB constants
LIGHT_CLAPPER_DB_FILE = 'lightclapper.db'
LIGHT_CLAPPER_TABLE = 'LightClapper'

# Logging Constants
LOGGING_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOGGING_DEFAULT_LEVEL = DEBUG
LOGGING_TEST_LEVEL = INFO

# Other constants
GOOD_STATUS = 200
