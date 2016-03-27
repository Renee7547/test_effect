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

#get the num of branch
count_branch = 0
branch_exec = 0
for i in range(len(code)):
	if code[i][0]=='b':
		count_branch = count_branch+1
print count_branch
#register the state of each statement
state = [[0]*len(code) for x in range(len(test))]
#register the state of each branch
branch = [[0]*count_branch for x in range(len(test))]
#count for total
invalid_state = 0
for i in range(len(code)):
	if code[i][0]=='-' or code[i][0]=='b' or code[i][0]=='c':
		invalid_state = invalid_state+1

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
'''
#count for sum of state
count = [0 for x in range(len(code))] 
for i in range(len(test)):
	for j in range(len(code)):
		count[j] = count[j] + state[i][j]

#count for total
count_t = len(code)-invalid_state
unreach = 0
for i in range(len(code)):
	if count[i] == 0:
		unreach = unreach +1
print 'unreach = '+str(unreach)
'''

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
bei = count_branch - unreach_branch
bc = 0
cover_list_branch = [0 for x in range(count_branch)]
old_cover_list_branch = [0 for x in range(count_branch)]
new_branch = [[0]*count_branch for x in range(len(test))]
new_test_branch = []
method = 'random'
if method == 'random':
	rand_test_branch = []
	#For this method, I randomly order the test case
	#and run the test cases in order untill coverage gets adequate
	order_branch = range(len(test))
	random.shuffle(order_branch)
	
	for i in range(len(test)):
		new_branch[i] = branch[order_branch[i]]
	for i in range(len(test)):
		new_test_branch.append(test[order_branch[i]])
	
	new_order_branch = []
	test_count = -1
	while test_count<len(test) and cover_count(cover_list_branch) != bei:
		test_count = test_count+1
		old_cover_count = cover_count(cover_list_branch)
		for j in range(count_branch):
			cover_list_branch[j] = cover_list_branch[j]+new_branch[test_count][j]
		new_cover_count = cover_count(cover_list_branch)
		if new_cover_count > old_cover_count:
			new_order_branch.append(test_count)

	size = len(new_order_branch)
	os.system('rm -rf '+file+'/random_branch.txt')
	for i in range(0, size):
		with open(file + '/random_branch.txt', 'a+') as f2:
			f2.write(new_test_branch[new_order_branch[i]]+'\n')

bei = count_branch - unreach_branch
bc = 0
cover_list_branch = [0 for x in range(count_branch)]
old_cover_list_branch = [0 for x in range(count_branch)]
new_branch = [[0]*count_branch for x in range(len(test))]
new_test_branch = []
method = 'total'
if method == 'total':
	count_list = [[0]*2 for x in range(len(test))]
	#initialize
	for i in range(len(test)):
		count_list[i][0] = i
		count_list[i][1] = cover_count(branch[i])
	sort_count = sorted(count_list, key=get_key, reverse=True)

	for i in range(len(test)):
		new_branch[i] = branch[sort_count[i][0]]
	for i in range(len(test)):
		new_test_branch.append(test[sort_count[i][0]])

	new_order = []
	test_count = -1
	while test_count<len(test) and cover_count(cover_list_branch) != bei:
		test_count = test_count+1
		old_cover_count = cover_count(cover_list_branch)
		for j in range(count_branch):
			cover_list_branch[j] = cover_list_branch[j]+new_branch[test_count][j]
		new_cover_count = cover_count(cover_list_branch)
		if new_cover_count > old_cover_count:
			new_order.append(test_count)
	
	os.system('rm -rf '+file+'/total_branch.txt')
	for i in range(0, len(new_order)):
		with open(file + '/total_branch.txt', 'a+') as f3:
			f3.write(new_test_branch[new_order[i]]+'\n')

