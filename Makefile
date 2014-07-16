### variables
SOURCES=$(DATADIR)essays.csv.gz $(DATADIR)projects.csv.gz $(DATADIR)outcomes.csv.gz $(DATADIR)resources.csv.gz $(DATADIR)sampleSubmission.csv.gz
DATADIR=data/
MODELDIR=models/
SUBMITDIR=predictions/
TRAIN=$(DATADIR)train3.csv
TEST=$(DATADIR)wanted3.csv
TRAINVW=$(TRAIN:.csv=.vw)
TESTVW=$(TEST:.csv=.vw)
DEFAULTNAME=a
LOSS=logistic
PASSES=1
CACHEFILE=/tmp/c
VW_ARGS=--loss_function $(LOSS) --passes $(PASSES)
DIR=current/

### goals
readme:
	cat README

all: all_uncompressed $(SUBMITDIR)$(DIR)$(DEFAULTNAME).csv.gz
all_uncompressed: $(MODELDIR)$(DIR)$(DEFAULTNAME).dat $(SUBMITDIR)$(DIR)$(DEFAULTNAME).txt $(SUBMITDIR)$(DIR)$(DEFAULTNAME).csv

$(TRAIN): $(SOURCES)
	python multicsv2csv.py 

$(TEST): $(SOURCES)
	python multicsv2csv.py 
	
$(DATADIR)%.vw: $(DATADIR)%.csv
	python csv2vw.py $< $@

$(MODELDIR)%.dat: $(TRAINVW)
	vw -d $(TRAINVW) $(VW_ARGS) -k --cache_file $(CACHEFILE) -f $@

$(SUBMITDIR)%.txt: $(MODELDIR)%.dat $(TESTVW)
	vw -d $(TESTVW) -t -i $< -p $@ --quiet

$(SUBMITDIR)%.csv: $(SUBMITDIR)%.txt
	python vw2kaggle.py < $< > $@

$(SUBMITDIR)%.csv.gz: $(SUBMITDIR)%.csv
	pigz $<