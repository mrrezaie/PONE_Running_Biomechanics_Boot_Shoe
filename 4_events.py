import numpy as np
import pandas as pd
import sys, os, csv
sys.path.append('D:\\Academic\\Codes\\Python\\MRR')
from MRR import readOsimExp, getFile
from scipy.signal import butter, filtfilt, find_peaks
import matplotlib.pyplot as plt

def HS(FOOT):
	FOOT2 = FOOT - np.min(FOOT)
	FOOT2[FOOT2>20] = np.nan
	return find_peaks(np.diff(FOOT2,2), distance=50)[0] +2


def TO(KNEE, HIP):
	# np.where(HIP<0)[0]
	KNEE2 = np.copy(KNEE)
	KNEE[HIP>-5] = np.nan 
	return find_peaks(-KNEE, distance=50)[0]

# subjects
subj = ['s%02i' %i for i in range(1,21)]
# remove specific subjects
for i in ['s05', 's06']:
    try:
        del subj[subj.index(i)]
    except:
        pass

parent = 'E:\\MMMMM'

# i = 's01'
# j = 'boot'
# k = 'T2'
# %%
for i in subj:
	for j in ['boot', 'shoe']:
		for k in ['T1', 'T2', 'T3', 'T4']:
			direc = os.path.join(parent, i, j, k)
			markers = readOsimExp(os.path.join(direc, 'exp', f'{i}_{j}_{k}_markers.trc'))
			kin = readOsimExp(os.path.join(direc, 'results', f'{i}_{j}_{k}_Kinematics_q.sto'))
			FOOT = {'R':(markers['RFF']['y'].values + markers['RCAL']['y'].values) /2,
				'L':(markers['LFF']['y'].values + markers['LCAL']['y'].values) /2}
			RCAL = markers['RCAL']['y'].values
			LCAL = markers['LCAL']['y'].values
			# RFF = markers['RFF']['y'].values
			# LFF = markers['LFF']['y'].values
			RKNEE = kin['knee_angle_r'].values
			LKNEE = kin['knee_angle_l'].values
			RHIP = kin['hip_flexion_r'].values
			LHIP = kin['hip_flexion_l'].values
			events = dict()
			for ii,jj in enumerate(HS(RCAL).tolist()):
				events[f'RHS{ii+1}'] = jj
            if (ii+1)>2: print(i,j,k,'\tmore than 2 RHS')
            if (ii+1)<2: print(i,j,k,'\tless than 2 RHS')
			for ii,jj in enumerate(TO(RKNEE, RHIP).tolist()):
				events[f'RTO{ii+1}'] = jj
			for ii,jj in enumerate(HS(LCAL).tolist()):
				events[f'LHS{ii+1}'] = jj
            if (ii+1)>2: print(i,j,k,'\tmore than 2 LHS')
            if (ii+1)<2: print(i,j,k,'\tless than 2 LHS')
			for ii,jj in enumerate(TO(LKNEE, LHIP).tolist()):
				events[f'LTO{ii+1}'] = jj
			# sort events based on timing
			events2 = sorted([value,key] for (key,value) in events.items())
			events = dict()
			for ii in range(len(events2)):
				events[events2[ii][1]] = events2[ii][0]
			# plot the events and save the graphs
			for ii in ['R', 'L']:
				plt.close('all')
				plt.figure(ii+'FOOT')
				plt.title(f'{i}_{j}_{k}_{ii}FOOT')
				plt.plot(np.diff(FOOT[ii]), label=ii+'FOOT')
				for key,value in events.items():
					if key.startswith(ii+'HS'):
						plt.axvline(value, color='g', label=f'HS: {value}')
					elif key.startswith(ii+'TO'):
						plt.axvline(value, color='r', label=f'TO: {value}')
				plt.legend()
				# plt.show()
				plt.savefig(os.path.join(direc, 'exp', f'{i}_{j}_{k}_{ii}.png'))
			# write events to a text file
			# with open(os.path.join(direc, 'exp', f'{i}_{j}_{k}_events.txt'), 'wt') as f:
			# 	for key,value in events.items():
			# 		f.write(f'{key}\t{value}\n')
			# 
			# 
			# 
			# ###############################################################################
			# temporal and distance variables
			# ###############################################################################
			fs = round(1 / (markers['time'][1] - markers['time'][0]))
            RCAL,LCAL = np.zeros((markers.shape[0],3)), np.zeros((markers.shape[0],3))
			b,a = butter(4, 2*20/fs)
            RCAL[:,0] = filtfilt(b,a, markers['RCAL']['x'].values)
            RCAL[:,2] = filtfilt(b,a, markers['RCAL']['z'].values)
            Ry     = filtfilt(b,a, markers['RTOE']['y'].values)
            LCAL[:,0] = filtfilt(b,a, markers['LCAL']['x'].values)
            LCAL[:,2] = filtfilt(b,a, markers['LCAL']['z'].values)
            Ly     = filtfilt(b,a, markers['LTOE']['y'].values)
			# read events from file
            # events = dict()
            # with open(file=os.path.join(direc, 'exp', f'{i}_{j}_{k}_events.txt'), mode='rt') as f:
            #     a = csv.reader(f, delimiter='\t')
            #     for x in a:
            #         events[x[0]] = int(x[1])
            TD = dict() # temporal (s) and distance (m) variables
            TD['velocity'], TD['Rstance'],TD['Rswing'],TD['Rflight'],TD['Rstep'],TD['Rstride'],TD['Lstance'],TD['Lswing'],TD['Lflight'],TD['Lstep'],TD['Lstride'],TD['RstepWidth'],TD['RflightLength'],TD['RstepLength'],TD['RstrideLength'],TD['RstrideHeight'],TD['LstepWidth'],TD['LflightLength'],TD['LstepLength'],TD['LstrideLength'],TD['LstrideHeight'] = [[] for ii in range(21)]
            # velocity
            TD['velocity'].append(np.mean(np.diff(kin['pelvis_tx']) / np.diff(kin['time'])))
            ii = 1
            while True:
                for jj in ['R', 'L']:
                    # STANCE
                    try:
                        if events[f'{jj}HS{ii}'] < events[f'{jj}TO{ii}']:
                            TD[f'{jj}stance'].append(abs(events[f'{jj}HS{ii}'] - events[f'{jj}TO{ii}']) /fs)
                        else:
                            TD[f'{jj}stance'].append(abs(events[f'{jj}HS{ii}'] - events[f'{jj}TO{ii+1}']) /fs)
                        stance = True
                    except:
                        stance = None
                    # SWING
                    try:
                        if events[f'{jj}TO{ii}'] < events[f'{jj}HS{ii}']:
                            TD[f'{jj}swing'].append(abs(events[f'{jj}TO{ii}'] - events[f'{jj}HS{ii}']) /fs)
                        else:
                            TD[f'{jj}swing'].append(abs(events[f'{jj}TO{ii}'] - events[f'{jj}HS{ii+1}']) /fs)
                        swing = True
                    except:
                        swing = None
                    # stride
                    try:
                        TD[f'{jj}stride'].append(abs(events[f'{jj}HS{ii}'] - events[f'{jj}HS{ii+1}']) /fs)
                        if jj == 'R':
                            TD['RstrideLength'].append(abs(RCAL[events[f'{jj}HS{ii}'],0] - RCAL[events[f'{jj}HS{ii+1}'],0]) /10)
                            TD['RstrideHeight'].append(np.max(Ry[events[f'{jj}HS{ii}']:events[f'{jj}HS{ii+1}']] /10))
                        else:
                            TD['LstrideLength'].append(abs(LCAL[events[f'{jj}HS{ii}'],0] - LCAL[events[f'{jj}HS{ii+1}'],0]) /10)
                            TD['LstrideHeight'].append(np.max(Ly[events[f'{jj}HS{ii}']:events[f'{jj}HS{ii+1}']] /10))
                        stride = True
                    except:
                        stride = None
                # right step
                try:
                    if events['RHS1'] < events['LHS1']:
                        TD['Rstep'].append(abs(events[f'RHS{ii}'] - events[f'LHS{ii}']) /fs)
                        TD['RstepWidth'].append(abs(abs(RCAL[events[f'RHS{ii}'],2]) - abs(LCAL[events[f'LHS{ii}'],2])) /10)
                        TD['RstepLength'].append(abs(abs(RCAL[events[f'RHS{ii}'],0]) - abs(LCAL[events[f'LHS{ii}'],0])) /10)
                        if events['RHS1'] < events['RTO1']:
                            TD['Rflight'].append(abs(events[f'RTO{ii}'] - events[f'LHS{ii}']) /fs)
                            TD['RflightLength'].append(abs(abs(RCAL[events[f'RTO{ii}'],0]) - abs(LCAL[events[f'LHS{ii}'],0])) /10)
                        elif events['RHS1'] > events['RTO1']:
                            TD['Rflight'].append(abs(events[f'RTO{ii+1}'] - events[f'LHS{ii}']) /fs)
                            TD['RflightLength'].append(abs(abs(RCAL[events[f'RTO{ii+1}'],0]) - abs(LCAL[events[f'LHS{ii}'],0])) /10)
                    elif events['RHS1'] > events['LHS1']:
                        TD['Rstep'].append(abs(events[f'RHS{ii}'] - events[f'LHS{ii+1}']) /fs)
                        TD['RstepWidth'].append(abs(abs(RCAL[events[f'RHS{ii}'],2]) - abs(LCAL[events[f'LHS{ii+1}'],2])) /10)
                        TD['RstepLength'].append(abs(abs(RCAL[events[f'RHS{ii}'],0]) - abs(LCAL[events[f'LHS{ii+1}'],0])) /10)
                        if events['RHS1'] < events['RTO1']:
                            TD['Rflight'].append(abs(events[f'RTO{ii}'] - events[f'LHS{ii+1}']) /fs)
                            TD['RflightLength'].append(abs(abs(RCAL[events[f'RTO{ii}'],0]) - abs(LCAL[events[f'LHS{ii+1}'],0])) /10)
                        elif events['RHS1'] > events['RTO1']:
                            TD['Rflight'].append(abs(events[f'RTO{ii+1}'] - events[f'LHS{ii+1}']) /fs)
                            TD['RflightLength'].append(abs(abs(RCAL[events[f'RTO{ii+1}'],0]) - abs(LCAL[events[f'LHS{ii+1}'],0])) /10)
                    stepR = True
                except:
                    stepR = None
                # left step
                try:
                    if events['RHS1'] < events['LHS1']:
                        TD['Lstep'].append(abs(events[f'LHS{ii}'] - events[f'RHS{ii+1}']) /fs)
                        TD['LstepWidth'].append(abs(abs(LCAL[events[f'LHS{ii}'],2]) - abs(RCAL[events[f'RHS{ii+1}'],2])) /10)
                        TD['LstepLength'].append(abs(abs(LCAL[events[f'LHS{ii}'],0]) - abs(RCAL[events[f'RHS{ii+1}'],0])) /10)
                        if events['LHS1'] < events['LTO1']:
                            TD['Lflight'].append(abs(events[f'LTO{ii}'] - events[f'RHS{ii+1}']) /fs)
                            TD['LflightLength'].append(abs(abs(LCAL[events[f'LTO{ii}'],0]) - abs(RCAL[events[f'RHS{ii+1}'],0])) /10)
                        elif events['LHS1'] > events['LTO1']:
                            TD['Lflight'].append(abs(events[f'LTO{ii+1}'] - events[f'RHS{ii+1}']) /fs)
                            TD['LflightLength'].append(abs(abs(LCAL[events[f'LTO{ii+1}'],0]) - abs(RCAL[events[f'RHS{ii+1}'],0])) /10)
                    elif events['RHS1'] > events['LHS1']:
                        TD['Lstep'].append(abs(events[f'LHS{ii}'] - events[f'RHS{ii}']) /fs)
                        TD['LstepWidth'].append(abs(abs(LCAL[events[f'LHS{ii}'],2]) - abs(RCAL[events[f'RHS{ii}'],2])) /10)
                        TD['LstepLength'].append(abs(abs(LCAL[events[f'LHS{ii}'],0]) - abs(RCAL[events[f'RHS{ii}'],0])) /10)
                        if events['LHS1'] < events['LTO1']:
                            TD['Lflight'].append(abs(events[f'LTO{ii}'] - events[f'RHS{ii}']) /fs)
                            TD['LflightLength'].append(abs(abs(LCAL[events[f'LTO{ii}'],0]) - abs(RCAL[events[f'RHS{ii}'],0])) /10)
                        elif events['LHS1'] > events['LTO1']:
                            TD['Lflight'].append(abs(events[f'LTO{ii+1}'] - events[f'RHS{ii}']) /fs)
                            TD['LflightLength'].append(abs(abs(LCAL[events[f'LTO{ii+1}'],0]) - abs(RCAL[events[f'RHS{ii}'],0])) /10)
                    stepL = True
                except:
                    stepL = None
                if True not in [stance, swing, stride, stepR, stepL]:
                    break
                ii += 1
			# write variables to a file
            with open(os.path.join(direc, 'results', f'{i}_{j}_{k}_TD.txt'), 'wt') as f:
                for key,value in TD.items():
                    f.write(f'{key}')
                    for ii in value:
                        f.write(f'\t{round(ii,5)}')
                    f.write('\n')
