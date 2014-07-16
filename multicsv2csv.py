#!/usr/bin/python
'''
file for kaggle competition KDD cup 2014 
http://www.kaggle.com/c/kdd-cup-2014-predicting-excitement-at-donors-choose/

author: sonja brodersen sonja.brodersen@gmail.com
 
convert multiple csv files (projects, essays, outcomes) into 1 train.csv and test.csv
'''
# TODO: argv outfiles 

import sys
import pandas as pd
import re
import numpy as np

def convertTrueFalse(df,field):
    return df[field].map(lambda x: 1 if x== 't' else -1)

def clean(s):
    try:
        return " ".join(re.findall(r'\w+', s,flags = re.UNICODE | re.LOCALE)).lower()
    except:
        return " ".join(re.findall(r'\w+', "no_text",flags = re.UNICODE | re.LOCALE)).lower()


###################################################################
### read
projects = pd.read_csv('projects.csv.gz', compression='gzip', index_col='projectid', encoding='utf-8')
essays = pd.read_csv('essays.csv.gz', compression='gzip', index_col='projectid', encoding='utf-8')
outcomes = pd.read_csv('outcomes.csv.gz', compression='gzip', index_col='projectid', encoding='utf-8')
resources = pd.read_csv('resources.csv.gz', compression='gzip', index_col='projectid', encoding='utf-8')
projects = projects.sort_index(axis=0)
essays = essays.sort_index(axis=0)
outcomes = outcomes.sort_index(axis=0)
resources = resources.sort_index(axis=0)


# rs.groupby('project_resource_type').size()
#project_resource_type
#Books                    1575792
#Other                     264644
#Supplies                 1341579
#Technology                477598
#Trips                       6186
#Visitors                    1222
#dtype: int64

###################################################################
### feature engineering
outcomes['is_exciting'] = convertTrueFalse(outcomes, 'is_exciting')

prres = resources.groupby(level=0).agg([np.mean, np.size, np.std])
projects['vendorid_size'] = prres.vendorid['size']
projects['item_unit_price_mean'] = prres.item_unit_price['mean']
projects['item_unit_price_size'] = prres.item_unit_price['std']
projects['item_quantity_mean'] = prres.item_quantity['mean']
projects['item_quantity_size'] = prres.item_quantity['std']

dropIdx= ['school_latitude', 'school_longitude', 
          'school_city', 'school_state', 'school_district', 'school_county', 
          'teacher_acctid', 'schoolid', 'school_ncesid']
for x in dropIdx:
    projects = projects.drop(x, 1)

tfIdx = ['school_charter', 'school_magnet', 'school_year_round', 'school_nlns', 'school_kipp', 'school_charter_ready_promise', 'teacher_teach_for_america',
         'teacher_ny_teaching_fellow', 'eligible_almost_home_match', 'eligible_double_your_impact_match']
for i in tfIdx:
    projects[i] = convertTrueFalse(projects, i)

###### convert categorical (level) features
### school_metro list = [val for val in projects['school_metro'].unique()]
metro = {'nan':0, 'urban':3, 'rural':1, 'suburban':2}
projects['school_metro'] = projects['school_metro'].map(lambda x: metro[str(x)])
# poverty_level
# ['highest poverty', 'high poverty', 'moderate poverty', 'low poverty']
pov = {'highest poverty':4, 'high poverty':3, 'moderate poverty':2, 'low poverty':1}
projects['poverty_level'] = projects['poverty_level'].map(lambda x: pov[x])
# grade_level
#[val for val in projects['grade_level'].unique()]
projects['grade_level'] = projects['grade_level'].map(lambda x: 0 if str(x)=='nan' else str(x).split('-')[1])

# resource type categorical!
resource_types = [val for val in projects['resource_type'].unique()]
projects['resource_type'] = projects['resource_type'].map(lambda x: resource_types.index(x))
#'primary_focus_subject', 'primary_focus_area', 'secondary_focus_subject', 'secondary_focus_area',
subjects = [val for val in projects['primary_focus_subject'].unique()]
projects['primary_focus_subject'] = projects['primary_focus_subject'].map(lambda x: subjects.index(x))
areas = [val for val in projects['primary_focus_area'].unique()]
projects['primary_focus_area'] = projects['primary_focus_area'].map(lambda x: areas.index(x))
subjects = [val for val in projects['secondary_focus_subject'].unique()]
projects['secondary_focus_subject'] = projects['secondary_focus_subject'].map(lambda x: subjects.index(x))
areas = [val for val in projects['secondary_focus_area'].unique()]
projects['secondary_focus_area'] = projects['secondary_focus_area'].map(lambda x: areas.index(x))
#'teacher_prefix' categorical
prefixes = [val for val in projects['teacher_prefix'].unique()]
projects['teacher_prefix'] = projects['teacher_prefix'].map(lambda x: prefixes.index(x))


pro_ess = projects.join([essays.drop('teacher_acctid',1)])

########################################
# text features
pro_ess['essaystripped'] = pro_ess['essay'].apply(clean)
pro_ess['essaylength'] = pro_ess['essaystripped'].apply(lambda x: len(str(x)))
pro_ess = pro_ess.drop('essay',1)

pro_ess['titles'] = pro_ess['title'].apply(clean)
pro_ess = pro_ess.drop('title',1)

pro_ess['needs'] = pro_ess['need_statement'].apply(clean)
pro_ess = pro_ess.drop('need_statement',1)

pro_ess = pro_ess.drop('short_description', 1)

########################################
# split bunch into train and wanted
train = pro_ess[pro_ess['date_posted'] < '2014-01-01']
wanted = pro_ess[pro_ess['date_posted'] >= '2014-01-01']

train['is_exciting'] = outcomes['is_exciting']

print >> sys.stderr, train.columns


#######################################
# output

#wanted=wanted.fillna(0)
#train=train.fillna(0)

train.to_csv('train3.csv')
wanted.to_csv('wanted3.csv')
