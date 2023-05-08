"""
Module Name:    Data Cleaning
Author:         Carlos Alberto Toruño Paniagua
Creation Date:  April 24th, 2023
Description:    This module contains the cleaning routine to consolidate all different 
                datamaps into a single database.
"""

# Importing required libraries
import os
import re
import pandas as pd

# Load data
path2data  = os.path.join(os.path.dirname(__file__), 
                          "Datamaps/")
path2files = [path2data + x for x in os.listdir(path2data)]
datamaps   = {re.search("(?<=DM_).+(?=\.xlsx)", file).group(): pd.read_excel(file) 
              for file in path2files
              if bool(re.search("GPP_2022_DM", file))}

# Concatenating datamaps and dropping duplicates
master_datamap = (pd
                  .concat([datamaps["CORE"], datamaps["EXP21"], datamaps["CAR"], datamaps["EXP22"]])
                  .drop_duplicates(subset = "merge")
                  .sort_values(by = "position")
                  .drop("position", axis = 1))

# Read STATA file
merged_info = pd.read_csv("merged_availability.csv")

# We fix the names from multiple choice questions to match the variable names in the datamap
multiple_choice = [
    "CAR_q13_1", "CAR_q20_1", "CAR_q21_1", "CAR_q22_1", "CAR_q35_1", "CAR_q42_1", "CAR_q43_1",
    "q25_1"
    ]

def mchoice_fix(row):
    vname = row["variable"]
    if vname in multiple_choice:
        new_vname = vname[:-2]
        return new_vname
    else:
        return vname

merged_info["variable"] = merged_info.apply(mchoice_fix, axis = 1)

# Fixing merge string values in the master datamap
# You need to individually check if there is NO OTHER variable with the following names in master_datamap. 
# For example:
# master_datamap.query("name == 'q66_G2'")
str_issue = [
    "q66_G2", "q24b_G2", "q24c_G2", "q24e_G2", "q24f_G2"
]

def str_fix(row):
    vname  = row["name"]
    vmerge = row["merge"]

    if vname in ["q24b_G2", "q24c_G2", "q24e_G2", "q24f_G2"]:
        prefix = "EXP_"
    elif vname in ["q66_G2"]:
        prefix = "CAR_"
    else:
        prefix = ""

    if vname in str_issue:
        new_name = prefix + vname
        return new_name
    else:
        return vmerge

master_datamap["merge"] = master_datamap.apply(str_fix, axis = 1)

# Fixing string value issues without a pattern
master_datamap.loc[master_datamap["name"]  == "q31", "merge"]  = "q22b"
master_datamap.loc[master_datamap["name"]  == "q34", "merge"]  = "q26"
master_datamap.loc[master_datamap["merge"] == "City", "merge"] = "city"

# Check which variables in the datamap are not in the merged file
# auxdf1 = master_datamap.merge(merged_info, 
#                               how       = "outer", 
#                               left_on   = "merge",
#                               right_on  = "variable",
#                               indicator = True)
# list1    = auxdf1.loc[auxdf1["_merge"] == "left_only", "merge"]
# notfound = master_datamap[master_datamap["merge"].isin(list1)]
# list2    = auxdf1.loc[auxdf1["_merge"] == "right_only", "variable"]
# notfound = merged_info[merged_info["variable"].isin(list2)]
# notfound.to_csv("notfound.csv")

# Joining data map info with merge availability
master_datamap = master_datamap.merge(merged_info, 
                                      how       = "left", 
                                      left_on   = "merge",
                                      right_on  = "variable")

# Replacing NaN in the availability column
master_datamap["availability"] = master_datamap["availability"].fillna("Always present")

# Creating new columns
master_datamap["available_countries"] = master_datamap["availability"].str.replace("[0-9\-]", "")
master_datamap["available_countries"] = (master_datamap["available_countries"]
                                         .str.split(", ")
                                         .apply(lambda x: ', '.join(sorted(set(x)))))
master_datamap["available_years"] = master_datamap["availability"].str.replace("[a-zA-Z\-\.'\s]", "")
master_datamap["available_years"] = (master_datamap["available_years"]
                                     .str.split(",")
                                     .apply(lambda x: ', '
                                            .join(sorted(set(filter(lambda y: y.strip() != '', x))))))
master_datamap.loc[master_datamap.availability == "Always present", "available_years"] = "Always present"

# Fixing modules
master_datamap.loc[master_datamap.module == "Contacts with the Police ", "module"] = "Contacts with the Police"
master_datamap.loc[master_datamap.module == "Post Survey Information", "module"]   = "Post-Survey Information"

# Save data for app
master_datamap.to_csv(os.path.join(path2data,
                                   "..",
                                   "datamap.csv"))
