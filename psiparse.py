#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import argparse


parser = argparse.ArgumentParser()

parser.add_argument("psi",
                    help = "PSI BED file generated by starsj2psi",
                    type = str)

parser.add_argument("-o", "--organism",
                    help = "One among human and mouse.",
                    type = str,
                    default = "human")

parser.add_argument("-c", "--chrom",
                    help = "Chromosome field.",
                    type = int,
                    default = 1)

parser.add_argument("-n", "--na",
                    help = "Value to be substituted to NAs.\n" +\
                           "This argument may take either numbers or strings.",
                    default = 0)

parser.add_argument("-s", "--separator",
                    help = "Field separator.",
                    type = str,
                    default = "\t")

parser.add_argument("-H", "--noheader",
                    help = "Enable if the input file has no header.",
                    action = "store_true")

parser.add_argument("-r", "--relaxed",
                    help = "relaxed filter on reads count.",
                    action = "store_true")

parser.add_argument("-q", "--quiet",
                    help = "Suppress verbosity.",
                    action = "store_true")

args = parser.parse_args()

if args.organism == "human":
	chromset = ['chr1', 'chr2', 'chr3', 'chr4', 'chr5', 'chr6', 'chr7',
	            'chr8', 'chr9', 'chr10', 'chr11', 'chr12', 'chr13',
	            'chr14', 'chr15', 'chr16', 'chr17', 'chr18', 'chr19',
	            'chr20', 'chr21', 'chr22', 'chrX', 'chrY', 'chrM']
elif args.organism == "mouse":
	chromset = ['chr1', 'chr2', 'chr3', 'chr4', 'chr5', 'chr6', 'chr7',
	            'chr8', 'chr9', 'chr10', 'chr11', 'chr12', 'chr13',
	            'chr14', 'chr15', 'chr16', 'chr17', 'chr18', 'chr19',
	            'chrX', 'chrY', 'chrM']
else:
	raise ValueError(args.psi + ': invalid organism choice')


def listAllFiles(directory):
	f = []
	for root, sub, files in os.walk(directory):
		for x in files:
			f += [os.path.join(root, x)]
	return f

def isint(x):
	try:
		a = float(x)
		b = int(a)
	except ValueError:
		return False
	else:
		return a == b

def psiParser(x, c = 0, na = 0, sep = '\t', header = True):
	out = x.split('.')[0] + '_clean.bed'
	w = open(out, "w")
	with open(x, "r") as lines:
		for line in lines:
			if header:
				#print(line)
				w.write("chrom\tintronStart\tintronEnd\tname\t" +\
				        "readsCount\tstrand\tsjMotif\t" +\
				        "ujr_raw\tmjr_raw\tujr\tmjr\tpsi5\tpsi3\n")
				header = False
			else:
				line = line.split(sep)
				if line[0] in chromset:
					#print(line)
					#print(len(line))
					#exit()
					if args.relaxed:
						#print(line[10], line[11])
						m = 0 if line[10] == '' else float(line[10])
						u = 0 if line[11] == '' else float(line[11])
						n = str(u + m)
					else:
						n = line[12]
					line = line[0:3] + [line[9]] + [n] + line[3:5] +\
					       line[6:8] + [line[11]] + [line[10]] +\
					       [line[14]] + [line[16].strip('\n')]
					#print(line)
					#print(len(line))
					#exit()
					line = [na if z in ('', '\n') else z for z in line]
					#print(line)
					#print(len(line))
					#exit()
					w.write('\t'.join(line) + '\n')
	w.close()
	return out


if not args.quiet:
	print("# PSI parsing started. Please, wait.")

c = args.chrom - 1
head = not args.noheader

try:
	if isint(na):
		na = str(int(args.na))
	else:
		na = str(float(args.na))
except:
	na = str(args.na)

if os.path.isfile(args.psi):
	out = psiParser(args.psi, c, na, args.separator, head)
	if not args.quiet:
		print("[!] 1 file created: .../" + os.path.basename(out))

elif os.path.isdir(args.psi):
	for x in listAllFiles(args.psi):
		out = psiParser(x, c, na, args.separator, head)
		if not args.quiet:
			print("[!] 1 file created: .../" + os.path.basename(out))

else:
	raise OSError(args.psi + ': file or directory not found')

if not args.quiet:
	print("# Done.")

