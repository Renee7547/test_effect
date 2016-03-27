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

with open (file+'/universe.txt') as f:
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

#get the num of statement
count_state = 0
for i in range(len(code)):
	if code[i][0]=='#' or code[i][0].isdigit():
		count_state = count_state+1
#get the num of branch
count_branch = 0
for i in range(len(code)):
	if code[i][0]=='b':
		count_branch = count_branch+1

print count_state
print count_branch

#register the state of each statement
state = [[0]*len(code) for x in range(len(test))]
#register the state of each branch
branch = [[0]*count_branch for x in range(len(test))]

for i in range(len(test)):
	#one test case
	if file == 'replace' or file == 'totinfo':
		os.system(command11+command2[i]+command3)
	else:
		os.system(command12+command2[i]+command3)
		
	with open (file+'/'+file+'.c.gcov') as f1:
		code = f1.read().splitlines()
	code = [x.replace(" ", "") for x in code]
	pos1 = -1
	pos2 = -1
	for j in range(len(code)):
		if code[j][0] == '#':
			pos1 = pos1+1
			state[i][pos1] = 0		
		elif code[j][0].isdigit():
			pos1 = pos1+1
			state[i][pos1] = 1
		elif code[j][0] == 'b':
				pos2 = pos2+1
				if code[j][12].isdigit() and int(code[j][12])!=0:
					branch[i][pos2] = 1
				else:
					branch[i][pos2] = 0

#count for sum of state
count = [0 for x in range(count_state)] 
for i in range(len(test)):
	for j in range(count_state):
		count[j] = count[j] + state[i][j]

#count for total unreach
unreach = 0
for i in range(count_state):
	if count[i] == 0:
		unreach = unreach +1
print 'unreach_state = '+str(unreach)

#count for sum of branch
count_unreach_branch = [0 for x in range(count_branch)]
for i in range(len(test)):
	for j in range(count_branch):
		count_unreach_branch[j] = count_unreach_branch[j]+branch[i][j]

unreach_branch = 0
for i in range(count_branch):
	if count_unreach_branch[i] == 0:
		unreach_branch = unreach_branch+1
print 'unreach_branch = '+str(unreach_branch)

method = sys.argv[2]
sei = count_state - unreach
bei = count_branch - unreach_branch
sc = 0
bc = 0
cover_list_state = [0 for x in range(count_state)]
old_cover_list_state = [0 for x in range(count_state)]
cover_list_branch = [0 for x in range(count_branch)]
old_cover_list_branch = [0 for x in range(count_branch)]
new_state = [[0]*count_state for x in range(len(test))]
new_branch = [[0]*count_branch for x in range(len(test))]
new_test = []
method = 'random'
if method == 'random':
	#For this method, I randomly order the test case
	#and run the test cases in order untill coverage gets adequate
	order = range(len(test))
	random.shuffle(order)
	
	# new_test with new_state and new_branch
	for i in range(len(test)):
		new_state[i] = state[order[i]]
	for i in range(len(test)):
		new_branch[i] = branch[order[i]]
	for i in range(len(test)):
		new_test.append(test[order[i]])
	
	new_order = []
	test_count = 0
	while test_count<len(test) and (cover_count(cover_list_branch)!=bei or cover_count(cover_list_state)!=sei):
		old_cover_count = cover_count(cover_list_state)+cover_count(cover_list_branch)
		#renew cover_list for state and branch
		for m in range(count_state):
			cover_list_state[m] = cover_list_state[m]+new_state[test_count][m]
		for n in range(count_branch):
			cover_list_branch[n] = cover_list_branch[n]+new_branch[test_count][n]
		new_cover_count = cover_count(cover_list_state)+cover_count(cover_list_branch)
		if new_cover_count > old_cover_count:
			new_order.append(test_count)
		test_count = test_count+1

	os.system('rm -rf '+file+'/random_combine.txt')
	for i in range(0, len(new_order)):
		with open(file + '/random_combine.txt', 'a+') as f2:
			f2.write(new_test[new_order[i]]+'\n')

