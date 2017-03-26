from operator import itemgetter
import collections
import itertools
import math
import numpy as np
import sys

def const_val(value):
	#return itertools.repeat(value).next
	return lambda: value

def prepare_data(source,target):
	es = []
	fs = []
	with open(source,'r') as e:
		for line in e:
			es.append(line.strip())

	with open(target,'r') as f:
		for line in f:
			fs.append(line.strip())

	assert len(es) == len(fs)

	return[(src.split(' '),tgt.split(' ')) for (src,tgt) in zip(es,fs)]

def get_alignment(german, english, t):
	max_align = []
	g_size = len(german)
	e_size = len(english)
	for (j, g) in enumerate(german):
		#current_max = (0, -1)
		#for (i, f) in enumerate(fs, 1):
		#	value = t[(e, f)] 
		#	if current_max[1] < value:
		#		current_max = (i, value)
		#max_align[j] = current_max[0]
		value = []
		for (i, e) in enumerate(english):
			value.append((1.0/(1.0 + abs(float(j)/len(german) - float(i)/len(english)))) * t[(e,g)])
		aligned_word = np.argmax(np.array(value).astype(np.float32))
		max_align.append((aligned_word,j))
	return max_align

def train(corpus, num_epochs):
	f_words = set()
	for (german, english) in corpus:
		for ger in german:
			f_words.add(ger)
	epsilon = float(1)/len(f_words)
	t = collections.defaultdict(const_val(epsilon))

	for i in range(0,num_epochs):
		count_ef = collections.defaultdict(float)
		total_f = collections.defaultdict(float)
		s_total = collections.defaultdict(float)
		for (german, english) in corpus:
			for e in english:
				s_total[e] = 0.0
				for g in german:
					s_total[e] += t[(e,g)]

			for e in english:
				for g in german:
					#print t[(e,g)],s_total[e] 
					count_ef[(e,g)] += float(t[(e,g)])/s_total[e]
					total_f[g] += float(t[(e,g)])/s_total[e]

		for (e,g) in count_ef.keys():
			t[(e,g)] = float(count_ef[(e,g)])/total_f[g]

	return t

def prepare_alignments(corpus,t,out_dir):
	fh = open(out_dir,'w')
	for (german,english) in corpus:
		arr = get_alignment(german,english,t)
		for (e,g) in arr:
			fh.write("%d-%d "%(e,g))
		fh.write("\n")

if __name__ == '__main__':

	german_file = sys.argv[1]
	english_file = sys.argv[2]
	out_file = sys.argv[3]
	#base_path = '/home/varsha/Documents/MT/Assignement1/en-de/'
	#corpus = prepare_data(base_path+'valid.en-de.low.de', base_path+'valid.en-de.low.en')
	corpus = prepare_data(german_file,english_file)
	t = train(corpus, 15)
	#for (e, f), val in t.items():
	#	print("{} {}\t{}".format(e, f, val))
	alignments = prepare_alignments(corpus,t,out_file)
