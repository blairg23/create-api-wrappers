'''
Automagically create prototype methods using a list of API endpoints. This is useful when implementing a language-specific wrapper for a given API.

The endpoints file should be named "endpoints.txt" and the list should contain names in this format:

HTTP_METHOD <endpoint>

where <endpoint> = endpoint after base URL.

Example:

GET statuses/mentions_timeline.json

will produce the method:

def get_statuses_mentions_timeline(self):
		"""
		Implements https://api.twitter.com/1.1/statuses/mentions_timeline.json
		"""
		pass

'''
import os

endpoints_list = 'endpoints.txt'
base_url = 'https://api.twitter.com/1.1/'

with open(endpoints_list, 'r') as infile:
	modified_lines = {}
	for line in infile.readlines():
		line = line.rstrip()
		# Remove forward slash, replace spaces with underscores, and return the non-capitalized version:
		modified_line = line.replace('/', ' ').replace(' ', '_').lower()
		print '[Creating method: ] {modified_line}()'.format(modified_line=modified_line)
		modified_lines[modified_line] = line.split(' ')[1]		

methods_file = 'api_methods.txt'
with open(methods_file, 'a+') as outfile:
	for modified_line, original_line in modified_lines.iteritems():
		final_output = 'def '
		final_output += modified_line
		final_output += '(self):\n'
		final_output += '\t\'\'\'\n'
		final_output += '\tImplements https://api.twitter.com/1.1/statuses/{original_line}.json\n'.format(original_line=original_line)
		final_output += '\t\'\'\'\n'
		final_output += '\tpass\n\n'
		outfile.write(final_output)
