# %%
import spm1d
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
plt.rcParams['axes.facecolor']='white'
plt.rcParams['savefig.facecolor']='white'
import pandas as pd
import numpy as np
import os
from scipy import stats
import sys
sys.path.append('D:\\Academic\\Codes\\Python\\MRR')
from MRR import readOsimExp
from scipy import stats

tt = True # two-tailed 
alpha_P = 0.05
g = 9.81
# subjects
subj = ['s%02i' %i for i in range(1,21)]
# remove specific subjects
for i in ['s05', 's06', 's13']:
    try:
        del subj[subj.index(i)]
    except:
        pass

parent = os.path.join(os.getcwd(), 'collate')
demo = pd.read_csv(os.path.join(os.getcwd(), 'demographics.csv'), index_col=0)

def default():
    ax.plot(np.mean(b,axis=0), label='boot', color='darkblue', lw=2, ls='solid')
    ax.fill_between(range(101), np.mean(b,axis=0)-np.std(b,axis=0), np.mean(b,axis=0)+np.std(b,axis=0), color='tab:blue', alpha=0.25, linewidth=0.0, label='boot±SD')
    ax.plot(np.mean(s,axis=0), label='shoe', color='darkred', lw=2, ls='dashed')
    ax.fill_between(range(101), np.mean(s,axis=0)-np.std(s,axis=0), np.mean(s,axis=0)+np.std(s,axis=0), color='orangered', alpha=0.25, linewidth=0.0, label='shoe±SD')
    ax.set_xlim((0,100))
    ax.set_ylim((np.min((b,s)), np.max((b,s)))) #np.max((b,s)), np.max((b,s))-0.1*np.max((b,s))
    ax.grid(True)



def annotate(spmi, thr=0.5):
    ax.fill_between(range(101), -100000, 100000, where=(np.abs(spmi.z)>=spmi.zstar), color='tab:green', alpha=0.2,label='Sig. diff')
    for iii in spmi.clusters:
        print('\t\t', np.round(iii.endpoints,1))
        if iii.P <= 0.001 : t = 'P<0.001'
        else: t = f'P={round(iii.P,3)}'
        if np.mean((np.mean(b,axis=0),np.mean(s,axis=0)),axis=0)[round(iii.centroid[0])] <= np.mean((b,s)):
            # r = np.max((b,s)) - 0.1*np.max((b,s))
            r = np.mean((np.mean(b,axis=0),np.mean(s,axis=0)),axis=0)[round(iii.centroid[0])] + thr*(np.max((b,s))-np.min((b,s)))
            typ='bottom'
        else:
            # r = np.min((b,s)) + 0.1*np.min((b,s))
            r = np.mean((np.mean(b,axis=0),np.mean(s,axis=0)),axis=0)[round(iii.centroid[0])] - thr*(np.max((b,s))-np.min((b,s)))
            typ='top'
        ax.text(iii.centroid[0], r, t, verticalalignment=typ, horizontalalignment='center', fontsize=12, fontweight='bold', rotation='horizontal', bbox=dict(facecolor='white', alpha=0.7))



# %%
grf = pd.read_pickle(os.path.join(parent, 'grf.zip'))
title = ['Anterior-Posterior', 'Vertical', 'Medial-Lateral']
plt.close('all')
plt.figure(figsize=(15,5), tight_layout=True)
plt.suptitle('Ground Reaction Force', fontsize=21, fontweight='bold')
for ii,i in enumerate(['x', 'y', 'z']):
    print(i)
    b = list()
    s = list()
    for j in subj:
        b.append(grf[i][j]['boot'].mean(axis=1).values / (demo['mass'].loc[j]*g))
        s.append(grf[i][j]['shoe'].mean(axis=1).values / (demo['mass'].loc[j]*g))
        # b.append(grf[i][j]['boot'].mean(axis=1).values)
        # s.append(grf[i][j]['shoe'].mean(axis=1).values)
        # plt.figure(j)
        # plt.plot(grf[i][j]['boot'].values, color='b')
        # plt.plot(grf[i][j]['shoe'].values, color='r')
        # plt.show()
    # plot
    ax = plt.subplot(1, 3, ii + 1)
    default()
    spm = spm1d.stats.ttest_paired(b, s)
    spmi = spm.inference(alpha=alpha_P, two_tailed=tt)
    annotate(spmi, thr=0.45)
    ax.set_xlabel('Stance (%)')
    ax.set_title(title[ii])
    if ii in [0,3,6]:
        ax.set_ylabel('N [%BW]')
    if ii == 2:
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

