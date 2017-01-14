import sys

fileNum = 28
prefix = ["SRR764"] * fileNum
num = range(782, 798) + range(802, 814)
fileName = []
for i in range(0, fileNum):
        fileName.append(prefix[i] + str(num[i]) + "/output/pileup")
        #fileName.append(prefix[i] + str(num[i]) + "/star_output/pileup_30")
for name in fileName:
	inFile = open(name,'r')
	
	f = open(name + ".count", 'w')
	f.write('chr\tbp\tA\tG\tC\tT\tdel\tins\tinserted\tambiguous\n')
	for line in inFile:
		data = line.strip().split('\t')
		bp = data[1]
		if(int(data[3]) <= 3):
			continue	
		bases = data[4].upper()
		ref = data[2].upper()
		
		types = {'A':0,'G':0,'C':0,'T':0,'-':0,'+':[],'X':[]}
		
		i = 0
		while i < len(bases):
			base = bases[i]
			if base == '^' or base == '$':
			        i += 1
			elif base == '-':
			        i += 1
			elif base == '*':
			        types['-'] += 1
			elif base == '+':
			        i += 1
			        addNum = int(bases[i])
			        addSeq = ''
			        for a in range(addNum):
			                i += 1
			                addSeq += bases[i]
			
			        types['+'].append(addSeq)
			elif base == '.' or base == ',':
			        types[ref] += 1
			else:
			        if types.has_key(base):
			                types[base] += 1
			        else:
			                types['X'].append(base)
			
			i += 1
		
		adds = '.'
		if len(types['+']) > 0:
			adds = ','.join(types['+'])
		
		amb = '.'
		if len(types['X']) > 0:
			amb = ','.join(types['X'])
		
		out = [bp,types['A'],types['G'],types['C'],types['T'],types['-'],len(types['+']),adds,amb]
		f.write(data[0] + '\t' + '\t'.join([str(x) for x in out]) + "\n")
