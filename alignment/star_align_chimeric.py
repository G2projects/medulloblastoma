
############################################
# NAME: star_align_chimeric.py
# AUTHOR: Luciano Giaco', Fernando Palluzzi
# Date: 16/03/2021
version = "0.1"
# ==========================================


import csv
import os
import sys
import subprocess

STAR_HG19 = '/data/hpc-data/shared/genomeRef/human/GRCh38/STAR/genecode'

def open_read_csv(csvfile, WD): 
	
    with open(csvfile, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            #print(', '.join(row))
            fastq1 = row[2]
            fastq2 = row[3]

            if os.path.isfile(fastq1) and os.path.isfile(fastq2):
                wd, fl = os.path.split(fastq1)
                roo, prefix = os.path.split(wd)
                currentDir = os.path.join(WD, prefix)
                # print(fastq1)
                # print(prefix)
                # print(currentDir)
                os.mkdir(currentDir)
                os.chdir(currentDir)
                str_to_run = ('STAR \
--readFilesIn '+fastq1+' '+fastq2+' \
--runThreadN 16 \
--genomeDir '+STAR_HG19+' \
--readFilesCommand zcat \
--outSAMtype BAM SortedByCoordinate \
--quantMode GeneCounts \
--chimSegmentMin 10 \
--outFileNamePrefix '+prefix)

                arr_to_run = str_to_run.split()
            
                print('[INFO] PROCESSING: '+str_to_run+'\n')
                subprocess.run(arr_to_run)
                # os.system(str_to_run)


def main(WD, csvfile):
    os.chdir(WD)
    print('[INFO] Working dir: '+ WD)
    open_read_csv(csvfile, WD)


if __name__ == '__main__':
    csvfile = sys.argv[1]
    WD = sys.argv[2]
    main(WD, csvfile)

