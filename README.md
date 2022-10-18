# Medulloblastoma
Characterization of backsplicing variants in Group 3 and Sonic Hedgehog (SHH) medulloblastoma patients.

## Hi-performance cluster tree

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

## PBS scheduler scripts

### EGA download script

Requirements: [conda](https://github.com/conda/conda), [PyEGA3](https://pypi.org/project/pyega3/), [EGA](https://ega-archive.org/) credentials

Filename format: **EGAF0000xxxxxxx_download.sh**

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
