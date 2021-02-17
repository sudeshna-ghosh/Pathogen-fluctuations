# Pathogen-fluctuations
-----------------------

Pathogenic genera are quantified in copies per million of unique functional genes based on Illumina short-read metagenomic sequencing data, single or pair-ended. 
 

Bacterial pathogen list: 
-----------------------
Genera: Aeromonas, Campylobacter, Clostridioides, Citrobacter, Enterobacter, Enterococcus, Escherichia, Helicobacter, Klebsiella, Morganella, Providencia, Salmonella, Shigella, Vibrio, Acinetobacter, Burkholderia, Haemophilus, Legionella, Mycobacterium, Proteus, Pseudomonas, Serratia, Staphylococcus, Stenotrophomonas and Streptococcus spp. 

Pathogen groups within genera: Mycobacterium avium complex (NCBI Taxonomy ID 120793), Stenotrophomonas maltophilia group (NCBI Taxonomy ID 995085), Enterobacter cloacae complex (NCBI Taxonomy ID 354276), Acinetobacter caloaceticus/baumanii complex (NCBI Taxonomy ID 909768) and Burkholderia cepacia complex (NCBI Taxonomy ID 87882).

Protozoa list: 
--------------
Genera: Acanthamoeba, Naegleria, Giardia, Vermamoeba spp.


Method for version 1
--------------------
Step1: Generate HUMAnN2 output of UniRef90 based functional gene classification

Step2: Run pathogen quantification analysis on the HUMAnN2 output




Step1: Generate HUMAnN2 output of UniRef90 based functional gene classification
-------------------------------------------------------------------------------

(Note: It will be updated to use HUMAnN3)

Please consult https://huttenhower.sph.harvard.edu/humann2 for details. 

(i) Install HUMAnN2, MetaPhlAn2 (v 2.8), and KneadData. I installed HUMAnN2 and MetaPhlAn2 in an environment with Python 2.7

(optional-check requirement:

	conda config --add channels bioconda
	conda config --add channels conda-forge
) 

$ conda install -c bioconda humann2

$ conda install metaphlan2=2.8 

$ conda install -c bioconda kneaddata

(ii) Download necessary databases.

$ humann2_databases --download chocophlan full $DIR

$ humann2_databases --download uniref uniref90_diamond $DIR

$ humann2_databases --download utility_mapping full $DIR

    $DIR = directory name/location

(iii) Generating HUMAnN2 output

a) Concatenate forward and reverse reads

b) Run KneadData

$ kneaddata --input $INPUT --output $OUTPUT_DIR --trimmomatic $PATH

Requires Java Runtime Environment
(Optional for human microbiome:
$ kneaddata_database --download human bowtie2 $DIR
$ kneaddata --input $INPUT --reference-db $DATABASE --output $OUTPUT_DIR)

    $INPUT = concatenated fastq file (can be gzipped) or a SAM/BAM formatted file name/location
    $DATABASE = the index of the KneadData database name/location (exp. human reference database)
    $OUTPUT_DIR = the output directory name/location
    $PATH = Location where trimmomatic is saved within KeadData (may be required)

c) Run HUMAnN2 and process output:

$ humann2 -v --input $INPUT --threads 32 --output $OUTPUT_DIR
    
    $INPUT = trimmed.fastq file name/location 
	$OUTPUT_DIR = the output directory name/location. If you have multiple samples create an empty directory to store $OUTPUT_DIR from all samples

$ humann2_join_tables -s --input $INPUT_DIR --output $TABLE --file_name genefamilies
  
    $INPUT_DIR = Name/location of directory containing HUMAnN2 output directories from samples to be joined
    $TABLE = Table name/location of joined table with all samples

$ humann2_renorm_table --input $TABLE_IN --output $TABLE_OUT --units cpm --update-snames

    $TABLE_IN = Table name/location of joined table with all samples
    $TABLE_OUT = Table name/location of table with copies per million (cpm) normalization

$ humann2_rename_table --input $TABLE_IN --names $NAMES --output $TABLE_OUT

    $TABLE_IN = Table name/location of table with copies per million (cpm) normalization 
    $TABLE_OUT =  Table name/location of joined normalized table with enzyme description
    $NAMES = use ‘uniref90’

$ humann2_split_stratified_table --input $TABLE_IN --output $OUTPUT_DIR

    $TABLE_IN = Table name/location of joined normalized table with enzyme description
    $OUTPUT_DIR = Directory name/location containing stratified and unstratified tables
This will generate 2 .tsv files, stratified and unstratified. 

Step2: Run pathogen quantification analysis on the HUMAnN2 output
-----------------------------------------------------------------

Clone the git repository https://github.com/sudeshna-ghosh/Pathogen-fluctuations

python pathogens_new.py –db $DB  --o $OUTPUT_FILE $INPUT_FILE
 
    provide full path to directory with pathogens_new.py
    $DB = Name/location of pathogen database folder (posted on github)
    $INPUT_FILE = Name/location of the unstratified genefamilies table in cpm 
    $OUTPUT_FILE = Name/location of pathogen abundance table in cpm of unique functional genes


	
