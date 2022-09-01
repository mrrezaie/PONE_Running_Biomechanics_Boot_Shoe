import numpy as np
import pandas as pd
import opensim as osim
import sys, os
sys.path.append('D:\\Academic\\Codes\\Python\\MRR')
from MRR import writeOsimExp, writeExtLoad, getFile, osimOperation, osimCoordination, HarringtonHJC, find_ranges
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

parent = 'E:\\MMMMM'
demo = pd.read_csv("E:\\MMMMM\\demographics.csv", index_col=0)
fc_force = 50
order = 4
mag_force = 7 # threshold for vertical force (N)
dur_force = 0.15 # threshold for minimum contact period (s)

i = 's13'
j = 'boot'
# k = 'T2'
# for i in subj:
#     for j in ['boot', 'shoe']:
        # ###############################################################################
        # static markers
        # ###############################################################################
		direc = os.path.join(parent, i, j, 'static')
		os.chdir(direc)
		# print(os.getcwd())
		for k in os.listdir():
			if k.endswith('.c3d'):
				fileName = k
		lab = fileName.split(';')[1][:-4]
		c3dAd = osim.C3DFileAdapter()
		c3d = c3dAd.read(fileName)
		markerVec3 = c3dAd.getMarkersTable(c3d)
		osimCoordination(markerVec3, lab)
		markerLabel = list(markerVec3.getColumnLabels())
		n_marker = int(markerVec3.getNumColumns())
		fs_marker = round(float(markerVec3.getTableMetaDataAsString('DataRate')))
		r_marker = int(markerVec3.getNumRows())
		unit_marker = markerVec3.getTableMetaDataAsString('Units')
		marker = markerVec3.flatten(['_x', '_y', '_z'])
		marker = marker.getMatrix().to_numpy()
        # virtual markers
		RASIS = marker[:, 3*markerLabel.index('RASI'):3*markerLabel.index('RASI')+3]
		LASIS = marker[:, 3*markerLabel.index('LASI'):3*markerLabel.index('LASI')+3]
		RPSIS = marker[:, 3*markerLabel.index('RPSI'):3*markerLabel.index('RPSI')+3]
		LPSIS = marker[:, 3*markerLabel.index('LPSI'):3*markerLabel.index('LPSI')+3]
		RHJC, LHJC = HarringtonHJC(RASIS, LASIS, RPSIS, LPSIS)
		RKJC = (marker[:, 3*markerLabel.index('RLFC'): 3*markerLabel.index('RLFC')+3] +
				marker[:, 3*markerLabel.index('RMFC'): 3*markerLabel.index('RMFC')+3]) /2
		LKJC = (marker[:, 3*markerLabel.index('LLFC'): 3*markerLabel.index('LLFC')+3] +
				marker[:, 3*markerLabel.index('LMFC'): 3*markerLabel.index('LMFC')+3]) /2
		RAJC = (marker[:, 3*markerLabel.index('RLMAL'): 3*markerLabel.index('RLMAL')+3] +
				marker[:, 3*markerLabel.index('RMMAL'): 3*markerLabel.index('RMMAL')+3]) /2
		LAJC = (marker[:, 3*markerLabel.index('LLMAL'): 3*markerLabel.index('LLMAL')+3] +
				marker[:, 3*markerLabel.index('LMMAL'): 3*markerLabel.index('LMMAL')+3]) /2
		RFF  = (marker[:, 3*markerLabel.index('RTOE'): 3*markerLabel.index('RTOE')+3] +
				marker[:, 3*markerLabel.index('RMT5'): 3*markerLabel.index('RMT5')+3]) /2
		LFF  = (marker[:, 3*markerLabel.index('LTOE'): 3*markerLabel.index('LTOE')+3] +
				marker[:, 3*markerLabel.index('LMT5'): 3*markerLabel.index('LMT5')+3]) /2
		# RTH = ( marker[:, 3*markerLabel.index('RTH1'): 3*markerLabel.index('RTH1')+3] +
		# 		marker[:, 3*markerLabel.index('RTH2'): 3*markerLabel.index('RTH2')+3] +
		# 		marker[:, 3*markerLabel.index('RTH3'): 3*markerLabel.index('RTH3')+3] +
		# 		marker[:, 3*markerLabel.index('RTH4'): 3*markerLabel.index('RTH4')+3]) /4
		# LTH = ( marker[:, 3*markerLabel.index('LTH1'): 3*markerLabel.index('LTH1')+3] +
		# 		marker[:, 3*markerLabel.index('LTH2'): 3*markerLabel.index('LTH2')+3] +
		# 		marker[:, 3*markerLabel.index('LTH3'): 3*markerLabel.index('LTH3')+3] +
		# 		marker[:, 3*markerLabel.index('LTH4'): 3*markerLabel.index('LTH4')+3]) /4
		# RTB = ( marker[:, 3*markerLabel.index('RTB1'): 3*markerLabel.index('RTB1')+3] +
		# 		marker[:, 3*markerLabel.index('RTB2'): 3*markerLabel.index('RTB2')+3] +
		# 		marker[:, 3*markerLabel.index('RTB3'): 3*markerLabel.index('RTB3')+3] +
		# 		marker[:, 3*markerLabel.index('RTB4'): 3*markerLabel.index('RTB4')+3]) /4
		# LTB = ( marker[:, 3*markerLabel.index('LTB1'): 3*markerLabel.index('LTB1')+3] +
		# 		marker[:, 3*markerLabel.index('LTB2'): 3*markerLabel.index('LTB2')+3] +
		# 		marker[:, 3*markerLabel.index('LTB3'): 3*markerLabel.index('LTB3')+3] +
		# 		marker[:, 3*markerLabel.index('LTB4'): 3*markerLabel.index('LTB4')+3]) /4
		midASIS = ( marker[:, 3*markerLabel.index('RASI'): 3*markerLabel.index('RASI')+3] +
					marker[:, 3*markerLabel.index('LASI'): 3*markerLabel.index('LASI')+3]) /2
		midPSIS = ( marker[:, 3*markerLabel.index('RPSI'): 3*markerLabel.index('RPSI')+3] +
					marker[:, 3*markerLabel.index('LPSI'): 3*markerLabel.index('LPSI')+3]) /2
		# midPelvis = (marker[:, 3*markerLabel.index('RASI'): 3*markerLabel.index('RASI')+3] +
		# 			marker[:, 3*markerLabel.index('LASI'): 3*markerLabel.index('LASI')+3] +
		# 			marker[:, 3*markerLabel.index('RPSI'): 3*markerLabel.index('RPSI')+3] +
		# 			marker[:, 3*markerLabel.index('LPSI'): 3*markerLabel.index('LPSI')+3]) /4
		ACR = ( marker[:, 3*markerLabel.index('RACR'): 3*markerLabel.index('RACR')+3] +
				marker[:, 3*markerLabel.index('LACR'): 3*markerLabel.index('LACR')+3]) /2
		markers = np.hstack((marker, midASIS, midPSIS, RHJC, LHJC, RKJC, LKJC, RAJC, LAJC, RFF, LFF, ACR))
		new = ['midASIS', 'midPSIS', 'RHJC', 'LHJC', 'RKJC', 'LKJC', 'RAJC', 'LAJC', 'RFF', 'LFF', 'ACR']
		for n in new: markerLabel.append(n)
		writeOsimExp(markers, os.path.join(direc, i+'_'+j+'_static.trc'), label=markerLabel, fs=fs_marker, inputName=fileName)
		if j == 'shoe':
            if 'LLL' not in demo.columns:
                newDemo = True
			    demo['LLL'].loc[i] = np.mean((np.linalg.norm(RHJC-RAJC, ord=2, axis=1), np.linalg.norm(LHJC-LAJC, ord=2, axis=1))) / 1000
        # 
        # 
        # 
        for k in ['T1', 'T2', 'T3', 'T4']:
            # ###############################################################################
            # dynamic
            # ###############################################################################
            direc = os.path.join(parent, i, j, k, 'exp')
            os.chdir(direc)
            for a in os.listdir():
                if a.endswith('.c3d'):
                    fileName = a
            names = fileName[:-4]
            names = names.split(';')
            lab = names[1]
            if names[2].startswith('r'): 
                foot = 'right'
            elif names[2].startswith('l'): 
                foot = 'left'
            fp = int(names[2][1])
            c3dAd = osim.C3DFileAdapter()
            c3dAd.setLocationForForceExpression(1)
            if c3dAd.getLocationForForceExpression()!=1: 
                raise RuntimeError('\nlocation for force expression is not COP')
            c3d = c3dAd.read(fileName)
            # 
            # MARKERS
            markerVec3 = c3dAd.getMarkersTable(c3d)
            osimCoordination(markerVec3, lab)
            markerLabel = list(markerVec3.getColumnLabels())
            # for i in markerLabel:
            #     if i.startswith('*'):
            #         markerVec3.removeColumn(i)
            #         markerLabel.remove(i)
            n_marker = int(markerVec3.getNumColumns())
            fs_marker = round(float(markerVec3.getTableMetaDataAsString('DataRate')))
            r_marker = int(markerVec3.getNumRows())
            unit_marker = markerVec3.getTableMetaDataAsString('Units')
            marker = markerVec3.flatten(['_x', '_y', '_z'])
            marker = marker.getMatrix().to_numpy()
            # RTH = ( marker[:, 3*markerLabel.index('RTH1'): 3*markerLabel.index('RTH1')+3] +
            #         marker[:, 3*markerLabel.index('RTH2'): 3*markerLabel.index('RTH2')+3] +
            #         marker[:, 3*markerLabel.index('RTH3'): 3*markerLabel.index('RTH3')+3] +
            #         marker[:, 3*markerLabel.index('RTH4'): 3*markerLabel.index('RTH4')+3]) /4
            # LTH = ( marker[:, 3*markerLabel.index('LTH1'): 3*markerLabel.index('LTH1')+3] +
            #         marker[:, 3*markerLabel.index('LTH2'): 3*markerLabel.index('LTH2')+3] +
            #         marker[:, 3*markerLabel.index('LTH3'): 3*markerLabel.index('LTH3')+3] +
            #         marker[:, 3*markerLabel.index('LTH4'): 3*markerLabel.index('LTH4')+3]) /4
            # RTB = ( marker[:, 3*markerLabel.index('RTB1'): 3*markerLabel.index('RTB1')+3] +
            #         marker[:, 3*markerLabel.index('RTB2'): 3*markerLabel.index('RTB2')+3] +
            #         marker[:, 3*markerLabel.index('RTB3'): 3*markerLabel.index('RTB3')+3] +
            #         marker[:, 3*markerLabel.index('RTB4'): 3*markerLabel.index('RTB4')+3]) /4
            # LTB = ( marker[:, 3*markerLabel.index('LTB1'): 3*markerLabel.index('LTB1')+3] +
            #         marker[:, 3*markerLabel.index('LTB2'): 3*markerLabel.index('LTB2')+3] +
            #         marker[:, 3*markerLabel.index('LTB3'): 3*markerLabel.index('LTB3')+3] +
            #         marker[:, 3*markerLabel.index('LTB4'): 3*markerLabel.index('LTB4')+3]) /4
            midASIS = ( marker[:, 3*markerLabel.index('RASI'): 3*markerLabel.index('RASI')+3] +
                        marker[:, 3*markerLabel.index('LASI'): 3*markerLabel.index('LASI')+3]) /2
            midPSIS = ( marker[:, 3*markerLabel.index('RPSI'): 3*markerLabel.index('RPSI')+3] +
                        marker[:, 3*markerLabel.index('LPSI'): 3*markerLabel.index('LPSI')+3]) /2
            RFF = ( marker[:, 3*markerLabel.index('RTOE'): 3*markerLabel.index('RTOE')+3] +
                    marker[:, 3*markerLabel.index('RMT5'): 3*markerLabel.index('RMT5')+3]) /2
            LFF = ( marker[:, 3*markerLabel.index('LTOE'): 3*markerLabel.index('LTOE')+3] +
                    marker[:, 3*markerLabel.index('LMT5'): 3*markerLabel.index('LMT5')+3]) /2
            markers = np.hstack((marker, midASIS, midPSIS, RFF, LFF))
            new =  ['midASIS', 'midPSIS', 'RFF', 'LFF']
            for n in new: markerLabel.append(n)
            writeOsimExp(markers, os.path.join(direc, i+'_'+j+'_'+k+'_markers.trc'), label=markerLabel, fs=fs_marker, inputName=fileName)
            # 
            # force data
            forceVec3 = c3dAd.getForcesTable(c3d)
            n_fp = int(forceVec3.getNumColumns()/3)
            fs_force = int(np.double(forceVec3.getTableMetaDataAsString('DataRate')))
            r_force = int(forceVec3.getNumRows())
            unit_force = list(forceVec3.getDependentsMetaDataString('units'))
            osimCoordination(forceVec3, lab)
            force = forceVec3.flatten(['_x', '_y', '_z'])
            forceLabel = list(force.getColumnLabels())
            for a in forceLabel:
                if a.startswith('p'):
                    osimOperation(force, a, '/', 1000)
                elif a.startswith('m'):
                    osimOperation(force, a, '/', 1000)
            force = force.getMatrix().to_numpy()
            # Smoothing parameters for Butterworth low-pass filter
            b, a = butter(order, 2*fc_force/fs_force, 'lowpass', output='ba')
            forceData = np.zeros((r_force,9))
            r = find_ranges(np.where(force[:,9*(fp-1)+1] >= mag_force)[0], fs_force*dur_force)[0]
            print(i, j, k, f'fp{fp}\t{r[0]/fs_force}\t{r[1]/fs_force}')
            if np.isnan(marker).any():
                print('    contains nan\t\t')
            for c in range(9):
                forceData[r[0]:r[1]+1, c] = filtfilt(b,a, force[r[0]:r[1]+1, 9*(fp-1)+c], padlen=100)
            forceLabel = list()
            xyz = ['x', 'y', 'z']
            for b in range(3): forceLabel.append(f'ground_force_1_v{xyz[b]}')
            for b in range(3): forceLabel.append(f'ground_force_1_p{xyz[b]}')
            for b in range(3): forceLabel.append(f'ground_torque_1_{xyz[b]}')
            writeOsimExp(forceData, os.path.join(direc, i+'_'+j+'_'+k+'_forces.mot'), label=forceLabel, fs=fs_force, inputName=fileName)
            # 
            # external loads
            exl = osim.ExternalLoads()
            exl.setName('ExtLoad')
            exl.setDataFileName(os.path.join(direc, i+'_'+j+'_'+k+'_forces.mot'))
            extForce = osim.ExternalForce()
            extForce.setName('FP1')
            extForce.set_applied_to_body('calcn_'+foot[0])
            extForce.set_force_expressed_in_body('ground')
            extForce.set_point_expressed_in_body('ground')
            extForce.set_force_identifier('ground_force_1_v')
            extForce.set_point_identifier('ground_force_1_p')
            extForce.set_torque_identifier('ground_torque_1_')
            extForce.set_data_source_name(names[0])
            exl.cloneAndAppend(extForce)
            exl.printToXML(os.path.join(parent, i, j, k, f'{i}_{j}_{k}_setupExtLoads.xml'))
# write new demographics data contains lower limb length (LLL)
if newDemo: 
    demo.to_csv(os.path.join(parent,'demographics.csv'), float_format='%0.3f')

            
