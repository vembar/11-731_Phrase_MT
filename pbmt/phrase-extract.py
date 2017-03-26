import math
import sys
import collections
def read_input(filename):
	alignments = []
	with open(filename,'r') as f:
		for line in f:
			tokens = line.strip()
			#sent = []
			#for a in tokens:
		#		if a != None:
		#			(e,f) = a.split('-')
		#			sent.append((int(e)+1,int(f)+1))
			alignments.append(tokens)
	return alignments

def get_align_dict(alignment):
	e_align = collections.defaultdict(list)
	g_align = collections.defaultdict(list)
	for pair in alignment.split(' '):
		tok = pair.split('-')
		e_align[int(tok[0])].append(int(tok[1]))
		g_align[int(tok[1])].append(int(tok[0]))
	return e_align, g_align

def check_QC(TP, g_align):
	TP.sort()
	begin = TP[0]
	for i in range(1, len(TP)):
		next = TP[i]
		if(next != begin+1):
			if(len(g_align[next]) != 0):
				return False
		begin = begin+1
	return True

def extract_phrase(german, english, alignment):
	e_align,g_align = get_align_dict(alignment)
	phrases = set()
	eng_size = len(english)
	germ_size = len(german)
	for e_st in range(0,eng_size):
		for e_ed in range(e_st, eng_size):
			if e_ed - e_st > 4:
				continue
			TP = []
			for i in range(e_st,e_ed+1):
				TP.extend(e_align[i])
				#print e_align[i]
			TP = list(set(TP))
			#	print TP
			if len(TP) == 0:
				continue
			#print "here"
			isConsec = check_QC(TP, g_align)
			
			if isConsec == True:
				#print "Found consec"	
				g_st, g_ed = min(TP), max(TP)
				if g_ed - g_st > 4:
					continue

				SP = []
				for i in range(g_st,g_ed+1):
					SP.extend(g_align[i])
				SP = list(set(SP))
				SP.sort()
				if len(SP) != 0 and min(SP) >= e_st and max(SP) <= e_ed:
					eng_phrase = " ".join(english[e_st:(e_ed+1)])
					germ_phrase = " ".join(german[g_st:(g_ed+1)])
					#print eng_phrase, germ_phrase
					phrases.add((eng_phrase,germ_phrase))
					while(g_st > 0 and len(g_align[g_st]) == 0):
						g_temp_e = g_ed
						if g_temp_e-g_st > 4:
							continue
						while(g_temp_e < germ_size and len(g_align[g_temp_e])==0):
							germ_phrase = " ".join(german[g_st:(g_temp_e+1)])
							phrases.add((eng_phrase,germ_phrase))
							g_temp_e += 1
						g_st = g_st - 1

	return list(phrases)

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

if __name__ == '__main__':
	source_file = sys.argv[1]
	target_file = sys.argv[2]
	alignments = read_input(sys.argv[3])
	out_file = sys.argv[4]
	out = open(out_file,'w')
	#alignments = read_input('alignments.txt')
	#base_path = '/home/varsha/Documents/MT/Assignement1/en-de/'
	corpus = prepare_data(source_file, target_file)
	count_fe = {}
	count_e = {}
	phrases = []
	for ((german, english), align) in zip(corpus,alignments):
		#print es, fs, align
		#temp, count_e, count_fe = phrase_extract(es, fs, align, count_e, count_fe)
		ext = extract_phrase(german, english, align)
		#print ext
		#	ext[(e,f)] = 1
		for (eng,germ) in ext:
			phrases.append((germ,eng))
			#germ = ' '.join(e)
			#eng = ' '.join(f)
			#print germ
			#print eng
			if eng in count_e:
				count_e[eng] += 1
			else:
				count_e[eng] = 1
			if (eng,germ) in count_fe:
				count_fe[(eng,germ)] += 1
			else:
				count_fe[(eng,germ)] = 1
			#print("{}{}{}".format(germ, '---->', eng))
	for (germ,eng) in phrases:
		#print key
		score = math.log(float(count_fe[(eng,germ)])/count_e[eng])
		if score != 0.0:
			score = -1.0 * score 
		out.write("{}{}{}{}{}{}".format(germ, '\t', eng,'\t', score,'\n'))
	out.close()