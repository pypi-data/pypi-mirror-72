# Card trick
A software package that extracts information from the ontology relationships 
from The Comprehensive Antibiotic Resistance Database (CARD) 
https://card.mcmaster.ca/home

Original code: https://gitlab.com/cgps/card_trick

Forked version code: https://gitlab.com/JFsanchezherrero/card_trick

This forked version retrieves all information for each entry available in CARD 
ontology information.

## Installation
This package requires Python3

```
pip3 install card-trick
```

## Usage
There are two main modules: search and update

```
usage: card-trick [-h] [-v] {update,search} ...

positional arguments:
  {update,search}  The following commands are available. Type card_trick
                   <COMMAND> -h for more help on a specific commands
    update         Get latest CARD ontology
    search         search CARD ontology

optional arguments:
  -h, --help       show this help message and exit
  -v, --version    display the version number
  --man            Additional information
```

### Download ontology database
```
usage: card-trick update [-h] [--path PATH] [-q QUIET]

optional arguments:
  -h, --help            show this help message and exit
  --path PATH           Path to store CARD ontology.
  -q QUIET, --quiet QUIET
                        Do not print process information
```


The update command `card-trick update` will download the latest version of the 
database. If already exists in the path provided (or default) it would update it.

Database in obo format is stored in your home directory in the .card-trick 
directory or in the directory stated using option --path 

Obo format file would be parsed into a csv file for later analysis.

All information for each entry in CARD ontology database are stored in the 
csv file.

### Search ontology database
```
usage: card-trick search -i INPUT -t {ARO,gene,antibiotic,target,any} 
                         [-f {json,csv,tsv,all}] [-o OUTPUT_NAME] [-p PATH] [-b]
                         [-i2 INPUT_2] [t2 {ARO,gene,antibiotic,target,any}] [-b2] [-q] [-h]

optional arguments:
  -h, --help            show this help message and exit
  
  -i INPUT, --input INPUT 
                        Input term to search in CARD ontology. Provide a unique 
                        term o several using --batch option
  
  -f {json,csv,tsv,all}, --format_output {json,csv,tsv,all}
                        Output format. csv, tsv or json
  
  -o OUTPUT_NAME, --output_name OUTPUT_NAME
                        Output name.
  
  -p PATH, --path PATH  
                        Path containing CARD ontology. Default is user’s home 
                        directory.
  
  -t {ARO,gene,antibiotic,target,any}, --term {ARO,gene,antibiotic,target,any}
                        The type of term provided to search.
  
  -b, --batch           Provide this option if input is a file containing
                        multiple terms, one per line.
  
  -i2 INPUT_2, --input_2 INPUT_2
                        Input term to search in results retrieved from first
                        input. Provide a unique term o several using --batch
                        option
  
  -t2 {ARO,gene,antibiotic,target,any}, --term_2 {ARO,gene,antibiotic,target,any}
                        The type of term provided to search for the second
                        input. Default: any
  
  -b2, --batch_2        Provide this option if input_2 is a file containing
                        multiple terms, one per line.
  
  -q, --quiet           Do not print process information

```

The command  `card-trick search` will return matches as a dataframe and print 
into a default tabular file. 

There are several possibilities to search the dataframe. This module can search for:
* gene entries
* ARO terms
* antibiotic to which a gene confers resistance 
* antibiotic to target a gene

No output is print to STDOUT as card-trick would retrieve all information from 
CARD ontology database and might be too much information.

There is a possibility to generate a batch search of multiple terms using option
batch.

Also, there is a possibility to link several searches: Use option --input_2, --term_2 or --batch_2
e.g. CTX genes that have a resistance to ceftazidime


Examples
```
## Different term options:
card-trick search -t antibiotic -i tigecycline
card-trick search -t target -i tigecycline
card-trick search -t gene -i ctx
card-trick search -t ARO -i ARO:3003032
card-trick search -t any -i ctx

## Using path database provided
card-trick search -t gene -i ctx --path /folder/to/card_ontology

## Batch example
card-trick search -t ARO --batch -i batch_entry_file.txt

## Multiple search
card-trick search -t gene -i ctx --path /folder/to/card_ontology -i2 ceftazidime -t2 antibiotic
card-trick search -t gene -i ctx --path /folder/to/card_ontology --batch_2 -i2 file.txt -t2 any 

## Output
card-trick search -t ARO --batch -i batch_entry_file.txt -f tsv -o example_name

```


## Using in a python script or program
Here is a simple code example to download, parse and search the database. 

If the database is download and parsed as a csv, just load the information to a 
pandas dataframe

```
import card_trick
import pandas as pd

CARD_folder=/path/to/your/database/ontology/card

## uptade database in a path
aro_obo_file = card_trick.ontology_functions.update_ontology(CARD_folder, False)

## get ontology and save it in csv
card_trick.ontology_functions.parse_ontology(aro_obo_file, False)

## load information
csv_file = CARD_folder + '/aro.obo.csv'
card_ontology = pd.read_csv(csv_file, sep=',', index_col=0)

## search for examples IDs
AROS_identified = ('ARO:3000026', 'ARO:3004058')
term = 'ARO'
information_ontology = card_trick_caller.get_info_CARD(AROS_identified, term, card_ontology)

```
