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

# SMS API using Nexmo
SMS_API_KEY = '2d73a813'
SMS_API_SECRET = 'FdjEZXyRZAG4gHao'
FROM_NUMBER = '12264088542'
TO_NUMBER = '16139839862'          

# Google Email for link
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587 
GMAIL_USERNAME = 'sysc3010homepixel@gmail.com' 
GMAIL_PASSWORD = 'homepixel3010'


# Other constants
GOOD_STATUS = 200