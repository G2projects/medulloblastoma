# Medulloblastoma project
Detection and characterization of backsplicing variants in Group 3 and Sonic Hedgehog (SHH) medulloblastoma patients.

## Cluster tree

```
/data/hpc-share/Fernando/medulloblastoma
|
> downloads              # EGA samples download directory
|  > credential.json
|  > EGAF0000xxxxxxx_download.sh
|
> CE2_refs               # Circ Explorer 2 references
|  > hg19_ens.txt
|  > hg19_kg.txt
|  > hg19_ref_all.txt
|  > hg19_ref.txt
|
> MB_group3         # medulloblastoma group 3 (moved to external SSD/HDD)
|  > FASTQ
|  > Alignments
|  > Counts
|
> MB_SHH            # medulloblastoma sonic hedgehog (moved to external SSD/HDD)
|  > FASTQ
|  > Alignments
|  > Counts
|
> HFB               # healthy fetal brain (moved to external SSD/HDD)
|  > FASTQ
|  > Alignments
|  > Counts
|
> HAB               # healthy adult brain (moved to external SSD/HDD)
|  > FASTQ
|  > Alignments
|  > Counts
|
> deprecated
```

## Supplementary files

The PBS script templates will require additional files, either provided with this repository or within the Bioinformatics Facility cluster.
They include:

- **credential.json** &nbsp;&nbsp; Credentials needed for downloading EGA datasets. Available at: /data/hpc-share/Fernando/medulloblastoma/downloads
- **ega.yml** &nbsp;&nbsp; Configuration file for the EGA conda environment (needed for EGA data downloading).
- **rnaseq.yml** &nbsp;&nbsp; Configuration file for the RNA-seq conda environment. This is needed for STAR read mapper and CIRCexplorer2 execution.
- **hg19_ref_all.txt** &nbsp;&nbsp; Transcripts reference file. This file contains transcripts from Ensembl, UCSC KnownGenes, and RefSeq databases.
- **GRCh37.p13.genome.fa** &nbsp;&nbsp; Reference genome (hg19) in fasta format. Available at: /data/hpc-share/genomeRef/GENCODEv19
- **gencode.v19.annotation.gtf** &nbsp;&nbsp; GENCODE hg19 transcripts. Available at: /data/hpc-share/genomeRef/GENCODEv19

## Backsplicing events calling

### EGA download script

