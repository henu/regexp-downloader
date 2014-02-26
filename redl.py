#!/usr/bin/python
import sys
import re
import urllib
import os
import BeautifulSoup
import urlparse

def main():

	urls_met = set()
	urls_to_handle = []

	# Read arguments
	if len(sys.argv) != 4:
		raise Exception('Invalid arguments! Usage: ' + sys.argv[0] + ' <initial URL> <regexp of URLs to crawl> <regexp of URLs to download>')
	initurl = sys.argv[1]
	try:
		crawl_re = re.compile(sys.argv[2])
	except:
		raise Exception('Regexp of URLs to crawl is not valid!')
	try:
		download_re = re.compile(sys.argv[3])
	except:
		raise Exception('Regexp of URLs to download is not valid!')

	# Add initial URL to the containers
	urls_met.add(initurl)
	urls_to_handle.append(initurl)

	# Start handling urls
	urls_checked = 0
	urls_to_handle_total = 1
	while len(urls_to_handle) > 0:
		url = urls_to_handle.pop()
		urls_checked += 1
		# TODO: Support robots.txt!

		print str(urls_checked) + '/' + str(urls_to_handle_total) + ': Checking ' + url

		# Download URL
		request = urllib.urlopen(url)
		content_type = request.info().type
		content = request.read()
		request.close()

		# Check if this URL should be downloaded
		if download_re.match(url):
			print '\tSaving...'
			filename = url.replace('/', '_').replace(':', '_')
			# If filename already exist, then decide another filename
			if os.path.exists(filename):
				extra_num = 1
				while os.path.exists(filename + '_' + str(extra_num)):
					extra_num += 1
			# Save file
			f = open(filename, 'wb')
			f.write(content)
			f.close()

		# Check if this URL should be crawled
		if not crawl_re.match(url):
			continue

		# If type cannot be scanned for more URLs, then skip it
		if content_type != 'text/html':
			continue

		print '\tScanning for more URLs...'

		# Remove embedded javascript, since it may cause errors
		while content.count("<script"):
			script_begin = content.find("<script")
			script_end = content.find("</script>", script_begin)
			content = content[0:script_begin] + content[script_end+9:]

		soup = BeautifulSoup.BeautifulSoup(content)

		# Find more URLs
		a_tags = soup.findAll("a")
		for a_tag in a_tags:
			# Get URL and ensure it is valid
			try:
				a_url = a_tag["href"]
			except KeyError:
				continue

			# If URL is relative, then make it absolute
			if len(a_url) > 0 and a_url[0] == '/':
				a_url = urlparse.urljoin(url, a_url)

			# Clean fragment identifier
			hash_pos = a_url.find('#')
			if (hash_pos >= 0):
				a_url = a_url[0:hash_pos]

			# If URL is already met, then ignore it
			if a_url in urls_met:
				continue

			# Add URL to containers. Prioritize
			# URLs that need downloading
			urls_met.add(a_url)
			if download_re.match(a_url):
				urls_to_handle.append(a_url)
				urls_to_handle_total += 1
			elif crawl_re.match(a_url):
				urls_to_handle.insert(0, a_url)
				urls_to_handle_total += 1
if __name__ == '__main__':
	try:
		main()
	except Exception as e:
		print 'ERROR: ' + str(e)
		sys.exit(1)
	sys.exit(0)

