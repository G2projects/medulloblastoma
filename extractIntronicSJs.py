#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import argparse


parser = argparse.ArgumentParser()

parser.add_argument("introns",
                    help = "Introns BED file. The first 6 fields" +\
                           "must be: chromosome, start, end, name, " +\
                           "score, strand.",
                    type = str)

parser.add_argument("-w", "--width",
                    help = "Width of the output region.",
                    type = int,
                    default = 1)

parser.add_argument("-j", "--junctionSide",
                    help = "Position of the field indicating in which" +\
                           "side (\"L\" or \"R\") the intron is.",
                    type = int,
                    default = -1)

parser.add_argument("-p", "--phenotype",
                    help = "Phenotype field.",
                    type = int,
                    default = -1)

parser.add_argument("-H", "--noheader",
                    help = "Enable if the input file has no header.",
                    action = "store_true")

parser.add_argument("-q", "--quiet",
                    help = "Suppress verbosity.",
                    action = "store_true")

args = parser.parse_args()


def listAllFiles(directory):
	f = []
	for root, sub, files in os.walk(directory):
		for x in files:
			f += [os.path.join(root, x)]
	return f

def extractJunctions(x, w = 1, j = -1, pheno = -1, header = True):
	out = x.split('.')[0] + '_junctions.bed'
	wrt = open(out, "w")
	
	with open(x, "r") as lines:
		for line in lines:
			if header:
				wrt.write("chrom\tjunctionStart\tjunctionEnd\tname\t" +\
				          "intronLengtht\tstrand\tphenotype\n")
				header = False
			else:
				line = line.strip().split()
				side = line[j] if j > -1 else 'L'
				strand = line[5] if line[5] in ('+', '-') else '.'
				#side = side + strand
				if side == 'L':
					start = str(int(line[2]) - w)
					end = line[2]
				elif side == 'R':
					start = line[1]
					end = str(int(line[1]) + w)
				line = [line[0], start, end, line[3], line[4],
				        strand, line[pheno]]
				wrt.write('\t'.join(line) + '\n')
	wrt.close()
	return out


if not args.quiet:
	print("# File parsing started. Please, wait.")

head = not args.noheader

if os.path.isfile(args.introns):
	out = extractJunctions(args.introns, w = args.width,
	                       j = args.junctionSide-1, pheno = args.phenotype-1,
	                       header = head)
	if not args.quiet:
		print("[!] 1 file created: .../" + os.path.basename(out))

elif os.path.isdir(args.introns):
	for x in listAllFiles(args.introns):
		out = extractJunctions(x, w = args.width, j = args.junctionSide-1,
		                       pheno = args.phenotype-1,
		                       header = head)
		if not args.quiet:
			print("[!] 1 file created: .../" + os.path.basename(out))

else:
	raise OSError(args.introns + ': file or directory not found')

if not args.quiet:
	print("# Done.")

