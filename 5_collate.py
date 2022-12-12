import numpy as np
# np.set_printoptions(suppress=True)
import pandas as pd
import sys, os, csv
sys.path.append('D:\\Academic\\Codes\\Python\\MRR')
from MRR import readOsimExp, interp
from scipy.signal import butter, filtfilt, find_peaks
import matplotlib.pyplot as plt

# subjects
subj = ['s%02i' %i for i in range(1,21)]
# remove specific subjects
for i in ['s05', 's06']:
    try:
        del subj[subj.index(i)]
    except:
        pass

parent = os.getcwd()
demo = pd.read_csv(os.path.join(parent, 'demographics.csv'), index_col=0)
g = 9.80665
speedRef = 12 # Km/h

tdLabel = ['velocity', 'Rstance', 'Rswing', 'Rflight','Rstep', 'Rstride', 'RstepWidth', 'RstepLength', 'RflightLength','RstrideLength', 'RstrideHeight', 'Lstance', 'Lswing','Lflight','Lstep', 'Lstride', 'LstepWidth', 'LstepLength','LflightLength','LstrideLength', 'LstrideHeight']
level0 = [h for h in tdLabel for i in range(len(subj)*2*4)]
level1 = [i for h in range(len(tdLabel)) for i in subj for j in range(8)]
level2 = [j for h in range(len(tdLabel)) for i in range(len(subj)) for j in ['boot', 'shoe'] for k in range(4)]
level3 = [k for h in range(len(tdLabel)) for i in range(len(subj)) for j in range(2) for k in ['T1', 'T2', 'T3', 'T4']]
TD = pd.DataFrame(index=range(1), data=np.nan*np.zeros((1,len(tdLabel)*len(subj)*2*4)), columns=[level0, level1, level2, level3])

grfLabel = ['x', 'y', 'z']
level0 = [h for h in grfLabel for i in range(len(subj)*2*4)]
level1 = [i for h in range(len(grfLabel)) for i in subj for j in range(8)]
level2 = [j for h in range(len(grfLabel)) for i in range(len(subj)) for j in ['boot', 'shoe'] for k in range(4)]
level3 = [k for h in range(len(grfLabel)) for i in range(len(subj)) for j in range(2) for k in ['T1', 'T2', 'T3', 'T4']]
grf = pd.DataFrame(index=range(101), data=np.zeros((101,len(grfLabel)*len(subj)*2*4)), columns=[level0, level1, level2, level3])

jointLabel = ['lumbar_extension', 'lumbar_bending', 'lumbar_rotation', 'hip_flexion', 'hip_adduction', 'hip_rotation', 'knee_angle', 'ankle_angle', 'subtalar_angle'] 
level0 = [h for h in jointLabel for i in range(len(subj)*2*4)]
level1 = [i for h in range(len(jointLabel)) for i in subj for j in range(8)]
level2 = [j for h in range(len(jointLabel)) for i in range(len(subj)) for j in ['boot', 'shoe'] for k in range(4)]
level3 = [k for h in range(len(jointLabel)) for i in range(len(subj)) for j in range(2) for k in ['T1', 'T2', 'T3', 'T4']]
jointi = pd.DataFrame(index=range(101), data=np.zeros((101,len(jointLabel)*len(subj)*2*4)), columns=[level0, level1, level2, level3])
jointc = jointi.copy()
veli = jointi.copy()
velc = jointi.copy()

bodyLabel = ['torso_Ox','torso_Oy','torso_Oz','pelvis_Ox','pelvis_Oy', 'pelvis_Oz', 'femur_Ox','femur_Oy','femur_Oz','tibia_Ox','tibia_Oy','tibia_Oz','calcn_Ox','calcn_Oy','calcn_Oz'] 
level0 = [h for h in bodyLabel for i in range(len(subj)*2*4)]
level1 = [i for h in range(len(bodyLabel)) for i in subj for j in range(8)]
level2 = [j for h in range(len(bodyLabel)) for i in range(len(subj)) for j in ['boot', 'shoe'] for k in range(4)]
level3 = [k for h in range(len(bodyLabel)) for i in range(len(subj)) for j in range(2) for k in ['T1', 'T2', 'T3', 'T4']]
bodyi = pd.DataFrame(index=range(101), data=np.zeros((101,len(bodyLabel)*len(subj)*2*4)), columns=[level0, level1, level2, level3])
bodyc = bodyi.copy()

momentLabel = ['lumbar_extension', 'lumbar_bending', 'lumbar_rotation', 'hip_flexion', 'hip_adduction', 'hip_rotation', 'knee_angle', 'knee_add', 'knee_rot', 'ankle_angle', 'subtalar_angle'] 
level0 = [h for h in momentLabel for i in range(len(subj)*2*4)]
level1 = [i for h in range(len(momentLabel)) for i in subj for j in range(8)]
level2 = [j for h in range(len(momentLabel)) for i in range(len(subj)) for j in ['boot', 'shoe'] for k in range(4)]
level3 = [k for h in range(len(momentLabel)) for i in range(len(subj)) for j in range(2) for k in ['T1', 'T2', 'T3', 'T4']]
moment = pd.DataFrame(index=range(101), data=np.zeros((101,len(momentLabel)*len(subj)*2*4)), columns=[level0, level1, level2, level3])
moment2 = moment.copy()

