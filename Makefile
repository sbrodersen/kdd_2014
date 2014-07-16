### variables
DEFAULTNAME=a
DEFAULTDIR=current/
DATADIR=data/
MODELDIR=models/
SUBMITDIR=predictions/

SOURCES=$(DATADIR)essays.csv.gz $(DATADIR)projects.csv.gz $(DATADIR)outcomes.csv.gz $(DATADIR)resources.csv.gz $(DATADIR)sampleSubmission.csv.gz
TRAIN=$(DATADIR)train_5.csv
TEST=$(DATADIR)wanted_5.csv
TRAINVW=$(TRAIN:.csv=.vw)
TESTVW=$(TEST:.csv=.vw)

### VW flags and args
LOSS=logistic
PASSES=1
CACHEFILE=/tmp/c
VW_ARGS=--loss_function $(LOSS) --passes $(PASSES)

### goals
readme:
	cat README
	
check_dirs:
	test -d $(DATADIR) || mkdir $(DATADIR)
	test -d $(MODELDIR) || mkdir $(MODELDIR)
	test -d $(SUBMITDIR) || mkdir $(SUBMITDIR)

	test -d $(MODELDIR)$(DEFAULTDIR) || mkdir $(MODELDIR)$(DEFAULTDIR)
	test -d $(SUBMITDIR)$(DEFAULTDIR) || mkdir $(SUBMITDIR)$(DEFAULTDIR)
	
all: all_uncompressed $(SUBMITDIR)$(DEFAULTDIR)$(DEFAULTNAME).csv.gz
	
all_uncompressed: check_dirs $(MODELDIR)$(DEFAULTDIR)$(DEFAULTNAME).dat $(SUBMITDIR)$(DEFAULTDIR)$(DEFAULTNAME).txt $(SUBMITDIR)$(DEFAULTDIR)$(DEFAULTNAME).csv
	
	
$(DATADIR)train_%.csv: 
	@test -d $(DATADIR) || mkdir $(DATADIR)
	python multicsv2csv.py $@
	
$(DATADIR)%.vw: $(DATADIR)%.csv
	@test -d $(DATADIR) || mkdir $(DATADIR)
	python csv2vw.py $< $@

$(MODELDIR)%.dat: $(TRAINVW)
	@test -d $(MODELDIR) || mkdir $(MODELDIR)
	vw -d $(TRAINVW) $(VW_ARGS) -k --cache_file $(CACHEFILE) -f $@

$(SUBMITDIR)%.txt: $(MODELDIR)%.dat $(TESTVW)
	@test -d $(SUBMITDIR) || mkdir $(SUBMITDIR)
	vw -d $(TESTVW) -t -i $< -p $@ --quiet

$(SUBMITDIR)%.csv: $(SUBMITDIR)%.txt
	@test -d $(SUBMITDIR) || mkdir $(SUBMITDIR)
	python vw2kaggle.py < $< > $@

$(SUBMITDIR)%.csv.gz: $(SUBMITDIR)%.csv
	@test -d $(SUBMITDIR) || mkdir $(SUBMITDIR)
	pigz $<