Requirements: [conda](https://github.com/conda/conda), [PyEGA3](https://pypi.org/project/pyega3), [EGA](https://ega-archive.org) credentials

Supplementary resources: **ega** conda environment

```
#! /bin/bash

#PBS -o EGAF0000xxxxxxx.stdout
#PBS -e EGAF0000xxxxxxx.stderr
#PBS -l select=2:ncpus=10:mem=60g
#PBS -l place=scatter
#PBS -N EGAF0000xxxxxxx
#PBS -m ea
#PBS -q workq
#PBS -M fernando.palluzzi@policlinicogemelli.it

module load anaconda/3
conda init bash
source ~/.bashrc
conda activate /data/hpc-data/shared/condaEnv/ega
cd /data/hpc-share/Fernando/medulloblastoma/download_shh

pyega3 -cf credential.json fetch EGAF0000xxxxxxx
```

### Alignment script

Requirements: [conda](https://github.com/conda/conda), [STAR](https://github.com/alexdobin/STAR)

Supplementary resources: **rnaseq** conda environment, **star_align_chimeric.py** script

```
#! /bin/bash 

#PBS -o EGAF0000xxxxxxx_xx.stdout 
#PBS -e EGAF0000xxxxxxx_xx.stderr 
#PBS -l select=2:ncpus=16:mem=30g
#PBS -l place=scatter
#PBS -N EGAF0000xxxxxxx_xx
#PBS -m ea
#PBS -q workq
#PBS -M fernando.palluzzi@policlinicogemelli.it

module load anaconda/3
conda init bash 
source ~/.bashrc 
conda activate /data/hpc-data/shared/condaEnv/rnaseq
cd /data/hpc-share/medulloblastoma/EGAF0000xxxxxxx_xx/alignment

python3 python3 star_align_chimeric.py \
/data/hpc-share/Fernando/medulloblastoma/EGAF0000xxxxxxx_xx/samplesheet.csv \
/data/hpc-share/Fernando/medulloblastoma/EGAF0000xxxxxxx_xx/alignment
```

#### Samplesheet format (.csv)
```
group,replicate,fastq_1,fastq_2,strandedness
MB,1,XXXXXXXXX_6_GTGGCC_1.fastq.gz,XXXXXXXXX_6_GTGGCC_2.fastq.gz,forward
control,1,XXXXXXXXX_7_AGGTTT_1.fastq.gz,XXXXXXXXX_7_AGGTTT_2.fastq.gz,forward
...
```

#### Output files

- Alignment file (***.bam**)
- Temporary alignment directory (this can be removed once the alignment is completed)
- Gene counts (***ReadsPerGene.out.tab**)
- Splicing junctions table (***SJ.out.tab**)
- Chimeric junctions table (***Chimeric.out.junction**)
- Execution summary (***Log.final.out**)
- Progress bar log (***Log.progress.out**)
- Execution log (***Log.out**)

### Backsplicing events calling

#### CIRCexplorer2

Requirements: [conda](https://github.com/conda/conda), [CIRCexplorer2](https://circexplorer2.readthedocs.io/en/latest)

Supplementary resources: **rnaseq** conda environment, transcripts file (**hg19_ref_all.txt**)

```
#! /bin/bash 

#PBS -o EGAF0000xxxxxxx_CE2.stdout 
#PBS -e EGAF0000xxxxxxx_CE2.stderr 
#PBS -l select=2:ncpus=16:mem=30g
#PBS -l place=scatter
#PBS -N EGAF0000xxxxxxx_CE2
#PBS -m ea
#PBS -q workq
#PBS -M fernando.palluzzi@policlinicogemelli.it

module load anaconda/3
conda init bash 
source ~/.bashrc 
conda activate /data/hpc-data/shared/condaEnv/rnaseq
cd /data/hpc-share/Fernando/medulloblastoma/EGAF0000xxxxxxx_xx

# This will create a back_spliced_junction.bed file
CIRCexplorer2 parse -t STAR EGAF0000xxxxxxxChimeric.out.junction > EGAF0000xxxxxxxCIRCexplorer2_parse.log

CIRCexplorer2 annotate \
-r /data/hpc-share/Fernando/medulloblastoma/CE2_refs/hg19_ref_all.txt \
-g /data/hpc-share/genomeRef/GENCODEv19/GRCh37.p13.genome.fa \
-b /data/hpc-share/Fernando/medulloblastoma/EGAF0000xxxxxxx_xx/back_spliced_junction.bed \
-o EGAF0000xxxxxxx_circularRNA.txt
```

#### CIRI

Requirements: [CIRI](https://ciri-cookbook.readthedocs.io/en/latest/CIRI2.html)

Supplementary resources: indexed hg19 genome (**GRCh37.p13.genome.fa**), transcripts file (**gencode.v19.annotation.gtf**)

```
#! /bin/bash

#PBS -o /data/hpc-share/medulloblastoma/cirifullXXXX.stdout
#PBS -e /data/hpc-share/medulloblastoma/cirifullXXXX.stderr
#PBS -l select=2:ncpus=16:mem=30g
#PBS -l place=scatter
#PBS -N ciriXXXX
#PBS -m ea
#PBS -q workq
#PBS -M fernando.palluzzi@policlinicogemelli.it

module load ciri/2.1.1

cd /data/hpc-share/Fernando/medulloblastoma

# The reference genome (-r) must be indexed!

java -jar /apps/ciri/2.1.1/bin/CIRI_Full_v2.1.1.jar \
-1 fastq/EGAF0000xxxxxxx/XXXXXXXXX_5_CATTTT_1.fastq.gz \
-2 fastq/EGAF0000xxxxxxx/XXXXXXXXX_5_CATTTT_2.fastq.gz \
-r /data/hpc-share/genomeRef/GENCODEv19/GRCh37.p13.genome.fa \
-a /data/hpc-share/genomeRef/GENCODEv19/gencode.v19.annotation.gtf \
-t 16 \
-d /data/hpc-share/Fernando/medulloblastoma/EGAF0000xxxxxxx_xx \
-o EGAF0000xxxxxxx_xx
```

## Splicing junction quantification

Requirements: [sj2psi converter](https://github.com/olgabot/sj2psi)

Supplementary resources: **starsj2psi.py**, **psiparse.py**, **extractIntronicSJs.py**

### Convert splicing junctions to percent spliced-in (PSI)

This utility quantifies splicing junction usage and outputs other intron and junction information.

```
usage: starsj2psi.py [-h] [-u UNIQUE] [-m MULTIMAP] [-q] sjout

positional arguments:
  sjout                 STAR alignment SJ.out.tab file.

optional arguments:
  
  -h, --help            show this help message and exit
  
  -u UNIQUE, --unique UNIQUE
                        Minimum number of unique reads per junction. (default: 5)
  
  -m MULTIMAP, --multimap MULTIMAP
                        Minimum number of multimapping reads per junction. (default: 10)
  
  -q, --quiet           Suppress verbosity. (default: False)
```

### PSI parsing

Parse the output of starsj2psi.py, making it human-friendly.

```
usage: psiparse.py [-h] [-o ORGANISM] [-c CHROM] [-n NA] [-s SEPARATOR] [-H] [-r] [-q] psi

positional arguments:
  
  psi                   PSI BED file generated by starsj2psi

optional arguments:
  
  -h, --help            show this help message and exit
  
  -o ORGANISM, --organism ORGANISM
                        One among human and mouse. (default: human)
  
  -c CHROM, --chrom CHROM
                        Chromosome field. (default: 1)
  
  -n NA, --na NA        Value to be substituted to NAs.
                        This argument may take either numbers or strings. (default: 0)
  
  -s SEPARATOR, --separator SEPARATOR
                        Field separator. (default: "\t")
  
  -H, --noheader        Enable if the input file has no header. (default: False)
  
  -r, --relaxed         relaxed filter on reads count. (default: False)
  
  -q, --quiet           Suppress verbosity. (default: False)
```

### Intronic junction extraction

Extract intronic junctions fom an intron BED file.

```
usage: extractIntronicSJs.py [-h] [-w WIDTH] [-j JUNCTIONSIDE] [-p PHENOTYPE] [-H] [-q] introns

positional arguments:
  
  introns               Introns BED file. The first 6 fields must be: chromosome, start, end, name, score, strand.

optional arguments:
  
  -h, --help            show this help message and exit
  
  -w WIDTH, --width WIDTH
                        Width of the output intronic junction region. (default: 1)
  
  -j JUNCTIONSIDE, --junctionSide JUNCTIONSIDE
                        Position of the field indicating in which side ("L" or "R") the intron is.
                        Set to -1 (default) to skip.
  
  -p PHENOTYPE, --phenotype PHENOTYPE
                        Phenotype field. Set to -1 (default) to skip.
  
  -H, --noheader        Enable if the input file has no header.
  
  -q, --quiet           Suppress verbosity.
```
