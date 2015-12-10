'''
Name: create_methods.py
Author: Blair Gemmer
Version: 20151204
Description:

Automagically creates prototype methods using a list of API endpoints. This is useful when implementing a language-specific wrapper for a given API.

Place the endpoints file in the source folder of a name that makes sense, such as "twitter".

The endpoints file should be named "endpoints.txt" and the list should contain names in this format:

HTTP_METHOD <endpoint>

where <endpoint> = endpoint after base URL.

Example:

GET statuses/mentions_timeline

will produce the method:

def get_statuses_mentions_timeline(self):
	"""
	Implements https://api.twitter.com/1.1//statuses/mentions_timeline.json
	Documentation URL: https://dev.twitter.com/rest/reference/get/statuses/mentions_timeline
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

def create_methods(source_folder='twitter', base_url='https://api.twitter.com/1.1/', docs_url = 'https://dev.twitter.com/rest/reference/', debug=True):
	'''
	Given a source folder name, base url, and documentation url, automagically creates prototype methods using a list of API endpoints and places them in a 
	file called api_methods.txt
	'''
	debug = debug # Set to True to see output
	endpoints_list = os.path.join(source_folder, 'endpoints.txt')
	base_url = base_url
	docs_url = docs_url
	with open(endpoints_list, 'r') as infile:
		modified_lines = OrderedDict()

		for line in infile.readlines():
			line = line.rstrip()
			# Remove forward slash, replace spaces with underscores, and return the non-capitalized version:
			modified_line = line.replace('/', ' ').replace(' ', '_').lower()
			if debug:
				print '[Creating method: ] {modified_line}()'.format(modified_line=modified_line)
			modified_lines[modified_line] = line

	methods_file = os.path.join(source_folder, 'api_methods.txt')
	with open(methods_file, 'a+') as outfile:
		for modified_line, original_line in modified_lines.iteritems():
			http_method = original_line.split(' ')[0]
			original_line = original_line.split(' ')[1]

			final_output = 'def '
			final_output += modified_line
			final_output += '(self):\n'
			final_output += '\t\'\'\'\n'
			final_output += '\tImplements {base_url}/{original_line}.json\n'.format(base_url=base_url, original_line=original_line)
			final_output += '\tDocumentation URL: {docs_url}{http_method}/{original_line}\n'.format(docs_url=docs_url, http_method=http_method.lower(), original_line=original_line)
			final_output += '\t\'\'\'\n'
			final_output += '\tpayload={\n\t}\n'
			final_output += '\tcontent = self.request(http_method=\'{http_method}\', payload=payload)\n'.format(http_method=http_method)
			final_output += '\treturn content\n\n'
		
			outfile.write(final_output)

			if debug:
				print '[Writing to file: ]'
				print final_output

def create_json(source_folder='twitter', base_url='https://api.twitter.com/1.1/', docs_url = 'https://dev.twitter.com/rest/reference/', debug=True):
	'''
	Given a source folder name, base url, and documentation url, automagically creates JSON data from the list of API endpoints and places it in
	a file called <source_folder>_api_data.json, where <source_folder> = the given source folder name.
	'''
	pass

if __name__ == '__main__':
	source_folder='twitter'
	base_url='https://api.twitter.com/1.1/'
	docs_url = 'https://dev.twitter.com/rest/reference/'
	debug=True
	#create_methods(source_folder=source_folder, base_url=base_url, docs_url = docs_url, debug=debug)
	create_json(source_folder=source_folder, base_url=base_url, docs_url = docs_url, debug=debug)



