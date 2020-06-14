#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from pandas import DataFrame

projectprofiles = pd.read_csv('./User Project Profiles.csv')

#Inputs - Come From FrontEnd of Application
user_id = int(input("User ID : "))
project_track = input("Track needed : ")

matching_track_profiles = DataFrame(columns=projectprofiles.columns)
k = 1

for index, row in projectprofiles.iterrows():
#     print(row)
    if row['User_ID'] == user_id:
        user_profile = row
        continue
    tracks = row['Tracks_Worked_On'].split('.')
#     print(tracks)
    if project_track in tracks:
#         print(row)
        matching_track_profiles.loc[k] = row
        k+=1
        
matching_track_profiles["Compatibility_Score"] = 100

compat_attributes = ['Team_Work_Time_Preference', 'Alignment_of_Work', 'Team_Learn_and_Work_Preference', 'Team_Working_Hours_Preference', 'Mode_of_Communication_Preference', 'Style_of_Communication_Preference']

def adjust_compat_team_attributes(attribute_name, user, collaborator):
    if user[attribute_name] == collaborator[attribute_name[5:]] or user[attribute_name] == 0 or collaborator[attribute_name[5:]] == 0:
        compat_adjust = 0
    else:
        compat_adjust = -10
    return compat_adjust
        
def adjust_compat_standalone_attributes(attribute_name, user, collaborator):
    if user[attribute_name] == collaborator[attribute_name] or user[attribute_name] == 0 or collaborator[attribute_name] == 0:
        compat_adjust = 0
    else:
        compat_adjust = -10
    return compat_adjust
        
for index, row in matching_track_profiles.iterrows():
    compat_adjust = 0
    for attribute in compat_attributes:
        if attribute[0:4] == 'Team':
            compat_adjust += adjust_compat_team_attributes(attribute, user_profile, row)
        else:
            compat_adjust += adjust_compat_standalone_attributes(attribute, user_profile, row)
    row["Compatibility_Score"] = row["Compatibility_Score"] + compat_adjust
    matching_track_profiles.loc[index] = row

matching_profiles_dict = {}

for index, row in matching_track_profiles.iterrows():
    matching_profiles_dict[row["User_ID"]] = row["Compatibility_Score"]
    
print(matching_profiles_dict)

