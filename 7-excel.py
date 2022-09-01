import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

grf = pd.read_pickle('E:\\MMMMM\\collate\\grf.zip')
joint = pd.read_pickle('E:\\MMMMM\\collate\\jointc.zip')
velContra = pd.read_pickle('E:\\MMMMM\\collate\\velc.zip')
bodyContra = pd.read_pickle('E:\\MMMMM\\collate\\bodyc.zip')
moment = pd.read_pickle('E:\\MMMMM\\collate\\moment.zip')
power = pd.read_pickle('E:\\MMMMM\\collate\\power.zip')
TD = pd.read_pickle('E:\\MMMMM\\collate\\TD.zip')
demo = pd.read_csv('E:\\MMMMM\\demographics.csv', index_col=0)
g = 9.806

subj = ['s%02i' %i for i in range(1,21)]
# remove specific subjects
for i in ['s05', 's06', 's13']:
    try:
        del subj[subj.index(i)]
    except:
        pass

grfLabel = ['x', 'y', 'z']
level1 = [i for i in subj for j in range(4)]
level2 = [j for i in range(len(subj)) for j in ['boot', 'shoe'] for k in range(2)]
level3 = [k for i in range(len(subj)) for j in range(2) for k in ['mean', 'std']]
grf2=pd.DataFrame(index=range(101), columns=[level1, level2, level3])
grf2.to_excel('E:\\MMMMM\\collate\\data_grf.xlsx', sheet_name=grfLabel[0])
writer = pd.ExcelWriter('E:\\MMMMM\\collate\\data_grf.xlsx', mode='a', if_sheet_exists='replace')
for i in grfLabel:
	grf2=pd.DataFrame(index=range(101), columns=[level1, level2, level3])
	for j in subj:
		for k in ['boot', 'shoe']:
			grf2.loc[:,(j,k,'mean')] = grf[i][j][k].mean(axis=1).values / demo['mass'].loc[j]*g
			grf2.loc[:,(j,k,'std')] = grf[i][j][k].std(axis=1).values / demo['mass'].loc[j]*g
	grf2.to_excel(writer, sheet_name=i)
writer.close() 



powerLabel = ['hip_flexion', 'knee', 'ankle', 'hip_adduction']
power2=pd.DataFrame(index=range(101), columns=[level1, level2, level3])
power2.to_excel('E:\\MMMMM\\collate\\data_power.xlsx', sheet_name=powerLabel[0])
writer = pd.ExcelWriter('E:\\MMMMM\\collate\\data_power.xlsx', mode='a', if_sheet_exists='replace')
for i in powerLabel:
	power2=pd.DataFrame(index=range(101), columns=[level1, level2, level3])
	for j in subj:
		for k in ['boot', 'shoe']:
			power2.loc[:,(j,k,'mean')] = power[i][j][k].mean(axis=1).values / demo['mass'].loc[j]
			power2.loc[:,(j,k,'std')] = power[i][j][k].std(axis=1).values / demo['mass'].loc[j]
	power2.to_excel(writer, sheet_name=i)
writer.close() 



momentLabel = ['hip_flexion', 'hip_adduction', 'hip_rotation', 'knee_angle', 'knee_add', 'knee_rot', 'ankle_angle', 'subtalar_angle']
moment2=pd.DataFrame(index=range(101), columns=[level1, level2, level3])
moment2.to_excel('E:\\MMMMM\\collate\\data_moment.xlsx', sheet_name=momentLabel[0])
writer = pd.ExcelWriter('E:\\MMMMM\\collate\\data_moment.xlsx', mode='a', if_sheet_exists='replace')
for i in momentLabel:
	moment2=pd.DataFrame(index=range(101), columns=[level1, level2, level3])
	for j in subj:
		for k in ['boot', 'shoe']:
			moment2.loc[:,(j,k,'mean')] = moment[i][j][k].mean(axis=1).values / demo['mass'].loc[j]
			moment2.loc[:,(j,k,'std')] = moment[i][j][k].std(axis=1).values / demo['mass'].loc[j]
	moment2.to_excel(writer, sheet_name=i)
writer.close() 



jointLabel = ['hip_flexion', 'hip_adduction', 'hip_rotation', 'knee_angle', 'ankle_angle', 'subtalar_angle']
joint2=pd.DataFrame(index=range(101), columns=[level1, level2, level3])
joint2.to_excel('E:\\MMMMM\\collate\\data_angle.xlsx', sheet_name=jointLabel[0])
writer = pd.ExcelWriter('E:\\MMMMM\\collate\\data_angle.xlsx', mode='a', if_sheet_exists='replace')
for i in jointLabel:
	joint2=pd.DataFrame(index=range(101), columns=[level1, level2, level3])
	for j in subj:
		for k in ['boot', 'shoe']:
			joint2.loc[:,(j,k,'mean')] = joint[i][j][k].mean(axis=1).values
			joint2.loc[:,(j,k,'std')] = joint[i][j][k].std(axis=1).values
	joint2.to_excel(writer, sheet_name=i)
writer.close() 