sei = count_state - unreach
bei = count_branch - unreach_branch
sc = 0
bc = 0
cover_list_state = [0 for x in range(count_state)]
old_cover_list_state = [0 for x in range(count_state)]
cover_list_branch = [0 for x in range(count_branch)]
old_cover_list_branch = [0 for x in range(count_branch)]
new_state = [[0]*count_state for x in range(len(test))]
new_branch = [[0]*count_branch for x in range(len(test))]
new_test = []
method = 'total'
if method == 'total':
	count_list = [[0]*2 for x in range(len(test))]
	#initialize
	for i in range(len(test)):
		count_list[i][0] = i
		count_list[i][1] = cover_count(branch[i])+cover_count(state[i])
	sort_count = sorted(count_list, key=get_key, reverse=True)

	for i in range(len(test)):
		new_state[i] = state[sort_count[i][0]]
	for i in range(len(test)):
		new_branch[i] = branch[sort_count[i][0]]
	for i in range(len(test)):
		new_test.append(test[sort_count[i][0]])

	new_order = []
	test_count = 0
	while test_count<len(test) and (cover_count(cover_list_branch)!=bei or cover_count(cover_list_state)!=sei):
		old_cover_count = cover_count(cover_list_state)+cover_count(cover_list_branch)
		for m in range(count_state):
			cover_list_state[m] = cover_list_state[m]+new_state[test_count][m]
		for n in range(count_branch):
			cover_list_branch[n] = cover_list_branch[n]+new_branch[test_count][n]
		new_cover_count = cover_count(cover_list_state)+cover_count(cover_list_branch)
		if new_cover_count > old_cover_count:
			new_order.append(test_count)
		test_count = test_count+1
	
	os.system('rm -rf '+file+'/total_combine.txt')
	for i in range(0, len(new_order)):
		with open(file + '/total_combine.txt', 'a+') as f3:
			f3.write(new_test[new_order[i]]+'\n')

sei = count_state - unreach
bei = count_branch - unreach_branch
sc = 0
bc = 0
cover_list_state = [0 for x in range(count_state)]
old_cover_list_state = [0 for x in range(count_state)]
cover_list_branch = [0 for x in range(count_branch)]
old_cover_list_branch = [0 for x in range(count_branch)]
new_state = [[0]*count_state for x in range(len(test))]
new_branch = [[0]*count_branch for x in range(len(test))]
new_test = []
method = 'add'
if method == 'add':
	next_test = 0
	new_order = []
	temp1 = [0 for x in range(count_state)]
	temp2 = [0 for x in range(count_branch)]

	while cover_count(old_cover_list_branch) != bei or cover_count(old_cover_list_state) != sei:
		#get a test
		sbc = cover_count(old_cover_list_state)+cover_count(old_cover_list_branch)
		for i in range(len(test)):	
			#cover_list
			for k in range(count_state):
				cover_list_state[k] = old_cover_list_state[k] + state[i][k]
			for j in range(count_branch):
				cover_list_branch[j] = old_cover_list_branch[j] + branch[i][j]
			if i not in new_order and cover_count(cover_list_branch)+cover_count(cover_list_state) > sbc: 
				sbc = cover_count(cover_list_branch)+cover_count(cover_list_state)
				select = i
				for m in range(count_state):
					temp1[m] = cover_list_state[m]
				for n in range(count_branch):
					temp2[n] = cover_list_branch[n]
		
		new_order.append(select)
		for m in range(count_state):
			old_cover_list_state[m] = temp1[m]
		for n in range(count_branch):
			old_cover_list_branch[n] = temp2[n]
	
	os.system('rm -rf '+file+'/add_combine.txt')
	for i in range(0, len(new_order)):
		with open(file + '/add_combine.txt', 'a+') as f4:
			f4.write(test[new_order[i]]+'\n')