plt.savefig(os.path.join(parent, 'grf.png'), dpi=300, bbox_inches='tight')
#
# 
# 
# 
# 
# %%
# core = pd.read_pickle('E:\\MMMMM\\collate\\core.zip')
# coreLabel = ['pelvis_Ox', 'pelvis_Oy', 'pelvis_Oz', 'torso_Ox', 'torso_Oy', 'torso_Oz', 'lumbar_extension', 'lumbar_bending', 'lumbar_rotation']
# plt.close('all')
# plt.figure(figsize=(15,13.5), tight_layout=True)
# plt.suptitle('Core Kinematics', fontsize=21, fontweight='bold')
# for ii,i in enumerate(coreLabel):
#     # print(i)
#     row = int(len(coreLabel)/3)
#     b = list()
#     s = list()
#     for j in subj:
#         b.append(core[i][j]['boot'].mean(axis=1).values)
#         s.append(core[i][j]['shoe'].mean(axis=1).values)
#         # b.append(core[i][j]['boot'].mean(axis=1).values)
#         # s.append(core[i][j]['shoe'].mean(axis=1).values)
#     spm = spm1d.stats.ttest_paired(b, s)
#     spmi = spm.inference(alpha=alpha_P, two_tailed=tt)
#     # plot
#     ax = plt.subplot(int(len(coreLabel)/3), 3, ii + 1)
#     default()
#     annotate(spmi, thr=0.3)
#     ax.set_xlabel('Stride (%)')
#     ax.set_title(i)
#     if ii in [0,3,6]:
#         ax.set_ylabel('Angle (deg)')
#     if ii == 2:
#         ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

# plt.savefig('E:\\MMMMM\\collate\\core.png', dpi=300, bbox_inches='tight')
# 
# 
# 
# 
# 
# %%
bt = 35.52
st = 36
jointIpsi = pd.read_pickle(os.path.join(parent, 'jointi.zip'))
jointContra = pd.read_pickle(os.path.join(parent, 'jointc.zip'))
jointLabel = ['hip_flexion', 'hip_adduction', 'hip_rotation', 'knee_angle', 'ankle_angle', 'subtalar_angle'] #'lumbar_extension', 'lumbar_bending', 'lumbar_rotation', 
title = ['Hip Flexion(+)', 'Hip Adduction(+)', 'Hip Internal Rotation(+)', 'Knee Flexion (+)', 'Ankle Dorsiflexion (+)', 'Subtalar Supination (+)']
plt.close('all')
plt.figure(figsize=(15,9.25), tight_layout=True)
plt.suptitle('Joint Kinematics', fontsize=21, fontweight='bold')
for ii,i in enumerate(jointLabel):
    print('kinematics', i)
    b = list()
    s = list()
    for j in subj:
        b.append(jointContra[i][j]['boot'].mean(axis=1).values)
        s.append(jointContra[i][j]['shoe'].mean(axis=1).values)
        # b.append(jointIpsi[i][j]['boot'].mean(axis=1).values)
        # s.append(jointIpsi[i][j]['shoe'].mean(axis=1).values)
        # b.append(np.mean((jointContra[i][j]['boot'].mean(axis=1).values, jointIpsi[i][j]['boot'].mean(axis=1).values), axis=0))
        # s.append(np.mean((jointContra[i][j]['shoe'].mean(axis=1).values, jointIpsi[i][j]['shoe'].mean(axis=1).values), axis=0))
        # plt.figure(j)
        # plt.plot(jointIpsi[i][j]['boot'].values, color='b')
        # plt.plot(jointIpsi[i][j]['shoe'].values, color='r')
        # plt.show()
    # plt.figure(i)
    # plt.plot(np.transpose(b), color='b')
    # plt.plot(np.transpose(s), color='r')
    # plt.show()
    spm = spm1d.stats.ttest_paired(b, s)
    spmi = spm.inference(alpha=alpha_P, two_tailed=tt)
    # plot
    ax = plt.subplot(int(len(jointLabel)/3), 3, ii + 1)
    default()
    annotate(spmi, thr=0.3)
    ax.set_xlabel('Stride (%)')
    ax.set_title(title[ii])
    ax.axvline(st, lw=1, color='r')
    ax.axvline(bt, lw=1, color='b')
    if ii in [0,3,6]:
        ax.set_ylabel('Angle (deg)')
    if ii == 2:
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

