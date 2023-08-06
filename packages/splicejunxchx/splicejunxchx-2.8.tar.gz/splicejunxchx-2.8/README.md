
# splicejunxchx

Splicejunxchx is a Python pipeline that takes splice junctions outputed by STAR (SJ.out.tab) and a GTF file to characterize the 5' and 3' splice
sites of a splice junction.

The pipeline includes the following capabilities:
- Determine if 5'/3' end is in a gene, transcript, exon, intron, 5'UTR, CDS, 3'UTR, start codon, or stop codon
- Determine if 5'/3' splice site (ss) is in a constitutive exon or intron
- Determine if 5'/3' end is annotated based on information in the GTF file
- Find closest ss upstream and downstream from the 5' and 3' ss  of the analyzed junction

Additional capabilities with required dependencies:
- The 51 bases centered around each splice site (needs bedtools)
- The 2 bases of the 5'/3' ss (bedtools)
- maxEnt score (need to download maxEnt perl files)
- A phyloP score over an average N nulceotides around each splice site(bigWigtoBedGraph)


## Installation

First, you must have python3.6>=, pandas0.23.4>=, and gtf2csv (see below)

```bash
pip install git+https://github.com/zyxue/gtf2csv.git#egg=gtf2csv
```

Look at the following websites to get: bedtools, bigWigToBedGraph, and maxEnt sccores:
- [bedtools](https://bedtools.readthedocs.io/en/latest/content/installation.html)
- [bigWigToBedGraph](http://hgdownload.cse.ucsc.edu/admin/exe/)
- For [maxEnt](http://hollywood.mit.edu/burgelab/maxent/download/), make sure you download fordownload.tar.gz and put score5.pl, score3.pl, me2x5, and the directory splicemodels in the root where you plan to run splicejunxchx

Now, install splicejunxchx using:

```bash
pip install splicejunxchx
```

## Usage

One suggestion is to ensure there is a 'data' directory in whichever root directory you plan to utilize this code. The data directory will store some temp files that include: Two CSV file of all the splice junctions and constitutive exons based on the GTF File 

The following is the full usage possibilities that can be added with splicejunxchx

```bash
splicejunxchx -h [-seqs SEQUENCE_FILE] [-supp SUPPORT_FILES SUPPORT_FILES] [-phyloP PHYLOPSCORES PHYLOPSCORES] [-maxEnt] inputs inputs output_file
```

There are several ways to utilize this pipeline. First, the basic way is to input the gtf.gz file and the SJ.out.tab file and name the output file. This will output the splice junctions with basic information regarding where each splice site lies according to the GTF and where the other closest splice sites are located. To run this command:

```bash
splicejunxchx raw_data/Homo_sapiens.GRCh38.95.gtf.gz raw_data/ERR152SJ.out.tab output/final_splice_junc.csv
```

If you are interested in adding sequence information, you must have bedtools installed (with getfasta function) and then add the .fa file after -seq:

```bash
splicejunxchx raw_data/Homo_sapiens.GRCh38.95.gtf.gz raw_data/ERR152SJ.out.tab output/final_splice_junc.csv -seq data/Homo_sapiens.GRCh38.95.fa 
```

In some cases, to increase speed and time, support files for reported splice junctions and constitutive exons can be provided to splicejunxchx if available.
- Reported splice junctions file must be csv with the following columns: [seqname,start,end,strand]
- Reported splice junctions file must be csv with the following columns: [seqname,start,end,strand,exon_id,gene_id]
- The pipeline generates these aforementioned files on the first run if you want to utilize the same GTF file but have differing splice junctions on the second run

```bash
splicejunxchx raw_data/Homo_sapiens.GRCh38.95.gtf.gz raw_data/ERR152SJ.out.tab output/final_splice_junc.csv -supp data/all_splice_junctions.csv data/cons_exons.csv
```

If you want to include maxEnt score include score5.pl, score3.pl, me2x5, and the directory splicemodels in the root where you plan to run splicejunxchx. Also add the -maxEnt flag

Lastly, to incorporate phyloP score, the input for this tag requires the phyloPscore file as a bigWig (.bw) and the second input as the number of nucleotides of individual phyloP scores requested around each splice site. This number cannot be more than 200 and must be an even number. 

```bash
splicejunxchx raw/Homo_sapiens.GRCh38.95.gtf.gz raw_data/ERR152SJ.out.tab output/final_splice_junc.csv -phyloP data/hg38.phyloP.bw 20
```


## Notes

### General notes about needed files and output structure

Make sure that the GTF File provided does not list out intron locations. This pipeline assumes that the only features present in the GTF File are: gene, transcript, exon, five_prime_utr, CDS, three_prime_utr, start codon, stop codon, and Selenocysteine

For splice junctions that have a unidentified strand (strand = 0), the pipeline create two copies of that splice junction and changes the strand=1 for one junction and the other to strand=2
- EX: If JNC92 has a strand of 0
    - The pipeline creates two junctions called JNC92.1 (strand =1) and JNC92.2 (strand=2)
- To find the splice junctions that are strand=0, search for the junctions that have a 'unidentified_strand' columns set to the value of 1 

### Columns in Output File 

The following columns are provided with more detail:

- Motif:[0: non-canonical; 1: GT/AG, 2: CT/AC, 3: GC/AG, 4: CT/GC, 5:AT/AC, 6: GT/AT]
- STAR_annotation: Both 5' and 3' splice site are annotated as one splice junction according to STAR
- Unidentified_strand: splice junction originally was undefined (Strand = 0), but this junction has been developed with assumption of being on positive or negative strand (see 'strand' column for assumption)
- 5'_in_constitutiveexon: Name of gene followed by the coordinates, else NA
- 5'_in_constitutiveintron: Name of gene followed by the coordinates, else NA
- 5'_in_CDS: If the 5' end is in a coding sequence region
- 5'phyloPscore: Average score over N nucleotides of each splice site
- 5'phylopList: List of phyloP values starting from lowest coordinate to highest coordinate
- 5'bases_maxEnt and 3'bases_maxEnt: the sequence needed to run a maxEnt score
- Similar logic is present in 3' regions 


## Acknowledgments
- Athma Pai and Eraj Khokhar for guidance and support
- Zyxue for gtf2csv: https://github.com/zyxue/gtf2csv
- Yeo G and Burge C.B., Maximum Entropy Modeling of Short Sequence Motifs with Applications to RNA Splicing Signals, RECOMB 2003 (Journal Comp. Bio in press)
