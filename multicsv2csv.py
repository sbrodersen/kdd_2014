#!/usr/bin/python
'''
file for kaggle competition KDD cup 2014 
http://www.kaggle.com/c/kdd-cup-2014-predicting-excitement-at-donors-choose/

author: sonja brodersen sonja.brodersen@gmail.com
 
convert multiple csv files (projects, essays, outcomes) into a train.csv and test.csv
'''
import sys
import pandas as pd
import re
import numpy as np

data_path = 'data/'

def convertTrueFalse(df,field):
    return df[field].map(lambda x: 1 if x== 't' else -1)

def clean(s):
    try:
        return " ".join(re.findall(r'\w+', s,flags = re.UNICODE | re.LOCALE)).lower()
    except:
        return " ".join(re.findall(r'\w+', "no_text",flags = re.UNICODE | re.LOCALE)).lower()

def read_data():
    projects = pd.read_csv(data_path+'projects.csv.gz', compression='gzip', index_col='projectid', encoding='utf-8')
    essays = pd.read_csv(data_path+'essays.csv.gz', compression='gzip', index_col='projectid', encoding='utf-8')
    outcomes = pd.read_csv(data_path+'outcomes.csv.gz', compression='gzip', index_col='projectid', encoding='utf-8')
    resources = pd.read_csv(data_path+'resources.csv.gz', compression='gzip', index_col='projectid', encoding='utf-8')
    projects = projects.sort_index(axis=0)
    essays = essays.sort_index(axis=0)
    outcomes = outcomes.sort_index(axis=0)
    resources = resources.sort_index(axis=0)
    return (projects, essays, outcomes, resources)

def feature_engineering(projects):
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
    return projects

def text_feature_engineering(projects, essays):
    pro_ess = projects.join([essays.drop('teacher_acctid',1)])
    pro_ess['essaystripped'] = pro_ess['essay'].apply(clean)
    pro_ess['essaylength'] = pro_ess['essaystripped'].apply(lambda x: len(str(x)))
    pro_ess = pro_ess.drop('essay',1)
    
    pro_ess['titles'] = pro_ess['title'].apply(clean)
    pro_ess = pro_ess.drop('title',1)
    
    pro_ess['needs'] = pro_ess['need_statement'].apply(clean)
    pro_ess = pro_ess.drop('need_statement',1)
    
    pro_ess = pro_ess.drop('short_description', 1)
    return pro_ess

def split_train_test(projects):
    train = projects[projects['date_posted'] < '2014-01-01']
    wanted = projects[projects['date_posted'] >= '2014-01-01']
    return (train, wanted) 

def output(train, wanted, train_file):
    train.to_csv(train_file)
    wanted.to_csv(train_file.replace("train","wanted"))

def resource_features(resources, projects):
    prres = resources.groupby(level=0).agg([np.mean, np.size, np.std])
    projects['vendorid_size'] = prres.vendorid['size']
    projects['item_unit_price_mean'] = prres.item_unit_price['mean']
    projects['item_unit_price_size'] = prres.item_unit_price['std']
    projects['item_quantity_mean'] = prres.item_quantity['mean']
    projects['item_quantity_size'] = prres.item_quantity['std']
    return projects

def main(argv):
    train_file = sys.argv[1]
    
    if train_file == '':
        print >> sys.stderr, 'usage: python csv2vw.py <filename>'
        sys.exit(2)
        
    # READ DATA
    (projects, essays, outcomes, resources) = read_data()
    ### FEATURE ENGINEERING
    # normal features
    projects = feature_engineering(projects)
    # aggregated resource features
    projects = resource_features(resources, projects)
    # text features
    projects = text_feature_engineering(projects, essays)
    
    # SPLIT TRAIN/TEST
    (train, wanted) = split_train_test(projects)
    
    # label
    outcomes['is_exciting'] = convertTrueFalse(outcomes, 'is_exciting')    
    train['is_exciting'] = outcomes['is_exciting']
    # verbose
    print >> sys.stderr, train.columns
    # output
    output(train, wanted, train_file)

if __name__ == "__main__":
    main(sys.argv[1:])



#### notes
#wanted=wanted.fillna(0)
#train=train.fillna(0)

# rs.groupby('project_resource_type').size()
#project_resource_type
#Books                    1575792
#Other                     264644
#Supplies                 1341579
#Technology                477598
#Trips                       6186
#Visitors                    1222
#dtype: int64