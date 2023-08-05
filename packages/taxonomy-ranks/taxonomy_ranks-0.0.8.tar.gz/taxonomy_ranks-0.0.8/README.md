# taxonomy-ranks

## 1 Introduction
To get taxonomy ranks information with ETE3 Python3 module (`http://etetoolkit.org/`)

## 2 Installation

Make sure your `pip` is from Python3

	$ which pip
	/Users/mengguanliang/soft/miniconda3/bin/pip
	
then type

    $ pip install taxonomy_ranks

There will be a command `taxaranks` created under the same directory where your `pip` command located.


If you want to learn more about Python3 and `pip`, please refer to `https://www.python.org/` and `https://docs.python.org/3/tutorial/venv.html?highlight=pip`.

## 3 Usage
	
	$ taxaranks

	taxaranks <taxonomy_list> <outfile>
	
	The 'taxonomy_list' file can be a list of ncbi taxa id or species names (or higher ranks, e.g. Family, Order), or a mixture of them.
	
	ete3 package will automatically download the NCBI Taxonomy database during the first time using of this program.
	
	
Once the NCBI Taxonomy database has been installed, there is no need to connect to the network any more, unless you want to update the database after a period of time, for this case, please go to `http://etetoolkit.org/docs/latest/tutorial/tutorial_ncbitaxonomy.html` for more details.

### using as a module

A taxa_name may have more than one potential_taxid.

		>>>from taxonomy_ranks import TaxonomyRanks
	    >>>rank_taxon = TaxonomyRanks(taxa_name)
	    >>>rank_taxon.get_lineage_taxids_and_taxanames()
	    >>>ranks = ('user_taxa', 'taxa_searched', 'superkingdom', 'kingdom', 'superphylum', 'phylum', 'subphylum', 'superclass', 'class', 'subclass', 'superorder', 'order', 'suborder', 'superfamily', 'family', 'subfamily', 'genus', 'subgenus', 'species')
	    >>>for rank in ranks:
	    >>>    print(rank, rank_taxon.lineages[potential_taxid][rank])

## 4 Example

run 

	$ taxaranks test.taxa test.taxa.out

Input file `test.taxa`content:
	
	Spodoptera litura
	Pieris rapae
	Locusta migratoria
	Frankliniella occidentalis
	Marsupenaeus japonicus
	Penaeus monodon

Result file `test.taxa.out` content:

	superkingdom	kingdom	superphylum	phylum	subphylum	superclass	class	subclass	superorder	ordersuborder	superfamily	family	subfamily	genus	subgenus	species
	Eukaryota	Metazoa	NA	Arthropoda	Hexapoda	NA	NA	Pterygota	NA	Lepidoptera	Glossata	Noctuoidea	Noctuidae	Amphipyrinae	Spodoptera	NA	Spodoptera litura
	Eukaryota	Metazoa	NA	Arthropoda	Hexapoda	NA	NA	Pterygota	NA	Lepidoptera	Glossata	Papilionoidea	Pieridae	Pierinae	Pieris	NA	Pieris rapae
	Eukaryota	Metazoa	NA	Arthropoda	Hexapoda	NA	NA	Pterygota	NA	Orthoptera	Caelifera	Acridoidea	Acrididae	Oedipodinae	Locusta	NA	Locusta migratoria
	Eukaryota	Metazoa	NA	Arthropoda	Hexapoda	NA	NA	Pterygota	NA	Thysanoptera	Terebrantia	Thripoidea	Thripidae	Thripinae	Frankliniella	NA	Frankliniella occidentalis
	Eukaryota	Metazoa	NA	Arthropoda	Crustacea	Multicrustacea	NA	Eumalacostraca	Eucarida	Decapoda	Dendrobranchiata	Penaeoidea	Penaeidae	NA	Marsupenaeus	NA	Marsupenaeus japonicus
	Eukaryota	Metazoa	NA	Arthropoda	Crustacea	Multicrustacea	NA	Eumalacostraca	Eucarida	Decapoda	Dendrobranchiata	Penaeoidea	Penaeidae	NA	Penaeus	NA	Penaeus monodon

## 5 Problems
### Your HOME directory runs out of space when downloading and installing the NCBI Taxonomy database during the first time using of this program.

The error message can be:
	
	sqlite3.OperationalEoor: disk I/O error

This is caused by `ete3` which will create a directory `~/.etetoolkit` to store the databse (ca. 500M), however, your HOME directory does not have enough space left.

*Solutions:*    
The solution is obvious.   

1. create a directory somewhere else that have enough space left:

		$ mkdir /other/place/myetetoolkit


2. remove the directory `~/.etetoolkit`  created by `ete3`:

		$ rm -rf ~/.etetoolkit
	

3. link your new directory to the HOME directory:

		$ ln -s /other/place/myetetoolkit ~/.etetoolkit
		
4. run the program again:

		$ taxaranks my_taxonomy_list outfile

This way, ete3 should work as expected.


### Update the NCBI taxonomy database
For more details, refer to `http://etetoolkit.org/docs/latest/tutorial/tutorial_ncbitaxonomy.html`.

1. open a console, and type
	
		$ python3

	You will enter the Python3 command line status.

2. excute following commands in Python3
		
		>from ete3 import NCBITaxa
		>ncbi = NCBITaxa()
		>ncbi.update_taxonomy_database()


## 6 Citations
Currently, I have no plan to publish `taxonomy-ranks`.

However, since `taxonomy-ranks` makes use of the `ete3` toolkit, you should cite it if you use `taxonomy-ranks` in your publications. 

	ETE 3: Reconstruction, analysis and visualization of phylogenomic data.
	Jaime Huerta-Cepas, Francois Serra and Peer Bork. 
	Mol Biol Evol 2016; doi: 10.1093/molbev/msw046

Please go to `http://etetoolkit.org/` for more details.

## 7 Author

Guanliang MENG. 

linzhi2012 at gmail.com