bei = count_branch - unreach_branch
bc = 0
cover_list_branch = [0 for x in range(count_branch)]
old_cover_list_branch = [0 for x in range(count_branch)]
new_branch = [[0]*count_branch for x in range(len(test))]
new_test_branch = []
method = 'add'
if method == 'add':
	next_test = 0
	new_order = []
	temp = [0 for x in range(count_branch)]

	while cover_count(old_cover_list_branch) != bei:
		#get a test
		bc = cover_count(old_cover_list_branch)
		for i in range(len(test)):	
			#cover_list
			for j in range(count_branch):
				cover_list_branch[j] = old_cover_list_branch[j] + branch[i][j]
			if i not in new_order and cover_count(cover_list_branch) > bc: 
				bc = cover_count(cover_list_branch)
				select = i
				for m in range(count_branch):
					temp[m] = cover_list_branch[m]
		
		new_order.append(select)
		for n in range(count_branch):
			old_cover_list_branch[n] = temp[n]
	
	os.system('rm -rf '+file+'/add_branch.txt')
	for i in range(0, len(new_order)):
		with open(file + '/add_branch.txt', 'a+') as f4:
			f4.write(test[new_order[i]]+'\n')


'''
method = sys.argv[2]
sei = count_t - unreach
sc = 0
cover_list = [0 for x in range(len(code))]
old_cover_list = [0 for x in range(len(code))]
new_state = [[0]*len(code) for x in range(len(test))]
new_test = []
method = 'random'
if method == 'random':
	rand_test = []
	#For this method, I randomly order the test case
	#and run the test cases in order untill coverage gets adequate
	order = range(len(test))
	random.shuffle(order)
	
	for i in range(len(test)):
		new_state[i] = state[order[i]]
	for i in range(len(test)):
		new_test.append(test[order[i]])
	
	new_order = []
	test_count = -1
	while test_count<len(test) and cover_count(cover_list) != sei:
		test_count = test_count+1
		old_cover_count = cover_count(cover_list)
		for j in range(len(code)):
			cover_list[j] = cover_list[j]+new_state[test_count][j]
		new_cover_count = cover_count(cover_list)
		if new_cover_count > old_cover_count:
			new_order.append(test_count)

	size = len(new_order)
	os.system('rm -rf '+file+'/random_branch.txt')
	for i in range(0, size):
		with open(file + '/random_branch.txt', 'a+') as f2:
			f2.write(new_test[new_order[i]]+'\n')

sc = 0
cover_list = [0 for x in range(len(code))]
old_cover_list = [0 for x in range(len(code))]
new_state = [[0]*len(code) for x in range(len(test))]
new_test = []
method = 'total'
if method == 'total':
	count_list = [[0]*2 for x in range(len(test))]
	#initialize
	for i in range(len(test)):
		count_list[i][0] = i
		count_list[i][1] = cover_count(state[i])
	sort_count = sorted(count_list, key=get_key, reverse=True)

	for i in range(len(test)):
		new_state[i] = state[sort_count[i][0]]
	for i in range(len(test)):
		new_test.append(test[sort_count[i][0]])

	new_order = []
	test_count = -1
	while test_count<len(test) and cover_count(cover_list) != sei:
		test_count = test_count+1
		old_cover_count = cover_count(cover_list)
		for j in range(len(code)):
			cover_list[j] = cover_list[j]+new_state[test_count][j]
		new_cover_count = cover_count(cover_list)
		if new_cover_count > old_cover_count:
			new_order.append(test_count)
	
	os.system('rm -rf '+file+'/total_branch.txt')
	for i in range(0, len(new_order)):
		with open(file + '/total_branch.txt', 'a+') as f3:
			f3.write(new_test[new_order[i]]+'\n')

sc = 0
cover_list = [0 for x in range(len(code))]
old_cover_list = [0 for x in range(len(code))]
new_state = [[0]*len(code) for x in range(len(test))]
new_test = []
method = 'add'
if method == 'add':
	next_test = 0
	new_order = []
	temp = [0 for x in range(len(code))]

	while cover_count(old_cover_list) != sei:
		#get a test
		sc = cover_count(old_cover_list)
		for i in range(len(test)):	
			#cover_list
			for j in range(len(code)):
				cover_list[j] = old_cover_list[j] + state[i][j]
			if i not in new_order and cover_count(cover_list) > sc: 
				sc = cover_count(cover_list)
				select = i
				for m in range(len(code)):
					temp[m] = cover_list[m]
		
		new_order.append(select)
		for n in range(len(code)):
			old_cover_list[n] = temp[n]
	
	os.system('rm -rf '+file+'/add_branch.txt')
	for i in range(0, len(new_order)):
		with open(file + '/add_branch.txt', 'a+') as f4:
			f4.write(test[new_order[i]]+'\n')
'''
