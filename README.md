# Medulloblastoma
Characterization of backsplicing variants in Group 3 and Sonic Hedgehog (SHH) medulloblastoma patients.

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
> alignments
|  > 
|  > 
|  > 
|  > 
|  > 
```

## PBS scheduler

### EGA download script

Filename format: **EGAF0000xxxxxxx_download.sh**

Requirements: [conda](https://github.com/conda/conda), [PyEGA3](https://pypi.org/project/pyega3), [EGA](https://ega-archive.org) credentials

Supplementary files: **ega** conda environment

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

pyega3 -cf /data/hpc-share/Fernando/medulloblastoma/download_shh/credential.json fetch EGAF0000xxxxxxx
```

### Alignment script

Filename format: **align_star.sh**

Requirements: [conda](https://github.com/conda/conda), [STAR](https://github.com/alexdobin/STAR)

Supplementary files: **rnaseq** conda environment

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
- Temporary alignment directory (can be removed after the alignment)
- Gene counts (***ReadsPerGene.out.tab**)
- Splicing junctions table (***SJ.out.tab**)
- Chimeric junctions table (***Chimeric.out.junction**)
- Execution summary (***Log.final.out**)
- Progress bar log (***Log.progress.out**)
- Execution log (***Log.out**)


