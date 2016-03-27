#!/usr/bin/env python

import os
import sys
import random

def cover_count(list):
	count = 0
	for i in list:
		if i > 0:
			count = count+1
	return count

def get_key(item):
	return item[1]

command2 = []
file = sys.argv[1]

method = sys.argv[2]
if method == 'random':
	with open (file+'/random_branch.txt') as f:
		test = f.read().splitlines()
if method == 'total':
	with open (file+'/total_branch.txt') as f:
		test = f.read().splitlines()
if method == 'add':
	with open (file+'/add_branch.txt') as f:
		test = f.read().splitlines()

command11 = 'cd ' + file + '; gcc -fprofile-arcs -ftest-coverage -g -o '+file+' '+file+'.c -lm 2> temp1; '
command12 = 'cd ' + file + '; gcc -fprofile-arcs -ftest-coverage -g -o '+file+' '+file+'.c 2> temp1; '
for i in range(len(test)):
	command2.append(file+' '+test[i]+' >temp2')
command3 ='; gcov -b -c '+file+' > temp3'

#get the length of .gcov
if file == 'replace' or file == 'totinfo':
	os.system(command11+command2[0]+command3)
else:
	os.system(command12+command2[0]+command3)

with open (file+'/'+file+'.c.gcov') as f1:
	code = f1.read().splitlines()
code = [x.replace(" ", "") for x in code]

#get the num of branch
count_branch = 0
for i in range(len(code)):
	if code[i][0]=='b':
		count_branch = count_branch+1

#register the state of each statement
state = [[0]*len(code) for x in range(len(test))]
#register the state of each branch
branch = [[0]*count_branch for x in range(len(test))]
#count for total

for i in range(len(test)):
	#one test case
	if file == 'replace' or file == 'totinfo':
		os.system(command11+command2[i]+command3)
	else:
		os.system(command12+command2[i]+command3)
		
	with open (file+'/'+file+'.c.gcov') as f1:
		code = f1.read().splitlines()
	code = [x.replace(" ", "") for x in code]
	pos = -1
	for j in range(len(code)):
		if code[j][0] == '#':
			state[i][j] = 0		
		elif code[j][0].isdigit():
			state[i][j] = 1
		else:
			state[i][j] = -1
			if code[j][0] == 'b':
				pos = pos+1
				if code[j][12].isdigit() and int(code[j][12])!=0:
					branch[i][pos] = 1
				else:
					branch[i][pos] = 0

#count for sum of branch
count_unreach_branch = [0 for x in range(count_branch)]
for i in range(len(test)):
	for j in range(count_branch):
		count_unreach_branch[j] = count_unreach_branch[j]+branch[i][j]

count = 0
for i in range(count_branch):
	if count_unreach_branch[i] > 0:
		count = count + 1
unreach = int(sys.argv[3])
print count_branch
print float(count)/(count_branch-unreach)
