=================================================
So you want to start using that big data in NCBI?
=================================================
Authored by: Adina Howe & Fan Yang

===================
Learning objectives
===================
This is a tutorials for working with the data that is available in NCBI.  The learning objectives for this tutorial are as follows:

1.  To be able to download specific gene sequences or genomes from NCBI (even with a big list of gene sequences).
2.  To be able to create use these genes as a database to annotate a sequencing dataset.
3.  To estimate the number of genes and their corresponding annotations in multiple sequencing datasets.

You will need to know some things prior to this tutorial:

1.  Familiarity with the structure of NCBI website and their nucleotide and genome databases.
2.  Ability to navigate in the unix shell.
3.  Ability to execute programs in the shell.
4.  Access and login to an Amazon EC2 instance or similar ubuntu-based server

The key challenge that we will work through...or your mission, if you choose to accept it, is to identify nitrogen fixation genes found in sequencing DNA from soils.

You have been delivered three dogma-changing metagenomes (sequencing datasets) originating from three different Iowa crop soils (corn, soybean, and prairie).  You are interesting in identifying nitrogen fixation genes that are associated with native bacteria in these soils.  Nitrogen fixation is a natural process performed by bacteria that converts nitrogen in the atmosphere into a form that is usable for plants.  If we can optimize natural nitrogen fixation, our hope is to reduce nitrogen fertilizer inputs that may contribute to the eutrophication of downstream waters (e.g., dead zones in the Gulf of Mexico).

==========
Your tools
==========

Get your EC2 instance going - you need an Ubuntu 14.0 based instance (64-bit) with the free tier, t2.micro.

================
Getting the Data
================

Task 1
------
Get the metagenome datasets and scripts related to this tutorial.

