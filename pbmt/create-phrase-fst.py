import sys
from collections import defaultdict

def write_fst(infilename, outfilename):
	out = open(outfilename,'w')
	#germ_state = {}
	#eng_state = {}
	curr_state = 0
	prev_state = 0
	states = {0:defaultdict(lambda: len(states))}
	visited = set()
	test_state = []

	with open(infilename) as f:
		for line in f:
			
			parts = line.strip().split('\t')
			source = parts[0].split(' ')
			target = parts[1].split(' ')
			score = parts[2]
			for ele in source:
				curr_state = states[prev_state][ele]
				if curr_state not in states:
					states[curr_state] = defaultdict(lambda: len(states))
					out.write(str(prev_state) + " " + str(curr_state) + " "+ ele + " "  + "<eps>" + "\n")	
				prev_state = curr_state

			for ele in target:
				#if ele not in eng_state:
				#	eng_state[ele] = state_num + 1
				#	state_num  += 1
				#trans_state = eng_state[ele]
				curr_state = states[prev_state][ele]
				if curr_state not in states:
					states[curr_state] = defaultdict(lambda: len(states))
					out.write(str(prev_state) + " " + str(curr_state) + " " + "<eps>" + " " + ele + "\n")
				prev_state = curr_state 
			out.write(str(prev_state) + " " + str(0) + " " + "<eps>" + " " + "<eps>" + " "+ score +"\n")
			prev_state = 0
	out.write(str(0) + " " + str(0) + " " + "<unk>" + " " + "<unk>" + "\n")	
	out.write(str(0) + " " + str(0) + " " + "</s>" + " " + "</s>" + "\n")
	out.write(str(0))
	out.close()

if __name__ == '__main__':
	inputfilename = sys.argv[1]
	outputfilename = sys.argv[2]
	write_fst(inputfilename,outputfilename)
