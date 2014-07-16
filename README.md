

use make to achieve your goals
================================

see Makefile


examples:
------------

to train your model with standard vw:
> make models/current/my_model.dat

to generate submit file for kaggle with your model == models/current/my_model.dat:
> make predictions/current/my_model.csv.gz

to train and generate standard submit file (--> predictions/current/a.csv.gz):
> make all
	
to train and generate standard submit file (--> predictions/current/a.csv):
> make all_uncompressed
	

if you know your data/xy.vw data is there execute do your vw commands and come back to generate the submit file from your model.
change variables according to your environment.