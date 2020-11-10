import http.client
import urllib
import logging
import time

key = "IJTZGO1YU2WN8EXU" #API WRITE KEY FOR L2_M_5D

class ThingSpeakWriter():
	def __init__(self, key):
		self.__key = key

	def write(self, fields):
		fields['key'] = self.__key
		status = None
		reason = None
		params = urllib.parse.urlencode(fields)

		logging.debug('Fields: {}'.format(fields))

		headers = {"Content-typeZZe": "application/x-www-form-urlencoded", "Accept": "text/plain"}
		conn = http.client.HTTPConnection("api.thingspeak.com:80")

		try:
			conn.request("POST", "/update", params, headers)
			response = conn.getresponse()
			status = response.status
			reason = response.reason
			conn.close()
		except:
			print ("Connection Failed")

		logging.debug('{0}, {1}'.format(status, reason))
		return status, reason

 

