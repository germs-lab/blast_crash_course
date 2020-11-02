=================================================
So you want to start using that big data in NCBI?
=================================================
Authored by: Adina Howe, Jia Liu, and Paul Villanueva; MODIFIED from a previous [tutorial](http://blast-tutorial.readthedocs.io/en/latest/ncbi/index.html)
=================================================

===================
Learning objectives
===================
This is a tutorial for working with sequencing data and running a program in shell.  The learning objectives for this tutorial are as follows:

1.  To be able to navigate and read a sequencing file in shell.
2.  To be able to run a command line blast.
3.  To be able to search a blast output file.

You will need to know some things prior to this tutorial:

1.  Access and login to an Amazon EC2 instance or similar ubuntu-based server
2.  A brief introduction to shell

Your mission, if you choose to accept it, is to XXXXXXXXXXXJia for you to fill in....

You have been delivered three dogma-changing metagenomes (sequencing datasets) originating from three different Iowa crop soils (corn, soybean, and prairie).  You are interesting in identifying nitrogen fixation genes that are associated with native bacteria in these soils.  Nitrogen fixation is a natural process performed by bacteria that converts nitrogen in the atmosphere into a form that is usable for plants.  If we can optimize natural nitrogen fixation, our hope is to reduce nitrogen fertilizer inputs that may contribute to the eutrophication of downstream waters (e.g., dead zones in the Gulf of Mexico).

==========
Your tools
==========

EC2 instance for computing with blast installed [Jia if you want you can have them isntall blast, that might be a fun learning exercise]
An intro to shell


================
Getting the Data
================

Suggested steps
1.  Look at the sequence file from seq facility
2.  Identify the database genes (look at it, possibly build it if you think there is time?)
3.  install blast?  i think its a good idea
4.  Run blast (makedb and a blast)
5.  Get output saved
6.  Look at output
7.  Grep something in the output 
