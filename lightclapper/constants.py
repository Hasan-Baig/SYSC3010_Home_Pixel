"""
constants.py
Some data in here will move to a database later
"""
# ThingSpeak Channel for HomePixel LightClapper
L2_M_5C1_WRITE_KEY = 'NA12OT85I0GT61HO'
L2_M_5C1_READ_KEY = 'YHMOLLMTKT2ENCK9'
L2_M_5C1_FEED = '1150656'

# ThingSpeak Channel for LightClapper testing
L2_M_5C2_WRITE_KEY = 'L8I9PFNVXGV9K5DX'
L2_M_5C2_READ_KEY = '1FN82DN1D6QAOIR2'
L2_M_5C2_FEED = '1208490'

# URL Syntax for LightClapper
READ_URL = 'https://api.thingspeak.com/channels/' + \
           '{CHANNEL_FEED}/fields/1.json?api_key=' + \
           '{READ_KEY}&results={HEADER}'

# Other constants
GOOD_STATUS = 200
