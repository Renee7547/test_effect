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

command2 = []
file = sys.argv[1]
method = sys.argv[2]

if method == 'random':
	with open (file+'/random_combine.txt') as f:
		test = f.read().splitlines()

elif method == 'total':
	with open (file+'/total_statement.txt') as f:
		test = f.read().splitlines()

elif method == 'add':
	with open (file+'/add_statement.txt') as f:
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

#count for total
count_state = 0
for i in range(len(code)):
	if code[i][0].isdigit() or code[i][0]=='#':
		count_state = count_state+1

#register the state of each statement
state = [[0]*count_state for x in range(len(test))]

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
			pos = pos+1
			state[i][pos] = 0		
		elif code[j][0].isdigit():
			pos = pos+1
			state[i][pos] = 1

#count for sum of state
count = [0 for x in range(count_state)] 
for j in range(count_state):
	for i in range(len(test)):
		count[j] = count[j] + state[i][j] 

unreach = int(sys.argv[3])
sei = count_state - unreach
sc = 0
cover_list = [0 for x in range(count_state)]

#For this method, I randomly order the test case
#and run the test cases in order untill coverage gets adequate
	
for j in range(count_state):
	for i in range(len(test)):
		cover_list[j] = cover_list[j]+state[i][j]
print sei
print float(cover_count(cover_list))/sei
print cover_count(cover_list)
