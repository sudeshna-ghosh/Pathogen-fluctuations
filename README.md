# Pathogen-fluctuations
-----------------------

The goal of this analysis is to estimate changes in relative abundance of pathogens across multiple samples. This method calculates differences in pathogen relative abundances at the genus level. Pathogen relative abundances are measured in copies per million of functional genes (options: all/unique to genus/unique to each species within a genus) from Illumina short-read metagenomic sequencing data, single or pair-ended. Functional gene are annotation against the UniRef90 database using Diamond [1] impremented through the HUMAnN2/MUMAnN3 pipeline [2]. 
 

Bacterial pathogen list: 
-----------------------
Genera: Aeromonas, Campylobacter, Clostridioides, Citrobacter, Enterobacter, Enterococcus, Escherichia, Helicobacter, Klebsiella, Leptospira, Listeria, Morganella, Providencia, Salmonella, Shigella, Vibrio, Acinetobacter, Burkholderia, Chryseobacterium, Elizabethkingia, Haemophilus, Legionella, Mycobacterium, Mycobacteroides, Mycolicibacterium, Mycolicibacter, Mycolicibacillus, Proteus, Pseudomonas, Segniliparus, Serratia, Staphylococcus, Stenotrophomonas and Streptococcus spp. 

Pathogen groups within genera (included in functional genes databases with all/unique to each species within a genes): Mycobacterium avium complex (NCBI Taxonomy ID 120793), Stenotrophomonas maltophilia group (NCBI Taxonomy ID 995085), Enterobacter cloacae complex (NCBI Taxonomy ID 354276), Acinetobacter caloaceticus/baumanii complex (NCBI Taxonomy ID 909768) and Burkholderia cepacia complex (NCBI Taxonomy ID 87882).

Protozoa list: 
--------------
Genera: Acanthamoeba, Cryptosporidium, Naegleria, Giardia, Vermamoeba spp.

Note: There are minor differences between pathogen databases wrt to the list of pathogens included. Check the running log for genera included in each database. 

Databases
---------
	All : all functional genes belong to a genus, including genes shared with other genera. This lowers the detection limit, however it can pick up related genera.
	Unique to genus: all functional genes belonging to a genus, excluding genes shared with other genera. 
	Unique to species: functional genes unique to each species belong to a genus. most conservative. While this database may be used to estimate relative abundances at the species level, the method has not been tested for species abundance estimation.

Test all three databases and use one that best suits goals of the analysis. 



Method for version 2
--------------------
(recommended)

Step1: Generate HUMAnN (version 3) output of UniRef90 based functional gene classification

Step2: Run pathogen quantification analysis on the HUMAnN output




Step1: Generate HUMAnN output of UniRef90 based functional gene classification
-------------------------------------------------------------------------------

Please consult https://huttenhower.sph.harvard.edu/humann for details. 

(i) Install HUMAnN and KneadData. 

(optional-check requirement:

	conda config --add channels defaults
	conda config --add channels bioconda
	conda config --add channels conda-forge
	conda config --add channels biobakery
) 

$ conda install humann -c biobakery

$ conda install -c bioconda kneaddata

(ii) Download necessary databases.

$ humann_databases --download chocophlan full $DIR --update-config yes

$ humann_databases --download uniref uniref90_diamond $DIR --update-config yes

$ humann_databases --download utility_mapping full $DIR --update-config yes

    $DIR = directory name/location

(iii) Generating HUMAnN output

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
Please check KneadData options to add necessary adapter files

c) Run HUMAnN and process output:

$ humann -v --input $INPUT --threads 32 --output $OUTPUT_DIR
    
    $INPUT = trimmed.fastq file name/location 
	$OUTPUT_DIR = the output directory name/location. If you have multiple samples create an empty directory to store $OUTPUT_DIR from all samples

Note: you can specify the --translated identity threshold parameter to 0.0 - 100.0. Default with UniRef90 is 80.0.

$ humann_join_tables -s --input $INPUT_DIR --output $TABLE --file_name genefamilies
  
    $INPUT_DIR = Name/location of directory containing HUMAnN2 output directories from samples to be joined
    $TABLE = Table name/location of joined table with all samples

$ humann_renorm_table --input $TABLE_IN --output $TABLE_OUT --units cpm --update-snames

    $TABLE_IN = Table name/location of joined table with all samples
    $TABLE_OUT = Table name/location of table with copies per million (cpm) normalization

$ humann_rename_table --input $TABLE_IN --names $NAMES --output $TABLE_OUT

    $TABLE_IN = Table name/location of table with copies per million (cpm) normalization 
    $TABLE_OUT =  Table name/location of joined normalized table with enzyme description
    $NAMES = use ‘uniref90’

$ humann_split_stratified_table --input $TABLE_IN --output $OUTPUT_DIR

    $TABLE_IN = Table name/location of joined normalized table with enzyme description
    $OUTPUT_DIR = Directory name/location containing stratified and unstratified tables
This will generate two *.tsv files, stratified and unstratified. 

Step2: Run pathogen quantification analysis on the HUMAnN output
-----------------------------------------------------------------

Clone the git repository https://github.com/sudeshna-ghosh/Pathogen-fluctuations

python pathogens_v2.py –db $DB  --o $OUTPUT_FILE $INPUT_FILE
 
    provide full path to directory with pathogens_v2.py
    $DB = Name/location of pathogen database folder (posted on github)
    $INPUT_FILE = Name/location of the unstratified genefamilies table in cpm 
    $OUTPUT_FILE = Name/location of pathogen abundance table in cpm of unique functional genes
	
optional arguments:

  -h, --help            show this help message and exit
  
  --db DB, -d DB        Database folder location
  
  --output_file   OUTPUT_FILE, -o OUTPUT_FILE
                        Output filename
			
  --max MAX    maximum abundance threshold : This will exclude genera with maximum 
	       abundance lower than the set threshhold. (Excludes genera with 
	       low abundance)
	       
  --diff DIFF  minimum difference threshold: difference between
               maximum and minimum abundances is less than or equal to
               this threshold. This will exclude genera with range of 
	       relative abundance below the set threshhold. (Excludes 
	       genera with low variation between samples)



Method for version 1 (older version)
--------------------
Step1: Generate HUMAnN2 output of UniRef90 based functional gene classification

Step2: Run pathogen quantification analysis on the HUMAnN2 output



Step1: Generate HUMAnN2 output of UniRef90 based functional gene classification
-------------------------------------------------------------------------------

(Note: recommend using HUMAnN3)

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

python pathogens_v1.py –db $DB  --o $OUTPUT_FILE $INPUT_FILE
 
    provide full path to directory with pathogens_v1.py
    $DB = Name/location of pathogen database folder (posted on github)
    $INPUT_FILE = Name/location of the unstratified genefamilies table in cpm 
    $OUTPUT_FILE = Name/location of pathogen abundance table in cpm of unique functional genes

1. Buchfink B, Xie C, Huson DH, "Fast and sensitive protein alignment using DIAMOND", Nature Methods 12, 59-60 (2015). doi:10.1038/nmeth.3176
2. Franzosa EA*, McIver LJ*, Rahnavard G, Thompson LR, Schirmer M, Weingart G, Schwarzberg Lipson K, Knight R, Caporaso JG, Segata N, Huttenhower C. Species-level functional profiling of metagenomes and metatranscriptomes. Nat Methods 15: 962-968 (2018).
