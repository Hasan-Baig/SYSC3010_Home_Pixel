"""
Purpose - Storing all constants for ThingSpeak Channel
"""

#ThingSpeak Channel for HomePixel TempSensor
WRITE_KEY_D1 = "IJTZGO1YU2WN8EXU"
READ_KEY_D1 = "LBMYHOFDUR5RGS35"
FEED_D1 = "1155221"

#ThingSpeak Channel for Testing TempSensor
WRITE_KEY_D2 = "UCIILDDZUN1STTZ7"
READ_KEY_D2 = "7NNEIYEELFKI1DDX"
FEED_D2 = "1227948"

READ_URL = "https://api.thingspeak.com/channels/" + \
	   "{CHANNEL_FEED}/fields/1.json?api_key=" + \
	   "{READ_KEY}&results={HEADER}"
