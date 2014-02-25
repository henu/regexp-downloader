#!/usr/bin/python
import sys
import re

def main():
	# Read arguments
	if len(sys.argv) != 4:
		raise Exception('Invalid arguments! Usage: ' + sys.argv[0] + '<initial URL> <regexp of URLs to crawl> <regexp of URLs to download>')
	initurl = sys.argv[1]
	try:
		crawl_re = re.compile(sys.argv[2])
	except:
		raise Exception('Regexp of URLs to crawl is not valid!')
	try:
		download_re = re.compile(sys.argv[3])
	except:
		raise Exception('Regexp of URLs to download is not valid!')

if __name__ == '__main__':
	try:
		main()
	except Exception as e:
		print 'ERROR: ' + str(e)
		sys.exit(1)
	sys.exit(0)

