'''
Downloads all of the provided urls from youtube and converts them into MP3 files

Author: Brandon Layton
'''
from tkinter import *
from tkinter.filedialog import askdirectory

import os, sys, getopt
import subprocess as sub
from multiprocessing import *

def download(args):
	url = args[0]
	fileDir = args[1]

	filePath = ""
	convertedPath = ""

	p = sub.Popen(".\\dependencies\\youtube-dl.exe --get-title " + url, stdout=sub.PIPE,stderr=sub.PIPE)
	output, errors = p.communicate()
	title = str(output,"ASCII").split("\r\n")[0]

	print("youtubedl - " + title)
	finalPath = fileDir+"\\"+title+".mp3"
	if os.path.isfile(finalPath):
		print("Already exists")
	else:
		p = sub.Popen(".\\dependencies\\youtube-dl.exe " + url, stdout=sub.PIPE,stderr=sub.PIPE)
		output, errors = p.communicate()
		res = str(output,"ASCII")
		try:
			filePath = res.split("Destination: ")[1].split("\r\n")[0];
			convertedPath = title.replace("\"","") + ".wav"
			print(filePath)

			print("FFMPEG - " + title)
			p = sub.Popen(".\\dependencies\\ffmpeg\\bin\\ffmpeg.exe -i \"%s\" \"%s\""%(filePath,convertedPath), stdout=sub.PIPE,stderr=sub.PIPE)
			output, errors = p.communicate()

			print("LAME - " + title)
			p = sub.Popen(".\\dependencies\\lame.exe \"%s\" \"%s\""%(convertedPath,finalPath), stdout=sub.PIPE,stderr=sub.PIPE)
			output, errors = p.communicate()
			os.remove(filePath)
			os.remove(convertedPath)
			while(os.path.isfile(convertedPath) or os.path.isfile(filePath)):pass
		except Exception as e:
			print("Error. Possibly the downloaded item already exists:\n"+
				  "#####"+e)
	print("DONE - " + title)

def remove(args):
	try:
		print("remove: " + str(args[0]))
		os.remove(args[0])
	except:pass
	args[1].put("Result!")


if __name__ == '__main__':
	urls = []
	mMap = []
	maxPoolSize = 5
	
	try:
		opts, args = getopt.getopt(sys.argv,"s:")
	except getopt.GetoptError:
		print('massYoutuber.py -s <maxPoolSize (default = 5)>')
		sys.exit(2)
	for opt, arg in opts:
		if opt=='-s':
			maxPoolSize = arg	

	fname = askdirectory(title="What folder to save music into?")
	Tk().destroy()
	
	f = open("urls.txt","r")

	for line in f:
		urls.append(line)

	for url in urls:
		mMap.append((""+url,""+fname))

	p = Pool(5)
	p.map(download, mMap)

	print("DONE! :D")