powerLabel = ['hip_flexion', 'hip_adduction', 'knee', 'ankle', 'subtalar'] 
level0 = [h for h in powerLabel for i in range(len(subj)*2*4)]
level1 = [i for h in range(len(powerLabel)) for i in subj for j in range(8)]
level2 = [j for h in range(len(powerLabel)) for i in range(len(subj)) for j in ['boot', 'shoe'] for k in range(4)]
level3 = [k for h in range(len(powerLabel)) for i in range(len(subj)) for j in range(2) for k in ['T1', 'T2', 'T3', 'T4']]
power = pd.DataFrame(index=range(101), data=np.zeros((101,len(powerLabel)*len(subj)*2*4)), columns=[level0, level1, level2, level3])
power2 = power.copy()

# i = 's01'
# j = 'boot'
# k = 'T1'

for i in subj:
	for j in ['boot', 'shoe']:
		for k in ['T1', 'T2', 'T3', 'T4']:
            direc = os.path.join(parent, i, j, k)
            # ###############################################################################
            # Temporal Distance variables
            # ###############################################################################
            td = dict()
            with open(file=os.path.join(direc, 'results', f'{i}_{j}_{k}_TD.txt'), mode='rt') as f:
                a = csv.reader(f, delimiter='\t')
                for x in a:
                    td[x[0]] = [float(x[y]) for y in range(1, len(x))]
            for label in tdLabel:
                TD.loc[:,(label,i,j,k)] = td[label][0]
            # sides
            s = demo['side'].loc[i][0]
            if s=='r': s2='l'
            elif s =='l': s2=='r'
            # FILES
            # static = readOsimExp(os.path.join(parent, i, j, 'static', f'{i}_{j}_static_position.mot'))
            forces = readOsimExp(os.path.join(direc, 'exp', f'{i}_{j}_{k}_forces.mot'))
            kinematics = readOsimExp(os.path.join(direc, 'results', f'{i}_{j}_{k}_Kinematics_q.sto'))
            ukinematics = readOsimExp(os.path.join(direc, 'results', f'{i}_{j}_{k}_Kinematics_u.sto'))
            bkinematics = readOsimExp(os.path.join(direc, 'results', f'{i}_{j}_{k}_BodyKinematics_pos_global.sto'))
            kinetics = readOsimExp(os.path.join(direc, 'results', f'{i}_{j}_{k}_inverse_dynamics.sto'))
            # ###############################################################################
            # GRF
            # ###############################################################################
            r = np.where(forces['ground_force_1_vy']>0)[0]
            for label in grfLabel:
                if s == 'l' and label == 'z':
                    grf.loc[:, (label,i,j,k)] = interp(-1*forces[f'ground_force_1_v{label}'][r[0]:r[-1]+1])
                else:
                    grf.loc[:, (label,i,j,k)] = interp(forces[f'ground_force_1_v{label}'][r[0]:r[-1]+1])
            # ###############################################################################
            # events
            # ###############################################################################
            e = dict() # events
            with open(file=os.path.join(direc, 'exp', f'{i}_{j}_{k}_events.txt'), mode='rt') as f:
                a = csv.reader(f, delimiter='\t')
                for x in a:
                    e[x[0]] = int(x[1])
            # ###############################################################################
            # joints angle
            # ###############################################################################
            # for ii in static.columns.to_list():
            #     if ii.endswith('/speed'):
            #         del static[ii]
            #     elif ii.endswith('/value'):
            #         static.columns = static.columns.str.replace(ii, ii.split('/')[3])
            # static.columns.to_list()
            # ipsilateral
            r = [e[f'{s.upper()}HS1'], e[f'{s.upper()}HS2']+1]
            r2 = [e[f'{s2.upper()}HS1'], e[f'{s2.upper()}HS2']+1]
            for label in jointLabel:
                if label.startswith('lumbar'):
                    jointi.loc[:,(label,i,j,k)] = (interp(kinematics[f'{label}'][r[0]:r[1]]))
                    veli.loc[:,(label,i,j,k)] = (interp(ukinematics[f'{label}'][r[0]:r[1]]))
                else:
                    jointi.loc[:,(label,i,j,k)] = (interp(kinematics[f'{label}_{s}'][r[0]:r[1]]))
                    veli.loc[:,(label,i,j,k)] = (interp(ukinematics[f'{label}_{s}'][r[0]:r[1]]))
                #  - static[f'{label}_{s}'].values
            # contralateral
            for label in jointLabel:
                if label.startswith('lumbar'):
                    jointc.loc[:,(label,i,j,k)] = (interp(kinematics[f'{label}'][r2[0]:r2[1]]))
                    velc.loc[:,(label,i,j,k)] = (interp(ukinematics[f'{label}'][r2[0]:r2[1]]))
                else:
                    jointc.loc[:,(label,i,j,k)] = (interp(kinematics[f'{label}_{s2}'][r2[0]:r2[1]]))
                    velc.loc[:,(label,i,j,k)] = (interp(ukinematics[f'{label}_{s2}'][r2[0]:r2[1]]))
            # ###############################################################################
            # body angle
            # ###############################################################################
            # ipsilateral
            for label in bodyLabel:
                label2 = label.split('_')
                if label2[0] in ['torso', 'pelvis']:
                    bodyi.loc[:,(label,i,j,k)] = (interp(bkinematics[f'{label}'][r[0]:r[1]]))
                else:
                    bodyi.loc[:,(label,i,j,k)] = (interp(bkinematics[f'{label2[0]}_{s}_{label2[1]}'][r[0]:r[1]]))
                #  - static[f'{label}_{s}'].values
            # contralateral
            for label in bodyLabel:
                label2 = label.split('_')
                if label2[0] in ['torso', 'pelvis']:
                    bodyc.loc[:,(label,i,j,k)] = (interp(bkinematics[f'{label}'][r2[0]:r2[1]]))
                else:
                    bodyc.loc[:,(label,i,j,k)] = (interp(bkinematics[f'{label2[0]}_{s2}_{label2[1]}'][r2[0]:r2[1]]))
            # ###############################################################################
            # joints moment
            # ###############################################################################
            # r = [e[f'{s.upper()}HS1'], e[f'{s.upper()}HS2']+1]
            if e[f'{s.upper()}TO1']+1 > e[f'{s.upper()}HS1']:
                r0 = [e[f'{s.upper()}HS1'], e[f'{s.upper()}TO1']+1]
            else:
                r0 = [e[f'{s.upper()}HS1'], e[f'{s.upper()}TO2']+1]
            for label in momentLabel:
                if label.startswith('lumbar'):
                    moment.loc[:,(label,i,j,k)] = interp(kinetics[f'{label}_moment'][r0[0]:r0[1]])
                    moment2.loc[:,(label,i,j,k)] = interp(kinetics[f'{label}_moment'][r[0]:r[1]])
                else:
                    moment.loc[:,(label,i,j,k)] = interp(kinetics[f'{label}_{s}_moment'][r0[0]:r0[1]])
                    moment2.loc[:,(label,i,j,k)] = interp(kinetics[f'{label}_{s}_moment'][r[0]:r[1]])
            # ###############################################################################
            # joints power
            # ###############################################################################
            # r = [e[f'{s.upper()}HS1'], e[f'{s.upper()}HS2']+1]
            if e[f'{s.upper()}TO1']+1 > e[f'{s.upper()}HS1']:
                r0 = [e[f'{s.upper()}HS1'], e[f'{s.upper()}TO1']+1]
            else:
                r0 = [e[f'{s.upper()}HS1'], e[f'{s.upper()}TO2']+1]
            for label in powerLabel:
                if label.startswith('hip'):
                    label2 = label
                else:
                    label2 = label+'_angle'
                power.loc[:,(label,i,j,k)] = interp(kinetics[f'{label2}_{s}_moment'][r0[0]:r0[1]] * np.radians(ukinematics[f'{label2}_{s}'][r0[0]:r0[1]]))
                power2.loc[:,(label,i,j,k)] = interp(kinetics[f'{label2}_{s}_moment'][r[0]:r[1]] * np.radians(ukinematics[f'{label2}_{s}'][r[0]:r[1]]))



# time normalized to 100% and data normalized to BW*LLL
TD.to_pickle(os.path.join(parent, 'collate', 'TD.zip'))
grf.to_pickle(os.path.join(parent, 'collate', 'grf.zip'))
jointi.to_pickle(os.path.join(parent, 'collate', 'jointi.zip'))
jointc.to_pickle(os.path.join(parent, 'collate', 'jointc.zip'))
bodyi.to_pickle(os.path.join(parent, 'collate', 'bodyi.zip'))
bodyc.to_pickle(os.path.join(parent, 'collate', 'bodyc.zip'))
# core.to_pickle(os.path.join(parent, 'collate', 'core.zip'))
moment.to_pickle(os.path.join(parent, 'collate', 'moment.zip'))
power.to_pickle(os.path.join(parent, 'collate', 'power.zip'))
moment2.to_pickle(os.path.join(parent, 'collate', 'moment2.zip'))
power2.to_pickle(os.path.join(parent, 'collate', 'power2.zip'))
veli.to_pickle(os.path.join(parent, 'collate', 'veli.zip'))
velc.to_pickle(os.path.join(parent, 'collate', 'velc.zip'))
