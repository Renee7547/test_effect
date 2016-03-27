#All programs are tested on the @well.cs.ucr.edu server
#HOW TO COMPILE AND RUN:
1	put the codes from main_code folder to benchmarks folder
2	./statement.py <filename> <methods>
--- <filename>:tcas, totinfo, etc.
	(Attention: the filename should NOT end with ‘/‘)
--- <methods>: random, total or additional
	(Attention: for result convenience, no matter what methods you choose, all the results for random, total and additional would be got)
3	Finally, we get the test suites in files random_statement.txt, total_statement.txt, and add_statement.txt within the <filename> folder

#HOW TO GET THE FAULT-EXPOSING CASES:
1	put faults_test.py in benchmarks folder
2	./faults_test.py <filename> <random_statement.txt>
	./faults_test.py <filename> <random_branch.txt>
	......
	./faults_test.py <filename> <total_combine.txt>
	......
