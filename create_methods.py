'''
Name: create_methods.py
Author: Blair Gemmer
Version: 20151204
Description:

Automagically create prototype methods using a list of API endpoints. This is useful when implementing a language-specific wrapper for a given API.

The endpoints file should be named "endpoints.txt" and the list should contain names in this format:

HTTP_METHOD <endpoint>

where <endpoint> = endpoint after base URL.

Example:

GET statuses/lists/show.json

will produce the method:

def get_lists_show(self):
	"""
	Implements https://api.twitter.com/1.1/statuses/lists/show.json
	"""
	payload={
	}
	content = self.request(http_method='GET', payload=payload)
	return content

It is up to you to implement the request method to perform a proper API request.

I recommend using the "requests" module.

'''
import os
from collections import OrderedDict

debug = True # Set to True to see output
endpoints_list = 'endpoints.txt'
base_url = 'https://api.twitter.com/1.1/'

with open(endpoints_list, 'r') as infile:
	modified_lines = OrderedDict()

	for line in infile.readlines():
		line = line.rstrip()
		# Remove forward slash, replace spaces with underscores, and return the non-capitalized version:
		modified_line = line.replace('/', ' ').replace(' ', '_').lower()
		if debug:
			print '[Creating method: ] {modified_line}()'.format(modified_line=modified_line)
		modified_lines[modified_line] = line

methods_file = 'api_methods.txt'
with open(methods_file, 'a+') as outfile:
	for modified_line, original_line in modified_lines.iteritems():
		http_method = original_line.split(' ')[0]
		original_line = original_line.split(' ')[1]

		final_output = 'def '
		final_output += modified_line
		final_output += '(self):\n'
		final_output += '\t\'\'\'\n'
		final_output += '\tImplements https://api.twitter.com/1.1/statuses/{original_line}.json\n'.format(original_line=original_line)
		final_output += '\t\'\'\'\n'
		final_output += '\tpayload={\n\t}\n'
		final_output += '\tcontent = self.request(http_method=\'{http_method}\', payload=payload)\n'.format(http_method=http_method)
		final_output += '\treturn content\n\n'
	
		outfile.write(final_output)

		if debug:
			print '[Writing to file: ]'
			print final_output