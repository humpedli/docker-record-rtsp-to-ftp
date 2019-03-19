#!/usr/bin/env python
#
# This file is licensed under the terms of the GPL, Version 3
#
# Copyright 2018 Tamas Kinsztler <https://github.com/humpedli>

__author__ = 'Tamas Kinsztler'
__copyright__ = 'Copyright (C) Tamas Kinsztler'
__license__ = 'GPLv3'
__version__ = '1.0'

import os
import sys
import json
from datetime import datetime
from sys import argv
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import threading

# HTTP server class
class MyServer(BaseHTTPRequestHandler):
	def _set_headers(self):
		self.send_response(200)
		self.send_header('Content-type', 'application/json')
		self.end_headers()

	def do_HEAD(self):
		self._set_headers()

	def do_POST(self):
		content_length = int(self.headers['Content-Length'])
		post_data = json.loads(self.rfile.read(content_length))
		try:
			if post_data['name'] and post_data['duration'] and post_data['stream_url'] and post_data['ftp_url']:
				t = threading.Thread(target=record_and_upload, args=[post_data])
				t.setDaemon(False)
				t.start()
				self._set_headers()
				self.wfile.write('{"done": true}')
				
		except Exception as e:
			print(e)
			self._set_headers()
			self.wfile.write('{"done": false}')

# Record and upload data
def record_and_upload(post_data):
	file_name = datetime.today().strftime('%Y%m%d_%H%M%S') + '_' + post_data['name'] + '.mov'
	os.system(('avconv -rtsp_transport tcp -y -i %s -vcodec copy -an -strict experimental -t %s /tmp/%s && curl --upload-file /tmp/%s %s%s && rm /tmp/%s > /dev/null') % (post_data['stream_url'], post_data['duration'], file_name, file_name, post_data['ftp_url'], '/' + file_name, file_name))
	print ('Recorded and uploaded file: %s') % (file_name)

# Main Loop
def main_loop(port=11122):
	print ('Started http server on port: %s') % (port)
	HTTPServer(('', port), MyServer).serve_forever()

# Start main loop
try:
	if len(argv) == 2:
		main_loop(port=int(argv[1]))
	else:
		main_loop()
except KeyboardInterrupt:
	print ('Interrupted by keypress')
	sys.exit(0)
