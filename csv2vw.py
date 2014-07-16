#!/usr/bin/python
'''
file for kaggle competition KDD cup 2014 
http://www.kaggle.com/c/kdd-cup-2014-predicting-excitement-at-donors-choose/

author: sonja brodersen sonja.brodersen@gmail.com
 
convert from kdd train.csv/wanted.csv to train.vw/wanted.vw

usage: python csv2vw.py <infile> <outfile>

List of fields:
NS   INDEX   NAME
        0    projectid,
X
        1    school_zip,
        2    school_metro,
        3    school_charter,
        4    school_magnet,
        5    school_year_round,
        6    school_nlns,
        7    school_kipp,
        8    school_charter_ready_promise,
L
        9    teacher_prefix,
       10    teacher_teach_for_america,
       11    teacher_ny_teaching_fellow,
A
       12    primary_focus_subject,
       13    primary_focus_area,
       14    secondary_focus_subject,
       15    secondary_focus_area,
R
       16    resource_type,
P
       17    poverty_level,
O
       18    grade_level,
Z
       19    fulfillment_labor_materials,
       20    total_price_excluding_optional_support,
       21    total_price_including_optional_support,
S
       22    students_reached,
Y
       23    eligible_double_your_impact_match,
       24    eligible_almost_home_match,

       25    date_posted,
       26    vendorid_size,
       27    item_unit_price_mean,
       28    item_unit_price_size,
       29    item_quantity_mean,
       30    item_quantity_size,

E
       31    essaystripped,
C
       32    essaylength
T
       33    titles,
N
       34    needs
]
'''

import sys, csv

def main(argv):
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if input_file == '' or output_file == '':
        print >> sys.stderr, 'usage: python csv2vw.py <infile> <outfile>'
        sys.exit(2)
    
    reader = csv.reader( open( input_file ))
    with open(output_file, 'wb') as o:
        counter = 0
        for line in reader:
            if counter != 0:
                # set the label
                if(len(line)==35):
                    label = -1
                elif line[35] == '0':
                    label = -1
                else:
                    label = line[35]
                # configure the output line    
                output_line = "%s %s '%s " % (label, 1, line[0])# weight is 1
                output_line += "|X %s " % " ".join(line[1:9])
                output_line += "|lehrer %s " % " ".join(line[9:12])
                output_line += "|area %s " % " ".join(line[12:16])
                output_line += "|resource %s " % " ".join(line[16:17])
                output_line += "|poverty %s " % " ".join(line[17:18])
                output_line += "|old %s " % " ".join(line[18:19])
                output_line += "|z %s " % " ".join(line[19:22])
                output_line += "|students %s " % " ".join(line[22:23])
                output_line += "|y %s " % " ".join(line[23:25])
                output_line += "|v %s " % line[26]
                output_line += "|u %s " % " ".join(line[27:29])
                output_line += "|i %s " % " ".join(line[29:31])
                output_line += "|countessay %s " % line[32]
                output_line += "|essay %s " % line[31]
                output_line += "|title %s " % line[33]
                output_line += "|need %s " % line[34]
                output_line += "\n"
                o.write( output_line )
            counter += 1
            if counter % 100000 == 0:
                print counter


if __name__ == "__main__":
    main(sys.argv[1:])
    