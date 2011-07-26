#!/usr/bin/env python
#Python 2 compatible (tested with 2.7.1+)
#Requires rtmpdump for downloading the flv files, and ffmpeg for converting the flv files to avi

"""ultimoasair.py: Oh, oh. Este script da-lhe sempre em quente!"""

__author__ = "Homes das ilhas";
__copyright__ = "Copyleft 2011, Homes das ilhas";
__credits__ = ["Alexandre Garcia", "Nuno Melo"];
__license__ = "WTFPL";
__version__ = "0.1";

import urllib2;
import os;
import re;
import subprocess;
import sys;

url = "http://rtp.pt/multimediahtml/progVideo.php?tvprog=24118";
source = urllib2.urlopen(url).read();

pattern = re.compile(r"<a href=\"/multimediahtml/video/ultimo-a-sair/([0-9]{4}-[0-9]{2}-[0-9]{2})\">");

res = pattern.findall(source);
res = set(res);

print str(len(res)) + " episodes found.";

eps = {};

pattern = re.compile(r"<li.*?><a href=\".*?Parte\">(.*?)</a></li>", re.DOTALL);

print "Getting link data...";

i = 1;

for item in res:
	sys.stdout.write("[" + str(i) + "/" + str(len(res)) + "] ... ");
	sys.stdout.flush();
	url = "http://rtp.pt/multimediahtml/video/ultimo-a-sair/" + item;
	source = urllib2.urlopen(url).read();
	partes = pattern.findall(source);
	size = len(partes);
	eps[item] = 1 if(size == 0) else size;
	print "OK";
	i+=1;

print "Will begin downloading soon...";

a = "";
while a != "y" and a != "n":
	a = (raw_input("If we find a file that already exists, should we overwrite it? [Y/N]")).lower();

filenames = [];

for k, v in eps.iteritems():
	for i in range(1, v+1):
		ep = k.replace("-", "");
		url = "rtmp://h2e.rtp.pt/fastplay/nas2.share/videos/auto/ultimosair/ultimosair_" + str(i) + "_" + ep + ".flv";
		name = ep + (("_parte_" + str(i)) if v > 1 else "") + ".flv";
		if (not os.path.isfile(name)) or (os.path.isfile(name) and a == "y"):
			filenames.append(name.rstrip('.flv'));
			sys.stdout.write("Downloading " + name + " ... ");
			sys.stdout.flush();
			subprocess.call("rtmpdump -r " + url + " -o " + name, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True);	
			print "OK";

for item in filenames:
	name = item + ".flv";
	dest = item + ".avi";
	print "Converting " + name + " to " + dest;
	try:
		if os.path.isfile(name):
			subprocess.call("ffmpeg -i " + name + " " + dest, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True);
		else:
			print "The file does not exist."
	except OSError as ex:
		print "Conversion failed. Do you have ffmpeg installed?";
