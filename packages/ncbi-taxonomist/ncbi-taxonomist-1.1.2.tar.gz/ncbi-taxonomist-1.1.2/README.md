# Readme

## Synopsis

ncbi-taxonomist handles and manages phylogenetic data from NCBI's Entrez
[taxonomy database](https://www.ncbi.nlm.nih.gov/taxonomy) . It can:

  - fetch infomration from Entrez' Taxonomy database
  - map between taxids and names
  - resolve lineages for taxid, names, and accessions
  - store obtained taxa and their data locally in a SQLite database
  - group taxa into user defined groups (locally)
  - extract specific ranks or lineages from subtrees

taxonomist has several simple operations, e.g. `map` or `import`, which work
together using pipes, e.g. to populate a database, `collect` will fetch data
from Entrez and print it to STDOUT while `import` reads the STDIN to populate a
local database. Taxonomic information is obtained from Entrez.

## Install

```$pip install ncbi-taxonomist --user```

This will fetch and install `ncbi-taxonomist` and its required dependencies
(see below) use for an user (no `root` required).

### Containers

`ncbi-taxonomist` is available as Docker and Singularity image including
[`jq`](https://stedolan.github.io/jq/) to manipulate its JSON output.

#### Docker

The Docker image is available on its
[GitLab Docker registry](https://gitlab.com/janpb/ncbi-taxonomist/container_registry)
and can be pulled using `docker pull registry.gitlab.com/janpb/ncbi-taxonomist:latest`.

#### Singularity

The Singularity image is availabel in the
[Singularity library](https://cloud.sylabs.io/library/jpb/default/ncbi-taxonomist)
and can be pulled using `singularity pull library://jpb/default/ncbi-taxonomist`.


### Dependencies

`ncbi-taxonomist` has one dependency:

  - `entrezpy`: to handle remote requests to NCBI's Entrez databases

    - [Source](https://gitlab.com/ncbipy/entrezpy.git)
    - [PyPi](https://pypi.org/project/entrezpy/)
    - [Publication](https://doi.org/10.1093/bioinformatics/btz385)

`entrezpy` is developed and maintained in the group of Prof. Edward C. Holmes
at The University of Sydney. It relies  solely on the Python standard
library. Therefore, `ncbi-taxonomist` is less prone to suffer
[dependency hell](https://en.wikipedia.org/wiki/Dependency_hell).

## Usage

**`ncbi-taxonomist <command> <options>`**

### Available commands

call without any command or option  to  get an overview of available commands.

`$ ncbi-taxonomist`

### Command help

To get the usage for a specific command, use:

`$ ncbi-taxonomist <command> -h`

For example, to see available options for the command `map`, use:

`$ ncbi-taxonomist map -h`.

## Output

`ncbi-taxonist` uses line based `JSON` as output because I have no clue what
you want to do with the result. Parsing `JSON` is simpler than XML and most
programming languages have a JSON parser in their standard library. This
allows to write quick formatter or viewers reading data directly from `STDIN`.

In addition, [`jq`](https://stedolan.github.io/jq/) is an excellent tool to
filter and manipulate `JSON` data. An example how to extract attributes from the
`ncbi-taxonomist map` command `JSON` output can be found in the
[documentation](file:///home/jan/projects/ncbi-taxonomist/doc/sphinx/build/html/cookbook.html#):

For more `jq` help, please refer to:

  - [`jq` manual](https://stedolan.github.io/jq/manual/)
  - [Matthew Lincoln, "Reshaping JSON with jq," The Programming Historian 5 (2016)](https://programminghistorian.org/en/lessons/json-and-jq)


## Basic Commands

Examples how ti use the basic commands. It no local database is passed as
argument, NCBI's Entrez databases will be queried.

A more elaborate example is shown for the `collect` command below.

### `map`

map taxonomic information from Entrez phylogeny server or loading a downloaded
NCBI Taxonomy database into a local database. Returns taxonomic nodes in `JSON`.

#### Map taxid and names

```
$: ncbi-taxonomist map -t 562, 10508 -n 'Homo sapiens', 'black willow'
{"name":"black willow","taxon":{"taxon_id":75714,"rank":"species","names":{"Salix nigra":"scientific_name","black willow":"CommonName"},"parent_id":40685,"name":"Salix nigra"}}
{"name":"Homo sapiens","taxon":{"taxon_id":9606,"rank":"species","names":{"Homo sapiens":"scientific_name","human":"GenbankCommonName","man":"CommonName"},"parent_id":9605,"name":"Homo sapiens"}}
{"taxid":10508,"taxon":{"taxon_id":10508,"rank":"family","names":{"Adenoviridae":"scientific_name"},"parent_id":2732559,"name":"Adenoviridae"}}
{"taxid":562,"taxon":{"taxon_id":562,"rank":"species","names":{"Escherichia coli":"scientific_name","Bacillus coli":"Synonym","Bacterium coli":"Synonym","Bacterium coli commune":"Synonym","Enterococcus coli":"Synonym","E. coli":"CommonName","Escherichia sp. 3_2_53FAA":"Includes","Escherichia sp. MAR":"Includes","bacterium 10a":"Includes","bacterium E3":"Includes","Escherichia/Shigella coli":"EquivalentName","ATCC 11775":"type material","ATCC:11775":"type material","BCCM/LMG:2092":"type material","CCUG 24":"type material","CCUG 29300":"type material","CCUG:24":"type material","CCUG:29300":"type material","CIP 54.8":"type material","CIP:54.8":"type material","DSM 30083":"type material","DSM:30083":"type material","IAM 12119":"type material","IAM:12119":"type material","JCM 1649":"type material","JCM:1649":"type material","LMG 2092":"type material","LMG:2092":"type material","NBRC 102203":"type material","NBRC:102203":"type material","NCCB 54008":"type material","NCCB:54008":"type material","NCTC 9001":"type material","NCTC:9001":"type material","personal::U5/41":"type material","strain U5/41":"type material"},"parent_id":561,"name":"Escherichia coli"}}
```

#### Map accessions

```
$ ncbi-taxonomist map -a MH842226.1 NQWZ01000003 -edb nucleotide
{"accs":"NQWZ01000003","data":{"taxon_id":45151,"accessions":{"accessionversion":"NQWZ01000003.1","caption":"NQWZ01000003","extra":"gi|1391950314|gb|NQWZ01000003.1||gnl|WGS:NQWZ01|ARCrossB10_scaffold_00003"},"db":"nucleotide","uid":1391950314}}
{"accs":"MH842226.1","data":{"taxon_id":122929,"accessions":{"accessionversion":"MH842226.1","caption":"MH842226","extra":"gi|1476663987|gb|MH842226.1|"},"db":"nucleotide","uid":1476663987}}

```
### Resolve lineages for names, taxids, and accessions.

#### Resolve names and taxids remotely:

```
$: ncbi-taxonomist map -t 562, 10508 -n human, 'black willow'
{"name":"black willow","taxon":{"taxon_id":75714,"rank":"species","names":{"Salix nigra":"scientific_name","black willow":"CommonName"},"parent_id":40685,"name":"Salix nigra"}}
{"name":"human","taxon":{"taxon_id":9606,"rank":"species","names":{"Homo sapiens":"scientific_name","human":"GenbankCommonName","man":"CommonName"},"parent_id":9605,"name":"Homo sapiens"}}
{"taxid":10508,"taxon":{"taxon_id":10508,"rank":"family","names":{"Adenoviridae":"scientific_name"},"parent_id":2732559,"name":"Adenoviridae"}}
{"taxid":562,"taxon":{"taxon_id":562,"rank":"species","names":{"Escherichia coli":"scientific_name","Bacillus coli":"Synonym","Bacterium coli":"Synonym","Bacterium coli commune":"Synonym","Enterococcus coli":"Synonym","E. coli":"CommonName","Escherichia sp. 3_2_53FAA":"Includes","Escherichia sp. MAR":"Includes","bacterium 10a":"Includes","bacterium E3":"Includes","Escherichia/Shigella coli":"EquivalentName","ATCC 11775":"type material","ATCC:11775":"type material","BCCM/LMG:2092":"type material","CCUG 24":"type material","CCUG 29300":"type material","CCUG:24":"type material","CCUG:29300":"type material","CIP 54.8":"type material","CIP:54.8":"type material","DSM 30083":"type material","DSM:30083":"type material","IAM 12119":"type material","IAM:12119":"type material","JCM 1649":"type material","JCM:1649":"type material","LMG 2092":"type material","LMG:2092":"type material","NBRC 102203":"type material","NBRC:102203":"type material","NCCB 54008":"type material","NCCB:54008":"type material","NCTC 9001":"type material","NCTC:9001":"type material","personal::U5/41":"type material","strain U5/41":"type material"},"parent_id":561,"name":"Escherichia coli"}}

```


#### Resolve accessions

Accessions have to be mapped prior to resolve.

`$ ncbi-taxonomist map  -a MH842226.1 NQWZ01000003.1 -r | ncbi-taxonomist resolve -m`

Output:

```
{"accs":"MH842226.1","data":{"taxon_id":122929,"accessions":{"caption":"MH842226","accessionversion":"MH842226.1","extra":"gi|1476663987|gb|MH842226.1|"},"db":"nucleotide","uid":"1476663987","lin":[{"taxon_id":122929,"rank":null,"names":{"Norovirus GII":"scientific_name","Norovirus genogroup 2":"Synonym","Norovirus genogroup II":"Synonym","Norwalk-like virus genogroup 2":"Synonym","Norwalk-like viruses genogroup 2":"Synonym","human calicivirus genogroup 2":"Synonym"},"parent_id":11983,"name":"Norovirus GII"},{"taxon_id":11983,"rank":"species","names":{"Norwalk virus":"scientific_name"},"parent_id":142786,"name":"Norwalk virus"},{"taxon_id":142786,"rank":"genus","names":{"Norovirus":"scientific_name"},"parent_id":11974,"name":"Norovirus"},{"taxon_id":11974,"rank":"family","names":{"Caliciviridae":"scientific_name"},"parent_id":2559587,"name":"Caliciviridae"},{"taxon_id":2559587,"rank":null,"names":{"Riboviria":"scientific_name"},"parent_id":10239,"name":"Riboviria"},{"taxon_id":10239,"rank":"superkingdom","names":{"Viruses":"scientific_name"},"parent_id":null,"name":"Viruses"}]}}
{"accs":"NQWZ01000003.1","data":{"taxon_id":45151,"accessions":{"caption":"NQWZ01000003","accessionversion":"NQWZ01000003.1","extra":"gi|1391950314|gb|NQWZ01000003.1||gnl|WGS:NQWZ01|ARCrossB10_scaffold_00003"},"db":"nucleotide","uid":"1391950314","lin":[{"taxon_id":45151,"rank":"species","names":{"Pyrenophora tritici-repentis":"scientific_name","Pyrenophora triticirepentis":"Synonym","Drechslera tritici-repentis":"Anamorph","Pyrenophora sp. CBS 259.59":"Includes","Pyrenophora sp. MUCL 18687":"Includes"},"parent_id":5027,"name":"Pyrenophora tritici-repentis"},{"taxon_id":5027,"rank":"genus","names":{"Pyrenophora":"scientific_name"},"parent_id":28556,"name":"Pyrenophora"},{"taxon_id":28556,"rank":"family","names":{"Pleosporaceae":"scientific_name"},"parent_id":715340,"name":"Pleosporaceae"},{"taxon_id":715340,"rank":"suborder","names":{"Pleosporineae":"scientific_name"},"parent_id":92860,"name":"Pleosporineae"},{"taxon_id":92860,"rank":"order","names":{"Pleosporales":"scientific_name"},"parent_id":451868,"name":"Pleosporales"},{"taxon_id":451868,"rank":"subclass","names":{"Pleosporomycetidae":"scientific_name"},"parent_id":147541,"name":"Pleosporomycetidae"},{"taxon_id":147541,"rank":"class","names":{"Dothideomycetes":"scientific_name"},"parent_id":715962,"name":"Dothideomycetes"},{"taxon_id":715962,"rank":null,"names":{"dothideomyceta":"scientific_name"},"parent_id":716546,"name":"dothideomyceta"},{"taxon_id":716546,"rank":null,"names":{"leotiomyceta":"scientific_name"},"parent_id":147538,"name":"leotiomyceta"},{"taxon_id":147538,"rank":"subphylum","names":{"Pezizomycotina":"scientific_name"},"parent_id":716545,"name":"Pezizomycotina"},{"taxon_id":716545,"rank":null,"names":{"saccharomyceta":"scientific_name"},"parent_id":4890,"name":"saccharomyceta"},{"taxon_id":4890,"rank":"phylum","names":{"Ascomycota":"scientific_name"},"parent_id":451864,"name":"Ascomycota"},{"taxon_id":451864,"rank":"subkingdom","names":{"Dikarya":"scientific_name"},"parent_id":4751,"name":"Dikarya"},{"taxon_id":4751,"rank":"kingdom","names":{"Fungi":"scientific_name"},"parent_id":33154,"name":"Fungi"},{"taxon_id":33154,"rank":null,"names":{"Opisthokonta":"scientific_name"},"parent_id":2759,"name":"Opisthokonta"},{"taxon_id":2759,"rank":"superkingdom","names":{"Eukaryota":"scientific_name"},"parent_id":131567,"name":"Eukaryota"},{"taxon_id":131567,"rank":null,"names":{"cellular organisms":"scientific_name"},"parent_id":null,"name":"cellular organisms"}]}}
```

### `collect`

Collect taxid and names remotely, mainly to collect taxonomic data to store in
local database. Does not work on local database.

#### Collect taxid and names remotely

`$ ncbi-taxonomist collect -t 562,10508  -n man, 'Influenza B virus (B/Acre/121609/2012)'`

### Piping `ncbi-commands`

An example showing the individual steps and outputs to collect remote
taxonomies, store them in local database, and resolve the linages. The last
point shows how to  use  pipes to creta e small taxonomic pipeline.

#### 1. Collect taxa information remotely and import into local database `taxa.db`

```
$ ncbi-taxonomist collect -t 562,10508  -n man, 'Influenza B virus (B/Acre/121609/2012)' |  \
  ncbi-taxonomist import -db taxa.db
```

Output (first couple of lines):

```
{"taxon_id":10239,"rank":"superkingdom","names":{"Viruses":"scientific_name"},"parent_id":null,"name":"Viruses"}
{"taxon_id":2559587,"rank":null,"names":{"Riboviria":"scientific_name"},"parent_id":10239,"name":"Riboviria"}
{"taxon_id":2497569,"rank":"phylum","names":{"Negarnaviricota":"scientific_name"},"parent_id":2559587,"name":"Negarnaviricota"}
<cut>
```

##### 2. Test local database:

`$ sqlite3 -line taxa.db  'SELECT * FROM taxa;SELECT * FROM names;`

##### 3. Resolve lineages from local database:

`$ ncbi-taxonomist resolve -t 562,10508  -n man, 'Influenza B virus' -db taxa.db`

Output:

```
{"name":"man","lin":[{"taxon_id":9606,"rank":"species","names":{"Homo sapiens":"scientific_name","human":"GenbankCommonName","man":"CommonName"},"parent_id":9605,"name":"Homo sapiens"},{"taxon_id":9605,"rank":"genus","names":{"Homo":"scientific_name"},"parent_id":207598,"name":"Homo"},{"taxon_id":207598,"rank":"subfamily","names":{"Homininae":"scientific_name"},"parent_id":9604,"name":"Homininae"},{"taxon_id":9604,"rank":"family","names":{"Hominidae":"scientific_name"},"parent_id":314295,"name":"Hominidae"},{"taxon_id":314295,"rank":"superfamily","names":{"Hominoidea":"scientific_name"},"parent_id":9526,"name":"Hominoidea"},{"taxon_id":9526,"rank":"parvorder","names":{"Catarrhini":"scientific_name"},"parent_id":314293,"name":"Catarrhini"},{"taxon_id":314293,"rank":"infraorder","names":{"Simiiformes":"scientific_name"},"parent_id":376913,"name":"Simiiformes"},{"taxon_id":376913,"rank":"suborder","names":{"Haplorrhini":"scientific_name"},"parent_id":9443,"name":"Haplorrhini"},{"taxon_id":9443,"rank":"order","names":{"Primates":"scientific_name"},"parent_id":314146,"name":"Primates"},{"taxon_id":314146,"rank":"superorder","names":{"Euarchontoglires":"scientific_name"},"parent_id":1437010,"name":"Euarchontoglires"},{"taxon_id":1437010,"rank":null,"names":{"Boreoeutheria":"scientific_name"},"parent_id":9347,"name":"Boreoeutheria"},{"taxon_id":9347,"rank":null,"names":{"Eutheria":"scientific_name"},"parent_id":32525,"name":"Eutheria"},{"taxon_id":32525,"rank":null,"names":{"Theria":"scientific_name"},"parent_id":40674,"name":"Theria"},{"taxon_id":40674,"rank":"class","names":{"Mammalia":"scientific_name"},"parent_id":32524,"name":"Mammalia"},{"taxon_id":32524,"rank":null,"names":{"Amniota":"scientific_name"},"parent_id":32523,"name":"Amniota"},{"taxon_id":32523,"rank":null,"names":{"Tetrapoda":"scientific_name"},"parent_id":1338369,"name":"Tetrapoda"},{"taxon_id":1338369,"rank":null,"names":{"Dipnotetrapodomorpha":"scientific_name"},"parent_id":8287,"name":"Dipnotetrapodomorpha"},{"taxon_id":8287,"rank":"superclass","names":{"Sarcopterygii":"scientific_name"},"parent_id":117571,"name":"Sarcopterygii"},{"taxon_id":117571,"rank":null,"names":{"Euteleostomi":"scientific_name"},"parent_id":117570,"name":"Euteleostomi"},{"taxon_id":117570,"rank":null,"names":{"Teleostomi":"scientific_name"},"parent_id":7776,"name":"Teleostomi"},{"taxon_id":7776,"rank":null,"names":{"Gnathostomata":"scientific_name"},"parent_id":7742,"name":"Gnathostomata"},{"taxon_id":7742,"rank":null,"names":{"Vertebrata":"scientific_name"},"parent_id":89593,"name":"Vertebrata"},{"taxon_id":89593,"rank":"subphylum","names":{"Craniata":"scientific_name"},"parent_id":7711,"name":"Craniata"},{"taxon_id":7711,"rank":"phylum","names":{"Chordata":"scientific_name"},"parent_id":33511,"name":"Chordata"},{"taxon_id":33511,"rank":null,"names":{"Deuterostomia":"scientific_name"},"parent_id":33213,"name":"Deuterostomia"},{"taxon_id":33213,"rank":null,"names":{"Bilateria":"scientific_name"},"parent_id":6072,"name":"Bilateria"},{"taxon_id":6072,"rank":null,"names":{"Eumetazoa":"scientific_name"},"parent_id":33208,"name":"Eumetazoa"},{"taxon_id":33208,"rank":"kingdom","names":{"Metazoa":"scientific_name"},"parent_id":33154,"name":"Metazoa"},{"taxon_id":33154,"rank":null,"names":{"Opisthokonta":"scientific_name"},"parent_id":2759,"name":"Opisthokonta"},{"taxon_id":2759,"rank":"superkingdom","names":{"Eukaryota":"scientific_name"},"parent_id":131567,"name":"Eukaryota"},{"taxon_id":131567,"rank":null,"names":{"cellular organisms":"scientific_name"},"parent_id":null,"name":"cellular organisms"}]}
{"name":"Influenza B virus (B/Acre/121609/2012)","lin":[{"taxon_id":1334390,"rank":null,"names":{"Influenza B virus (B/Acre/121609/2012)":"scientific_name"},"parent_id":11520,"name":"Influenza B virus (B/Acre/121609/2012)"},{"taxon_id":11520,"rank":"species","names":{"Influenza B virus":"scientific_name"},"parent_id":197912,"name":"Influenza B virus"},{"taxon_id":197912,"rank":"genus","names":{"Betainfluenzavirus":"scientific_name"},"parent_id":11308,"name":"Betainfluenzavirus"},{"taxon_id":11308,"rank":"family","names":{"Orthomyxoviridae":"scientific_name"},"parent_id":2499411,"name":"Orthomyxoviridae"},{"taxon_id":2499411,"rank":"order","names":{"Articulavirales":"scientific_name"},"parent_id":2497577,"name":"Articulavirales"},{"taxon_id":2497577,"rank":"class","names":{"Insthoviricetes":"scientific_name"},"parent_id":2497571,"name":"Insthoviricetes"},{"taxon_id":2497571,"rank":"subphylum","names":{"Polyploviricotina":"scientific_name"},"parent_id":2497569,"name":"Polyploviricotina"},{"taxon_id":2497569,"rank":"phylum","names":{"Negarnaviricota":"scientific_name"},"parent_id":2559587,"name":"Negarnaviricota"},{"taxon_id":2559587,"rank":null,"names":{"Riboviria":"scientific_name"},"parent_id":10239,"name":"Riboviria"},{"taxon_id":10239,"rank":"superkingdom","names":{"Viruses":"scientific_name"},"parent_id":null,"name":"Viruses"}]}
{"taxid":562,"lin":[{"taxon_id":562,"rank":"species","names":{"Escherichia coli":"scientific_name","Bacillus coli":"Synonym","Bacterium coli":"Synonym","Bacterium coli commune":"Synonym","Enterococcus coli":"Synonym","E. coli":"CommonName","Escherichia sp. 3_2_53FAA":"Includes","Escherichia sp. MAR":"Includes","bacterium 10a":"Includes","bacterium E3":"Includes","Escherichia/Shigella coli":"EquivalentName","ATCC 11775":"type material","ATCC:11775":"type material","BCCM/LMG:2092":"type material","CCUG 24":"type material","CCUG 29300":"type material","CCUG:24":"type material","CCUG:29300":"type material","CIP 54.8":"type material","CIP:54.8":"type material","DSM 30083":"type material","DSM:30083":"type material","IAM 12119":"type material","IAM:12119":"type material","JCM 1649":"type material","JCM:1649":"type material","LMG 2092":"type material","LMG:2092":"type material","NBRC 102203":"type material","NBRC:102203":"type material","NCCB 54008":"type material","NCCB:54008":"type material","NCTC 9001":"type material","NCTC:9001":"type material"},"parent_id":561,"name":"Escherichia coli"},{"taxon_id":561,"rank":"genus","names":{"Escherichia":"scientific_name"},"parent_id":543,"name":"Escherichia"},{"taxon_id":543,"rank":"family","names":{"Enterobacteriaceae":"scientific_name"},"parent_id":91347,"name":"Enterobacteriaceae"},{"taxon_id":91347,"rank":"order","names":{"Enterobacterales":"scientific_name"},"parent_id":1236,"name":"Enterobacterales"},{"taxon_id":1236,"rank":"class","names":{"Gammaproteobacteria":"scientific_name"},"parent_id":1224,"name":"Gammaproteobacteria"},{"taxon_id":1224,"rank":"phylum","names":{"Proteobacteria":"scientific_name"},"parent_id":2,"name":"Proteobacteria"},{"taxon_id":2,"rank":"superkingdom","names":{"Bacteria":"scientific_name"},"parent_id":131567,"name":"Bacteria"},{"taxon_id":131567,"rank":null,"names":{"cellular organisms":"scientific_name"},"parent_id":null,"name":"cellular organisms"}]}
{"taxid":10508,"lin":[{"taxon_id":10508,"rank":"family","names":{"Adenoviridae":"scientific_name"},"parent_id":10239,"name":"Adenoviridae"},{"taxon_id":10239,"rank":"superkingdom","names":{"Viruses":"scientific_name"},"parent_id":null,"name":"Viruses"}]}
```

##### 4. All in one go

```
$ ncbi-taxonomist collect -t 562,10508  -n man, 'Influenza B virus (B/Acre/121609/2012)' |  \
  ncbi-taxonomist import -db taxa.db  | ncbi-taxonomist resolve
```

Output:

Please note: this will return taxids, not names, But the lineages are identical.
```
{"taxid":1334390,"lin":[{"taxon_id":1334390,"rank":null,"names":{"Influenza B virus (B/Acre/121609/2012)":"scientific_name"},"parent_id":11520,"name":"Influenza B virus (B/Acre/121609/2012)"},{"taxon_id":11520,"rank":"species","names":{"Influenza B virus":"scientific_name"},"parent_id":197912,"name":"Influenza B virus"},{"taxon_id":197912,"rank":"genus","names":{"Betainfluenzavirus":"scientific_name"},"parent_id":11308,"name":"Betainfluenzavirus"},{"taxon_id":11308,"rank":"family","names":{"Orthomyxoviridae":"scientific_name"},"parent_id":2499411,"name":"Orthomyxoviridae"},{"taxon_id":2499411,"rank":"order","names":{"Articulavirales":"scientific_name"},"parent_id":2497577,"name":"Articulavirales"},{"taxon_id":2497577,"rank":"class","names":{"Insthoviricetes":"scientific_name"},"parent_id":2497571,"name":"Insthoviricetes"},{"taxon_id":2497571,"rank":"subphylum","names":{"Polyploviricotina":"scientific_name"},"parent_id":2497569,"name":"Polyploviricotina"},{"taxon_id":2497569,"rank":"phylum","names":{"Negarnaviricota":"scientific_name"},"parent_id":2559587,"name":"Negarnaviricota"},{"taxon_id":2559587,"rank":null,"names":{"Riboviria":"scientific_name"},"parent_id":10239,"name":"Riboviria"},{"taxon_id":10239,"rank":"superkingdom","names":{"Viruses":"scientific_name"},"parent_id":null,"name":"Viruses"}]}
{"taxid":9606,"lin":[{"taxon_id":9606,"rank":"species","names":{"Homo sapiens":"scientific_name","human":"GenbankCommonName","man":"CommonName"},"parent_id":9605,"name":"Homo sapiens"},{"taxon_id":9605,"rank":"genus","names":{"Homo":"scientific_name"},"parent_id":207598,"name":"Homo"},{"taxon_id":207598,"rank":"subfamily","names":{"Homininae":"scientific_name"},"parent_id":9604,"name":"Homininae"},{"taxon_id":9604,"rank":"family","names":{"Hominidae":"scientific_name"},"parent_id":314295,"name":"Hominidae"},{"taxon_id":314295,"rank":"superfamily","names":{"Hominoidea":"scientific_name"},"parent_id":9526,"name":"Hominoidea"},{"taxon_id":9526,"rank":"parvorder","names":{"Catarrhini":"scientific_name"},"parent_id":314293,"name":"Catarrhini"},{"taxon_id":314293,"rank":"infraorder","names":{"Simiiformes":"scientific_name"},"parent_id":376913,"name":"Simiiformes"},{"taxon_id":376913,"rank":"suborder","names":{"Haplorrhini":"scientific_name"},"parent_id":9443,"name":"Haplorrhini"},{"taxon_id":9443,"rank":"order","names":{"Primates":"scientific_name"},"parent_id":314146,"name":"Primates"},{"taxon_id":314146,"rank":"superorder","names":{"Euarchontoglires":"scientific_name"},"parent_id":1437010,"name":"Euarchontoglires"},{"taxon_id":1437010,"rank":null,"names":{"Boreoeutheria":"scientific_name"},"parent_id":9347,"name":"Boreoeutheria"},{"taxon_id":9347,"rank":null,"names":{"Eutheria":"scientific_name"},"parent_id":32525,"name":"Eutheria"},{"taxon_id":32525,"rank":null,"names":{"Theria":"scientific_name"},"parent_id":40674,"name":"Theria"},{"taxon_id":40674,"rank":"class","names":{"Mammalia":"scientific_name"},"parent_id":32524,"name":"Mammalia"},{"taxon_id":32524,"rank":null,"names":{"Amniota":"scientific_name"},"parent_id":32523,"name":"Amniota"},{"taxon_id":32523,"rank":null,"names":{"Tetrapoda":"scientific_name"},"parent_id":1338369,"name":"Tetrapoda"},{"taxon_id":1338369,"rank":null,"names":{"Dipnotetrapodomorpha":"scientific_name"},"parent_id":8287,"name":"Dipnotetrapodomorpha"},{"taxon_id":8287,"rank":"superclass","names":{"Sarcopterygii":"scientific_name"},"parent_id":117571,"name":"Sarcopterygii"},{"taxon_id":117571,"rank":null,"names":{"Euteleostomi":"scientific_name"},"parent_id":117570,"name":"Euteleostomi"},{"taxon_id":117570,"rank":null,"names":{"Teleostomi":"scientific_name"},"parent_id":7776,"name":"Teleostomi"},{"taxon_id":7776,"rank":null,"names":{"Gnathostomata":"scientific_name"},"parent_id":7742,"name":"Gnathostomata"},{"taxon_id":7742,"rank":null,"names":{"Vertebrata":"scientific_name"},"parent_id":89593,"name":"Vertebrata"},{"taxon_id":89593,"rank":"subphylum","names":{"Craniata":"scientific_name"},"parent_id":7711,"name":"Craniata"},{"taxon_id":7711,"rank":"phylum","names":{"Chordata":"scientific_name"},"parent_id":33511,"name":"Chordata"},{"taxon_id":33511,"rank":null,"names":{"Deuterostomia":"scientific_name"},"parent_id":33213,"name":"Deuterostomia"},{"taxon_id":33213,"rank":null,"names":{"Bilateria":"scientific_name"},"parent_id":6072,"name":"Bilateria"},{"taxon_id":6072,"rank":null,"names":{"Eumetazoa":"scientific_name"},"parent_id":33208,"name":"Eumetazoa"},{"taxon_id":33208,"rank":"kingdom","names":{"Metazoa":"scientific_name"},"parent_id":33154,"name":"Metazoa"},{"taxon_id":33154,"rank":null,"names":{"Opisthokonta":"scientific_name"},"parent_id":2759,"name":"Opisthokonta"},{"taxon_id":2759,"rank":"superkingdom","names":{"Eukaryota":"scientific_name"},"parent_id":131567,"name":"Eukaryota"},{"taxon_id":131567,"rank":null,"names":{"cellular organisms":"scientific_name"},"parent_id":null,"name":"cellular organisms"}]}
{"taxid":562,"lin":[{"taxon_id":562,"rank":"species","names":{"Escherichia coli":"scientific_name","Bacillus coli":"Synonym","Bacterium coli":"Synonym","Bacterium coli commune":"Synonym","Enterococcus coli":"Synonym","E. coli":"CommonName","Escherichia sp. 3_2_53FAA":"Includes","Escherichia sp. MAR":"Includes","bacterium 10a":"Includes","bacterium E3":"Includes","Escherichia/Shigella coli":"EquivalentName","ATCC 11775":"type material","ATCC:11775":"type material","BCCM/LMG:2092":"type material","CCUG 24":"type material","CCUG 29300":"type material","CCUG:24":"type material","CCUG:29300":"type material","CIP 54.8":"type material","CIP:54.8":"type material","DSM 30083":"type material","DSM:30083":"type material","IAM 12119":"type material","IAM:12119":"type material","JCM 1649":"type material","JCM:1649":"type material","LMG 2092":"type material","LMG:2092":"type material","NBRC 102203":"type material","NBRC:102203":"type material","NCCB 54008":"type material","NCCB:54008":"type material","NCTC 9001":"type material","NCTC:9001":"type material"},"parent_id":561,"name":"Escherichia coli"},{"taxon_id":561,"rank":"genus","names":{"Escherichia":"scientific_name"},"parent_id":543,"name":"Escherichia"},{"taxon_id":543,"rank":"family","names":{"Enterobacteriaceae":"scientific_name"},"parent_id":91347,"name":"Enterobacteriaceae"},{"taxon_id":91347,"rank":"order","names":{"Enterobacterales":"scientific_name"},"parent_id":1236,"name":"Enterobacterales"},{"taxon_id":1236,"rank":"class","names":{"Gammaproteobacteria":"scientific_name"},"parent_id":1224,"name":"Gammaproteobacteria"},{"taxon_id":1224,"rank":"phylum","names":{"Proteobacteria":"scientific_name"},"parent_id":2,"name":"Proteobacteria"},{"taxon_id":2,"rank":"superkingdom","names":{"Bacteria":"scientific_name"},"parent_id":131567,"name":"Bacteria"},{"taxon_id":131567,"rank":null,"names":{"cellular organisms":"scientific_name"},"parent_id":null,"name":"cellular organisms"}]}
{"taxid":10508,"lin":[{"taxon_id":10508,"rank":"family","names":{"Adenoviridae":"scientific_name"},"parent_id":10239,"name":"Adenoviridae"},{"taxon_id":10239,"rank":"superkingdom","names":{"Viruses":"scientific_name"},"parent_id":null,"name":"Viruses"}]}
```


#### Format specific filed from map output to csv using `jq`

- Extract  taxid, rank, and scientific name from `map` `JSON` output using `jq`:

```
ncbi-taxonomist map -t 2 -n human -r | \
jq -r '[.taxon.taxon_id,.taxon.rank,(.taxon.names|to_entries[]|select(.value=="scientific_name").key)]|@csv'
```


### Subtree to extract lineages and ranks

Subtree can extract whole or partial lineages from any taxid within its lineage.
This command works currently only with a local database. This examples creates
local database to demonstrate the command.

#### Creating a local database:

```
$ ncbi-taxonomist collect -t 142786 9606 | ncbi-taxonomist import -db test.db
```

#### Obtaining subtrees

```
$ ncbi-taxonomist subtree -db test.db -t 142786 9606 --lrank order --hrank phylum
{"taxid":9606,"subtrees":[{"taxon_id":9443,"rank":"order","names":{"Primates":"scientific_name"},"parent_id":314146,"name":"Primates"},{"taxon_id":314146,"rank":"superorder","names":{"Euarchontoglires":"scientific_name"},"parent_id":1437010,"name":"Euarchontoglires"},{"taxon_id":1437010,"rank":"NA","names":{"Boreoeutheria":"scientific_name"},"parent_id":9347,"name":"Boreoeutheria"},{"taxon_id":9347,"rank":"NA","names":{"Eutheria":"scientific_name"},"parent_id":32525,"name":"Eutheria"},{"taxon_id":32525,"rank":"NA","names":{"Theria":"scientific_name"},"parent_id":40674,"name":"Theria"},{"taxon_id":40674,"rank":"class","names":{"Mammalia":"scientific_name"},"parent_id":32524,"name":"Mammalia"},{"taxon_id":32524,"rank":"NA","names":{"Amniota":"scientific_name"},"parent_id":32523,"name":"Amniota"},{"taxon_id":32523,"rank":"NA","names":{"Tetrapoda":"scientific_name"},"parent_id":1338369,"name":"Tetrapoda"},{"taxon_id":1338369,"rank":"NA","names":{"Dipnotetrapodomorpha":"scientific_name"},"parent_id":8287,"name":"Dipnotetrapodomorpha"},{"taxon_id":8287,"rank":"superclass","names":{"Sarcopterygii":"scientific_name"},"parent_id":117571,"name":"Sarcopterygii"},{"taxon_id":117571,"rank":"NA","names":{"Euteleostomi":"scientific_name"},"parent_id":117570,"name":"Euteleostomi"},{"taxon_id":117570,"rank":"NA","names":{"Teleostomi":"scientific_name"},"parent_id":7776,"name":"Teleostomi"},{"taxon_id":7776,"rank":"NA","names":{"Gnathostomata":"scientific_name"},"parent_id":7742,"name":"Gnathostomata"},{"taxon_id":7742,"rank":"NA","names":{"Vertebrata":"scientific_name"},"parent_id":89593,"name":"Vertebrata"},{"taxon_id":89593,"rank":"subphylum","names":{"Craniata":"scientific_name"},"parent_id":7711,"name":"Craniata"},{"taxon_id":7711,"rank":"phylum","names":{"Chordata":"scientific_name"},"parent_id":33511,"name":"Chordata"}]}
{"taxid":142786,"subtrees":[{"taxon_id":464095,"rank":"order","names":{"Picornavirales":"scientific_name"},"parent_id":2732506,"name":"Picornavirales"},{"taxon_id":2732506,"rank":"class","names":{"Pisoniviricetes":"scientific_name"},"parent_id":2732408,"name":"Pisoniviricetes"},{"taxon_id":2732408,"rank":"phylum","names":{"Pisuviricota":"scientific_name"},"parent_id":2732396,"name":"Pisuviricota"}]}
```
### Group

Groups can organize taxa into non-taxonomic groups, e.g. taxa used
in an experiment. The example collects two species by its common name,
stores them in a local database and adds the to the group 'tree'.
../src/ncbi-taxonomist resolve  -n 'Black willow' 'Black hickory' -db test4.db | ../src/ncbi-taxonomist group --add tree -db test4.db

```
$ ncbi-taxonomist collect -n 'Black willow' 'Black hickory' | \
  ncbi-taxonomist import -db taxa.db                        | \
  ncbi-taxonomist group --add tree -db taxa.db
```

#### Retrieve a group

Groups can be retrieved as taxids and processed, e.g. with `jq`, and reused.

```
$ ncbi-taxonomist group --get tree -db taxa.db  | \
  jq '.taxa[]'                                  | \
  ncbi-taxonomist map -t -db taxa.db
```
