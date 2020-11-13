"""
Move API keys to database (temp file)
"""
# ThingSpeak Channel for HomePixel SecuritySystem
L2_M_5A1_WRITE_KEY = '4ZYI2SW67KJBJR6A'
L2_M_5A1_READ_KEY = 'RZGQ9FXZIQX5LZUP'
L2_M_5A1_FEED = '1152483'

# ThingSpeak Channel for SecuritySystem testing
L2_M_5A2_WRITE_KEY = 'B8IMPW6Y5OSC47MJ'
L2_M_5A2_READ_KEY = '88DYKYTO4OQ2BT2U'
L2_M_5A2_FEED = '1152488'

# URL Syntax for LightClapper
READ_URL = 'https://api.thingspeak.com/channels/' + \
           '{CHANNEL_FEED}/fields/1.json?api_key=' + \
           '{READ_KEY}&results={HEADER}'

# Other constants
GOOD_STATUS = 200