All the tutorial materials are contained on a Github repository.  The reason for using Github is that this material can be updated by me and grabbed by you lucky folk seamlessly with just a couple commands.  To refresh your memmory, [here](https://github.com/edamame-course/Github/blob/master/Tutorial.md) is Jackson's github tutorial. If you are interested in learning more about Git, see this [tutorial](http://git-lectures.github.io/) also. Now, let's get some play data:     

    git clone https://github.com/germs-lab/tutorial-blast-annotation
 
This command will make a directory (or folder for those more Finder/Explorer inclined) named "tutorial-blast-annotation" in the location where it was run.  Within that directory, there will be two directories named "data" and "ncbi".  You can see this by navigating (hint:  cd) to the "tutorial-blast-annotation" directory and typing:
    
    ls -lah

This totorial is located in directory ["ncbi"](https://github.com/germs-lab/tutorial-blast-annotation/blob/master/ncbi/index.md). There are many more for you to explore on your own. 

Task 2
------
Navigate to the data directory and identify the number of sequences in each file.  Hint:  To find specific characters in a file, you can use [grep](http://www.gnu.org/software/grep/manual/html_node/Usage.html).  For example, to find all instances of AGTC in the corn.fa file, we could:

    grep AGTC corn.fa

To find sequences, we know that each sequence will start with a special character, ">".  This character in the shell, remember, is a bit special.  So to find it as a symbol in the text, we're going to put a '^' right before it in quotes:

    grep ^">" corn.fa

Now, to count, you'll remember we can use the command "wc", with a pipe...So you're command will look something like this:
    
    grep ^">" corn.fa | wc

Or...if you want to do this quicky::
   
    for x in *fa; do echo $x; grep ^">" $x | wc; done

To identify nitrogen fixation genes, you've been tasked to build a database of all previously observed known nitrogen fixation genes (nifH).  To build this database, you have been reading literature for about two weeks and come up with a list of about 30 genes:

gi|985477984|emb|LN997366.1|   
gi|985477986|emb|LN997367.1|   
gi|985477988|emb|LN997368.1|   
gi|985477990|emb|LN997369.1|   
...   
gi|38679|emb|X51500.1|  
gi|470075|emb|Z31716.1|   

You'll also see this list in a file in the data directory (hint:  use cat).

Task 3
------
Check out the file containing these gene IDs.

You have a sinking feeling like this isn't really leveraging the big data biology that everyone says sequencing technologies have provided.  You've decided to check out NCBI for its contents.

Task 4
------
Go to the NCBI webpage and identify an estimate of total nifH genes and download a list of their accession numbers.

You'll want to navigate in a web-browser to the `http://www.ncbi.nlm.nih.gov/`.  You'll see in the search query box that you can search a number of databases.  Here, we want to look at the nucleotide database and query something along the lines of nifH or nitrogen fixation.

When I did this, there were nearly 270,000 genes that were hit by this query.  You will want to look for the "Send To" link at the upper right of the page (put on a magnifying glass!), and download the GI list for this query.

Task 5
------
Find that file on your computer and give it a peek.  If you're feeling up for it, transfer it to your EC2 instance (hint:  scp).

To make this tutorial not-as-painful to complete in a reasonable amount of time, I've also made a list of 300 nifH genes from NCBI and put them in a file **300-nifh-genes.txt** in the data directory.  I would highly suggest you use this gene to build your database going forward in this tutorial.

Task 6
------
Take a look at this file.  Prove to yourself that it contains 300 genes (Hint:  wc)

Now, we are going to learn how to download these genes (by learning about the NCBI API below)

Task 7
------
Think about how you would download this data if you didn't have this tutorial.

You may have thought about some of the following:

1. Go to the web portal and look up each FASTA
2. Go to the [FTP site](ftp://ftp.ncbi.nlm.nih.gov/refseq/), find each genome, and download manually
3. Use the NCBI Web Services API to download the data

Among these, I'm going to assume many of you are familiar with the first two.  This tutorial then is going to focus on using APIs.

================================
Scaling "Getting the Data" On Up
================================

Here's some [answers](http://stackoverflow.com/questions/7440379/what-exactly-is-the-meaning-of-an-api) on what exactly is API, among which my favorite is "an interface through which you access someone else's code or through which someone else's code accesses yours -- in effect the public methods and properties."

The NCBI has a whole toolkit which they call **Entrez Programming Utilities** or **eutils** for short.  You can read all about it in the [documentation](http://www.ncbi.nlm.nih.gov/books/NBK25501/).  There are a lot of things you can do to interface with all things NCBI, including publications, etc., but I am going to focus today on downloading sequencing data. NCBI has also developed [Entrez Direct](http://www.ncbi.nlm.nih.gov/news/02-06-2014-entrez-direct-released/) to directly access, parse, and dowload from NCBI databases from command line.

Today we are going to focus on how to obtain sequence files using `curl` or `wget` and eutil web links from command line. To do this, you're going to be using one tool in **eutils**, called **efetch**.  There is a whole chapter devoted to [efetch](http://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EFetch) -- when I first started doing this kind of work, this documentation always broke my heart.  Its easier for me to just show you how to use it.

Task 8
------

Open a web browser, and check out what NCBI knows about this gene (nifH, in this case).  Check it out [here](http://www.ncbi.nlm.nih.gov/nuccore/X51500.1).

Task 9
------

Download the gene with eutils commands in your web-browser and take a look at the file.

On your web-browser, paste the following URL to download the nucleotide genome for gene **X51500.1**:   
    
    http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=X51500.1&rettype=fasta&retmode=text


Task 10
-------

Try downloading the GenBank file instead by pasting this onto your web-browser:

    http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=CP000962&rettype=gb&retmode=text

Do you notice the difference in these two commands?  Let's breakdown the command here:

1.  `http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?`  This is command telling your computer program (or your browser) to talk to the NCBI API tool efetch.
2.  `db=nuccore`  This command tells the NCBI API that you'd like it to look in this particular database for some data.  Other databases that the NCBI has available can be found [here](http://eutils.ncbi.nlm.nih.gov/entrez/eutils/einfo.fcgi).
3.  `id=X51500.1`  This command tells the NCBI API efetch the ID of the gene/genome you want to find.
4.  `rettype=gb&retmode=text`  These two commands tells the NCBI how the data is returned.  You'll note that in the two examples above this command varied slightly.  In the first, we asked for only the FASTA sequence, while in the second, we asked for the Genbank file.  Here's some elusive documentation on where to find these ["return" objects](http://www.ncbi.nlm.nih.gov/books/NBK25499/table/chapter4.T._valid_values_of__retmode_and/?report=objectonly).

Also, a useful command is also `version=1`.  There are different versions of sequences and some times that is useful.  For reproducibility, I try to specify versions in my queries, see these [comments](http://www.ncbi.nlm.nih.gov/Class/MLACourse/Modules/Format/exercises/qa_accession_vs_gi.html).

**Note:**

   Notice the "&" that comes between each of these little commands, it is necessary and important.


Ok, let's think of automating this sort of query.  So...we're moving from your lil laptop to your jumbo EC2 instance now.

Task 11
-------
Download a gene sequence on the command line.

Going back onto your instance, in the shell, you could run the same commands above with the addition of *curl* on your EC2 instance:    
    
    curl "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=X51500.1&rettype=fasta&retmode=text"


You'll see it fly on to your screen.  Don't panic - you can save it to a file and make it more useful BUT note the path you are in and where you will save this file (as long as you know...that's fine):    
    
    curl "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=X51500.1&rettype=fasta&retmode=text" > X51500.1.fa


You could now imagine writing a program where you made a list of IDs you want to download and put it in a for loop, *curling* each genome and saving it to a file.  The following is a shell script, ["fetch_genome.sh"](https://github.com/germs-lab/tutorial-blast-annotation/blob/master/ncbi/fetch_genome.sh). It should be located in your current directory. Let's take a quick look at it (Hint: less).

You'll see that the *id* here is a string character which is obtained from list of IDs contained in a separate file.  The rest of the script manages where the files are being placed and what they are named.  It also prints some output to the screen so you know its running.
    

You'll see that you need to provide a list of IDs (the first argument) and a directory where you want to save the downloaded files (the second argument).

Task 12a
--------

Run this script (note that your paths for the script or data may need to be specified) -- also see note below:   
    
    bash fetch_genome.sh ../data/300-nifh-genes.txt nifh_genes_fas


Sit back and think of the glory that is happening on your screen right now...

**Note:**    
If you are nervous....you may want to run this on just a few of these IDs to begin with.  You can create a smaller list using the *head* command with the -n parameter in the shell.  For example, `head -n 3 300-nifh-genes.txt > 3genes.txt`.

Task 12b
--------
After all the 300 genes are downloaded, you will want to concatenate them into one file (Hint: `cat` and `>>`), named "**all-nifH.fa**".

Task 13
-------
Take a break.   Put up your pink stickie if you need help with this.

====================================
Moving forward on your own: comparing your data to the databases
====================================

Frequently, we ask the question of whether a gene is present or not in our metagenome (and their potential abundance). 
There are lots of ways to do this and arguably "blasting" is one of the most common.
What we have done so far is collecting a specific set (i.e., nifH) of genes from a public database. We can use this collection as our new blast database.

To blast, you will need to:    
1. Format your downloaded nifH gene fasta file ("**all-nifH.fa**") for blast  
   (Hint: use `makeblastdb`)  
2. Perform blast  
   (Hint: use `blastn`)  

Also please see Tracy Teal's tutorial [here](https://github.com/edamame-course/BLAST-tutorial/blob/master/running-BLAST.md) for reference.

==========
Conclusion
==========

You now have the foundation for having some sequencing data that you need to compare to any database.  You should be able to generate the information needed to perform statistical analyses.  Note, that you can do this for specific genes and also genomes...!    Now, go forth and conquer!


====================================================
Bonus Material on Genbank Files and Genome downloads
====================================================

We also use a lot of python to work with eutil as well as blast results. The alternative version of this tutorial contains lots of python code. If you are interested, they can be found [here](https://github.com/germs-lab/tutorial-blast-annotation/blob/master/ncbi/index.txt).  
