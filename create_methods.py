'''
Name: create_methods.py
Author: Blair Gemmer
Version: 20151204
Description:

Automagically creates prototype methods using a list of API endpoints. This is useful when implementing a language-specific wrapper for a given API.

Place the endpoints file in the source folder of a name that makes sense, such as "twitter".

The endpoints file should be named "endpoints.txt" and the list should contain names in this format:

HTTP_METHOD <endpoint> <parameters>

where <endpoint> = endpoint after base URL and <parameters> are all available parameters for the API method.

Example:

GET statuses/mentions_timeline count since_id max_id trim_user contributor_details include_entities

will produce the method:

def get_statuses_mentions_timeline(self, count='', since_id='', max_id='', trim_user='', contributor_details='', include_entities=''):
	"""
	Implements https://api.twitter.com/1.1//statuses/mentions_timeline.json
	Documentation URL: https://dev.twitter.com/rest/reference/get/statuses/mentions_timeline
	"""
	payload={
		'count':count,
		'since_id':since_id,
		'max_id':max_id,
		'trim_user':trim_user,
		'contributor_details':contributor_details,
		'include_entities':include_entities
	}
	content = self.request(http_method='GET', payload=payload)
	return content

It is up to you to implement the request method to perform a proper API request.

I recommend using the "requests" module.

As a side piece, it will create a nice JSON data file for you to use to implement any future projects.

This JSON file will be called "<source_folder>_api_data.json", where <source_folder> is the name of the folder you placed "endpoints.txt" in.

In this Twitter Rest API example, it would be called "twitter_rest_api_data.json" for the "twitter_rest" source folder.
'''
import os, errno
import json
from collections import OrderedDict

def create_methods(source_folder='twitter', base_url='https://api.twitter.com/1.1/', docs_url = 'https://dev.twitter.com/rest/reference/', debug=True):
	'''
	Given a source folder name, base url, and documentation url, automagically creates prototype methods using a list of API endpoints and places them in a 
	file called api_methods.txt
	'''
	Create a JSON file for easier readability:
	create_json(source_folder=source_folder, base_url=base_url, docs_url = docs_url, debug=debug)
	json_file = os.path.join(source_folder, source_folder+'_api_data.json')
	with open(json_file) as infile:
		api = json.load(infile)

	# debug = debug # Set to True to see output
	# endpoints_list = os.path.join(source_folder, 'endpoints.txt')
	# base_url = base_url
	# docs_url = docs_url
	# modified_lines = OrderedDict()
	# with open(endpoints_list, 'r') as infile:				
	# 	for line in infile.readlines():
	# 		line = line.rstrip()
	# 		modified_line = line.replace('/', ' ').replace(' ', '_').lower()
	# 		modified_lines[modified_line] = line
	methods_file = os.path.join(source_folder, 'api_methods.txt') # keep
	with open(methods_file, 'a+') as outfile: # keep
		# for modified_line, original_url in modified_lines.iteritems():
		# 	if debug:
		# 		print '[Creating method: ] {modified_line}()\n'.format(modified_line=modified_line)
		# 	http_method = original_url.split(' ')[0]
		# 	original_url = original_url.split(' ')[1]

		# 	final_output = 'def '
		# 	final_output += modified_line
		# 	final_output += '(self):\n'
		# 	final_output += '\t\'\'\'\n'
		# 	final_output += '\tImplements {base_url}/{original_url}.json\n'.format(base_url=base_url, original_url=original_url)
		# 	final_output += '\tDocumentation URL: {docs_url}{http_method}/{original_url}\n'.format(docs_url=docs_url, http_method=http_method.lower(), original_url=original_url)
		# 	final_output += '\t\'\'\'\n'
		# 	final_output += '\tpayload={\n\t}\n'
		# 	final_output += '\tcontent = self.request(http_method=\'{http_method}\', payload=payload)\n'.format(http_method=http_method)
		# 	final_output += '\treturn content\n\n'
		
		# 	outfile.write(final_output)

		# 	if debug:
		# 		print '[Writing to file: ]'
		# 		print final_output

def create_json(source_folder='twitter', base_url='https://api.twitter.com/1.1/', docs_url = 'https://dev.twitter.com/rest/reference/', debug=True):
	'''
	Given a source folder name, base url, and documentation url, automagically creates JSON data from the list of API endpoints and places it in
	a file called <source_folder>_api_data.json, where <source_folder> = the given source folder name.
	'''
	debug = debug # Set to True to see output
	endpoints_list = os.path.join(source_folder, 'endpoints.txt')
	base_url = base_url
	docs_url = docs_url

	json_text = OrderedDict()
	json_text['base_url'] = base_url
	json_text['docs_url'] = docs_url
	json_text['endpoints'] = []
	with open(endpoints_list, 'r') as infile:				
		for line in infile.readlines():
			api_endpoint = {}
			line = line.rstrip() # Original line, with newline stripped out			
			split_line = line.split(' ') # Split them up with spaces
			method_and_url = split_line[0:2] # Grab the first two entries
			method_and_url = ' '.join(method_and_url) # and join them with a space
			# Remove forward slash, replace spaces with underscores, and return the non-capitalized version:
			wrapper_format = method_and_url.replace('/', ' ').replace(' ', '_').lower()
			parameters = split_line[2:len(split_line)] # Grab all other entries (the parameters)			
			http_method = split_line[0] # Grab just the http method
			original_url = split_line[1] # Grab just the URL
			resource_url = '{base_url}{original_url}.json\n'.format(base_url=base_url, original_url=original_url)
			documentation_url = '{docs_url}{http_method}/{original_url}\n'.format(docs_url=docs_url, http_method=http_method.lower(), original_url=original_url)
			if debug:
				print '[Reading Line: ]', line+'\n'
				print 'Original Line:', line
				print 'HTTP Method and URL:', method_and_url 
				print 'API Method Parameters:', parameters 
				print 'Final Wrapper Format: {wrapper_format}()'.format(wrapper_format=wrapper_format)
				print 'Resource URL:', resource_url
				print 'Documentation URL:', documentation_url
				print '----------------------------------------------------\n'
			# Populate the api_endpoint dictionary:
			api_endpoint['original_url'] = line
			api_endpoint['wrapper_format'] = wrapper_format
			api_endpoint['parameters'] = parameters
			api_endpoint['resource_url'] = resource_url
			api_endpoint['documentation_url'] = documentation_url
			# And add it to our JSON text:
			json_text['endpoints'].append(api_endpoint)			
	json_file = os.path.join(source_folder, source_folder+'_api_data.json')
	# Remove the file if it already exists:
	try:
		os.remove(json_file)
	except OSError as e: # this would be "except OSError, e:" before Python 2.6
		if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
			raise # re-raise exception if a different error occured
	# and then just create it:
	with open(json_file, 'a+') as outfile:
			json.dump(json_text, outfile)

if __name__ == '__main__':
	source_folder='twitter_rest'
	base_url='https://api.twitter.com/1.1/'
	docs_url = 'https://dev.twitter.com/rest/reference/' # twitter_rest and twitter_collections
	debug=True
	#docs_url = 'https://dev.twitter.com/oauth/' # twitter_oauth

	create_methods(source_folder=source_folder, base_url=base_url, docs_url = docs_url, debug=debug)
	



