#!/usr/bin/env python

import os
import sys
import glob
import filecmp

def cover_count(list):
	count = 0
	for i in list:
		if i > 0:
			count=count+1 
	return count

'''
def file_exist(rootdir):
	filelist = glob.glob(os.path.join(rootdir, 'output1'))
	if filelist:
		return 1
	else:
		return 0
'''	
faults = []
file = sys.argv[1]
os.chdir(file)
for f in glob.glob("v*"):
	faults.append(f)

command0 = []
for i in range(len(faults)):
	command0.append('cd '+faults[i]+';')

command11 = 'gcc -g -o '+file+' '+file+'.c -lm 2> temp1; '
command12 = 'gcc -g -o '+file+' '+file+'.c 2> temp1; '

input = sys.argv[2]
#test random_statement
with open (input) as f1:
	test = f1.read().splitlines()

open('output', 'w+')
open('output1', 'w+')

command21 = []
command22 = []
for i in range(len(test)):
	#outside
	command21.append('./'+file+' '+test[i]+' >output')
	#inside, for faults
	command22.append('./'+file+' '+test[i]+' >output1')

mark = [0 for x in range(len(faults))]
for i in range(len(test)):
	#one test, get the right output
	if file == 'replace' or file == 'totinfo':
		os.system(command11+command21[i])
	else:
		os.system(command12+command21[i])
	for j in range(len(faults)):
		if file == 'replace' or file == 'totinfo':
			os.system(command0[j]+command11)
			os.system('mv '+faults[j]+'/'+file+ ' ../'+file)
			os.system(command22[i])
		else:
			os.system(command0[j]+command12)
			os.system('mv '+faults[j]+'/'+file+ ' ../'+file)
			os.system(command22[i])
		if not filecmp.cmp('output', 'output1'):
			mark[j] = 1
exposed = []
for i in range(len(faults)):
	if mark[i]>0:
		exposed.append(faults[i])

print float(cover_count(mark))/len(faults)
print exposed
