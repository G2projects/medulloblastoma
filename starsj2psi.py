#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import pandas as pd
import sj2psi

try:
    # For Python 3
    from io import StringIO
except ImportError:
    # For Python 2
    from StringIO import StringIO

import argparse


parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("sjout",
                    help = "STAR alignment SJ.out.tab file.",
                    type = str)

parser.add_argument("-u", "--unique",
                    help = "Minimum number of unique reads per junction.",
                    type = int,
                    default = 5)

parser.add_argument("-m", "--multimap",
                    help = "Minimum number of multimapping reads per junction.",
                    type = int,
                    default = 10)

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

def writePsi(x, u = 5, m = 10):
	out = x.split('.')[0] + '_psi.bed'
	sj = sj2psi.read_sj_out_tab(x)
	psi = sj2psi.get_psis(sj, min_unique = u, min_multimap = m)
	psi.to_csv(out, sep = '\t', index = False)
	return out


if not args.quiet:
	print("# PSI computation started. Please, wait.")

if os.path.isfile(args.sjout):
	out = writePsi(args.sjout, u = args.unique, m = args.multimap)
	if not args.quiet:
		print("[!] 1 file created: .../" + os.path.basename(out))

elif os.path.isdir(args.sjout):
	for x in listAllFiles(args.sjout):
		out = writePsi(x, u = args.unique, m = args.multimap)
		if not args.quiet:
			print("[!] 1 file created: .../" + os.path.basename(out))
else:
	raise OSError(args.sjout + ': file or directory not found')

if not args.quiet:
	print("# Done.")