plt.savefig(os.path.join(parent, 'joint.png'), dpi=300, bbox_inches='tight')
# plt.show()
# 
# 
# 
# 
# 
# %%
bt = 35.52
st = 36
velIpsi = pd.read_pickle(os.path.join(parent, 'veli.zip'))
velContra = pd.read_pickle(os.path.join(parent, 'velc.zip'))
velLabel = ['hip_flexion', 'hip_adduction', 'hip_rotation', 'knee_angle', 'ankle_angle', 'subtalar_angle'] #'lumbar_extension', 'lumbar_bending', 'lumbar_rotation', 
title = ['Hip Flexion(+)', 'Hip Adduction(+)', 'Hip Internal Rotation(+)', 'Knee Flexion (+)', 'Ankle Dorsiflexion (+)', 'Subtalar Supination (+)']
plt.close('all')
plt.figure(figsize=(15,9.25), tight_layout=True)
plt.suptitle('Joint Angular Velocity', fontsize=21, fontweight='bold')
for ii,i in enumerate(velLabel):
    print('kinematics', i)
    b = list()
    s = list()
    for j in subj:
        b.append(velContra[i][j]['boot'].mean(axis=1).values)
        s.append(velContra[i][j]['shoe'].mean(axis=1).values)
        # b.append(velIpsi[i][j]['boot'].mean(axis=1).values)
        # s.append(velIpsi[i][j]['shoe'].mean(axis=1).values)
        # b.append(np.mean((velContra[i][j]['boot'].mean(axis=1).values, velIpsi[i][j]['boot'].mean(axis=1).values), axis=0))
        # s.append(np.mean((velContra[i][j]['shoe'].mean(axis=1).values, velIpsi[i][j]['shoe'].mean(axis=1).values), axis=0))
        # plt.figure(j)
        # plt.plot(velIpsi[i][j]['boot'].values, color='b')
        # plt.plot(velIpsi[i][j]['shoe'].values, color='r')
        # plt.show()
    # plt.figure(i)
    # plt.plot(np.transpose(b), color='b')
    # plt.plot(np.transpose(s), color='r')
    # plt.show()
    spm = spm1d.stats.ttest_paired(b, s)
    spmi = spm.inference(alpha=alpha_P, two_tailed=tt)
    # plot
    ax = plt.subplot(int(len(velLabel)/3), 3, ii + 1)
    default()
    annotate(spmi, thr=0.3)
    ax.set_xlabel('Stride (%)')
    ax.set_title(title[ii])
    ax.axvline(st, lw=1, color='r')
    ax.axvline(bt, lw=1, color='b')
    if ii in [0,3,6]:
        ax.set_ylabel('Velocity (deg/s)')
    if ii == 2:
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

plt.savefig(os.path.join(parent, 'vel.png'), dpi=300, bbox_inches='tight')
# plt.show()
# 
# 
# 
# 
# 
# %%
bodyIpsi = pd.read_pickle(os.path.join(parent, 'bodyi.zip'))
bodyContra = pd.read_pickle(os.path.join(parent, 'bodyc.zip'))
bodyLabel = ['torso_Ox', 'torso_Oy', 'torso_Oz','pelvis_Ox', 'pelvis_Oy', 'pelvis_Oz', 'femur_Ox','femur_Oy','femur_Oz','tibia_Ox','tibia_Oy','tibia_Oz','calcn_Ox','calcn_Oy','calcn_Oz'] 
plt.close('all')
plt.figure(figsize=(15,20), tight_layout=True)
plt.suptitle('body Kinematics', fontsize=21, fontweight='bold')
for ii,i in enumerate(bodyLabel):
    print('Bodies', i)
    b = list()
    s = list()
    for j in subj:
        b.append(bodyContra[i][j]['boot'].mean(axis=1).values)
        s.append(bodyContra[i][j]['shoe'].mean(axis=1).values)
        # b.append(bodyIpsi[i][j]['boot'].mean(axis=1).values)
        # s.append(bodyIpsi[i][j]['shoe'].mean(axis=1).values)
        # b.append(np.mean((bodyContra[i][j]['boot'].mean(axis=1).values, bodyIpsi[i][j]['boot'].mean(axis=1).values), axis=0))
        # s.append(np.mean((bodyContra[i][j]['shoe'].mean(axis=1).values, bodyIpsi[i][j]['shoe'].mean(axis=1).values), axis=0))
    spm = spm1d.stats.ttest_paired(b, s)
    spmi = spm.inference(alpha=alpha_P, two_tailed=tt)
    # plot
    ax = plt.subplot(int(len(bodyLabel)/3), 3, ii + 1)
    default()
    annotate(spmi, thr=0.3)
    ax.set_xlabel('Stride (%)')
    ax.set_title(i)
    ax.axvline(st, lw=1, color='r')
    ax.axvline(bt, lw=1, color='b')
    if ii in [0,3,6]:
        ax.set_ylabel('Angle (deg)')
    if ii == 2:
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

