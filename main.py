import sys, os, shutil, pprint, csv, zipfile, pip, time
from ftplib import FTP
from keboola import docker

cfg = docker.Config('/data/')
parameters = cfg.get_parameters()
config = {}
configFields = ['bucket', 'host', 'username', '#password', 'folder', 'file']

for field in configFields:
	config[field] = parameters.get(field)

	if not config[field]:
		raise Exception('Missing mandatory configuration field: '+field)


def processFile(fileName):
	entity = fileName.replace('.csv','')
	tableDestination = "/data/out/tables/in.c-"+config['bucket']+"."+entity
	writeHeader = True

	if os.path.isfile("/data/out/tables/in.c-"+config['bucket']+"."+entity):
		writeHeader = False

	counter = 0
	with open(fileName, 'r', encoding='utf-8') as fin, open(tableDestination, 'a', encoding='utf-8') as fout:
		for line in fin:
			if writeHeader == True:
				header = line.replace(" ", "_")
				header = header.replace("(", "")
				header = header.replace(")", "")
				header = header.replace("%", "pct")
				header = '"index"'+header
				
				fout.write(header)
				writeHeader = False
			elif writeHeader == False and counter == 0:
				pass
			else:
				if len(line) > 1:
					fout.write(line)
			counter += 1

def downloadFiles():
	ftp = FTP(config['host'])
	ftp.login(user=config['username'], passwd = config['#password'])

	ftp.cwd(config['folder'])

	newFilename = config['file'].replace(".csv", "")
	newFilename = newFilename+time.strftime("_%Y-%m-%d.csv")

	try:
		ftp.rename(config['file'], newFilename)
	except:
		pass

	localfile = open(config['file'], 'wb')
	ftp.retrbinary('RETR ' + newFilename, localfile.write, 1024)

	ftp.quit()
	localfile.close()

	processFile(config['file'])

downloadFiles()


