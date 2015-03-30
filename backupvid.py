#! /usr/bin/python
import subprocess, re, time, argparse, os



def arg_parsing():
	#parse the args
	parser = argparse.ArgumentParser()
	parser.add_argument("-i",
						"--in-dir",
						type = str,
						dest = 'in_dir',
						help = "Directory to be read",
						required = True)
	return parser.parse_args()

args = arg_parsing()
to_convert = []

#Get the iso's in the directory
#something like: GI_S1_D1.iso
for aFile in os.listdir(args.in_dir):
	if aFile.endswith('.iso'):
		temp_dict = {
		"full" : aFile,
		"title": aFile.split('.')[0],
		"show" : aFile.split('_')[0],
		"seas" : aFile.split('_')[1],
		"disc" : aFile.split('_')[2].replace('.iso','')
		}
		to_convert.append(temp_dict)

	#build args to run

for aFile in to_convert:
	to_run = "HandBrakeCLI"\
				+ " --scan"\
				+ " -t"\
				+ " 0"\
				+ " --min-duration"\
				+ " 600"\
				+ " --input=%s" % aFile["full"]

	#run the command
	p1 = subprocess.Popen([to_run], 
						stdout=subprocess.PIPE,
						stderr=subprocess.PIPE,
						shell=True)

	#initialize titles to read
	titles_to_read = []

	#find the titles longer than 6 minutes
	#store the title number in titles_lines
	titles_lines = re.compile(r'\+\s{1}title\s{1}\d+\:')
	for line in p1.communicate()[1].split('\n'):
		match = re.match(titles_lines, line)
		if match:
			temp_match = match.group().replace(':', '')
			titles_to_read.append(temp_match.split(' ')[2])

	#check directory 
	outDir = "%sS%s" %(aFile["show"], aFile["seas"])
	if not os.path.isdir(outDir):
		os.mkdir(outDir)

	#write each title to its own file
	for title in titles_to_read:
		outfile = outDir + "D" + str(aFile["disc"]) + "_E" + str(title)
		output = outDir + os.sep + outfile + ".mp4"
		to_run = "HandBrakeCLI"\
					+ " -t"\
					+ " %s" % (str(title))\
					+ " --input=%s" % (aFile["full"])\
					+ " --output=%s" % output

		#p2 = subprocess.Popen([to_run],
		#					shell=True)
		os.system(to_run)