plt.savefig(os.path.join(parent, 'body.png'), dpi=300, bbox_inches='tight')
# 
# 
# 
# 
# 
# %%
moment = pd.read_pickle(os.path.join(parent, 'moment.zip'))
momentLabel = ['hip_flexion', 'hip_adduction', 'hip_rotation', 'knee_angle', 'knee_add', 'knee_rot', 'ankle_angle', 'subtalar_angle']# 'lumbar_extension', 'lumbar_bending', 'lumbar_rotation',
title = ['Hip Flexor(+)', 'Hip Adductor(+)', 'Hip Internal Rotator(+)', 'Knee Flexor (+)', 'Knee Adductor (+)', 'Knee Internal Rotator (+)', 'Ankle Dorsiflexor (+)', 'Subtalar Supinator (+)']
plt.close('all')
plt.figure(figsize=(15,13.5), tight_layout=True)
plt.suptitle('Joint Moment', fontsize=21, fontweight='bold')
for ii,i in enumerate(momentLabel):
    print('moment', i)
    b = list()
    s = list()
    for j in subj:
        b.append(moment[i][j]['boot'].mean(axis=1).values / (demo['mass'].loc[j]))
        s.append(moment[i][j]['shoe'].mean(axis=1).values / (demo['mass'].loc[j]))
        # plt.figure(j)
        # plt.plot(moment[i][j]['boot'].values, color='b')
        # plt.plot(moment[i][j]['shoe'].values, color='r')
        # plt.show()
    # plt.figure(i)
    # plt.plot(np.transpose(b), color='b', lw=1)
    # plt.plot(np.transpose(s), color='r', lw=1)
    # plt.show()
    spm = spm1d.stats.ttest_paired(b, s)
    spmi = spm.inference(alpha=alpha_P, two_tailed=tt)
    # plot
    ax = plt.subplot(3, 3, ii + 1)
    default()
    annotate(spmi, thr=0.3)
    ax.set_xlabel('Stance (%)')
    ax.set_title(title[ii])
    if ii in [0,3,6]:
        ax.set_ylabel('N.m [%BM]')
    if ii == 2:
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

plt.savefig(os.path.join(parent, 'moment.png'), dpi=300, bbox_inches='tight')
# 
# 
# 
# 
# 
# %%
power = pd.read_pickle(os.path.join(parent, 'power.zip'))
plt.close('all')
plt.figure(figsize=(15,9.25), tight_layout=True)
plt.suptitle('Joint Power', fontsize=21, fontweight='bold')
for ii,i in enumerate(['hip_flexion', 'knee', 'ankle', 'hip_adduction']):
    print('power', i)
    b = list()
    s = list()
    for j in subj:
        b.append(power[i][j]['boot'].mean(axis=1).values / (demo['mass'].loc[j]))
        s.append(power[i][j]['shoe'].mean(axis=1).values / (demo['mass'].loc[j]))
        # plt.figure(j)
        # plt.plot(power[i][j]['boot'].values, color='b')
        # plt.plot(power[i][j]['shoe'].values, color='r')
        # plt.show()
    spm = spm1d.stats.ttest_paired(b, s)
    spmi = spm.inference(alpha=alpha_P, two_tailed=tt)
    # plot
    ax = plt.subplot(2, 3, ii + 1)
    default()
    annotate(spmi, thr=0.3)
    ax.set_xlabel('Stance (%)')
    ax.set_title(i)
    if ii in [0,3,6]:
        ax.set_ylabel('Watts [%BM]')
    if ii == 2:
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    del spm, spmi
# plt.show(block=False)
plt.savefig(os.path.join(parent, 'power.png'), dpi=300, bbox_inches='tight')
# 
# 
# 
# 
# %%
TD = pd.read_pickle(os.path.join(parent, 'TD.zip'))
tdLabel = ['velocity', 'stance', 'swing', 'flight', 'step', 'stride', 'stepWidth', 'stepLength', 'strideLength', 'flightLength','strideHeight']
result = dict()

for i in tdLabel:
    b,s = list(),list()
    for j in subj:
        side = demo['side'].loc[j][0]
        if side=='r': side2='l'
        elif side =='l': side2=='r'
        if i != 'velocity': i2 = side2.upper()+i
        else: i2 = 'velocity'
        if i2.endswith('Width') or i2.endswith('Length') or i2.endswith('Height'):
            b.append(np.mean(TD[i2][j]['boot'].values))# / (demo['LLL'].loc[j]*100))
            s.append(np.mean(TD[i2][j]['shoe'].values))# / (demo['LLL'].loc[j]*100))
        else:
            b.append(np.mean(TD[i2][j]['boot'].values)*1000)
            s.append(np.mean(TD[i2][j]['shoe'].values)*1000)
    # print('boot', stats.shapiro(np.array(b)))
    # print('shoe', stats.shapiro(np.array(s)))
    result[i] = [round(np.mean(b),2), round(np.std(b),2), round(np.mean(s),2), round(np.std(s),2), stats.ttest_rel(b, s)]
result
100 - result['swing'][0]*100 / result['stride'][0]
100 - result['swing'][2]*100 / result['stride'][2]
np.mean(60/np.array(b))
np.std(60/np.array(b))
np.mean(60/np.array(s))
np.std(60/np.array(s))
stats.ttest_rel(60/np.array(b), 60/np.array(s))
