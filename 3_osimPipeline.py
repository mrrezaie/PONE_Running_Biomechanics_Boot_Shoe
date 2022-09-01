import numpy as np
import pandas as pd
import opensim as osim
osim.Logger.setLevel(6) # off
from subprocess import call
import sys, os, csv
# add opensim dll files directory to system path
os.environ["PATH"] += os.pathsep + 'F:\\OpenSim 4.3\\bin'

scaleExec=True
ikExec=True
idExec=True
analyseExec = True

# subjects
subj = ['s%02i' %i for i in range(1,21)]
# remove specific subjects
for i in ['s05', 's06']:
    try:
        del subj[subj.index(i)]
    except:
        pass

parent = 'E:\\MMMMM'
# demographics data
demo = pd.read_csv(os.path.join(parent, 'demographics.csv'), index_col=0)
# boot\shoe mass difference
dmass = 0.3 # kg

# i = 's13'
# j = 'boot'
# k = 'T1'
for i in subj:
    for j in ['boot', 'shoe']:
        if scaleExec:
    		direc = os.path.join(parent, i, j)
            # ###############################################################################
            # opensim scale tool
            # ###############################################################################
    		time_range = osim.ArrayDouble()
    		time_range.setitem(0, 0)
    		time_range.setitem(1, 10)
    		scale = osim.ScaleTool('E:\\MMMMM\\osim\\setupScaleDefault.xml')
    		scale.setPathToSubject('')
    		scale.setName(f'{i}_{j}')
    		scale.setSubjectMass(demo['mass'].loc[i])
    		scale.setSubjectHeight(1000*demo['height'].loc[i]) # in mm
    		scale.setSubjectAge(float(demo['age'].loc[i]))
    		scale.getGenericModelMaker().setModelFileName('E:\\MMMMM\\osim\\Raj2015.osim')
    		scale.getGenericModelMaker().setMarkerSetFileName('E:\\MMMMM\\osim\\markers.xml')
    		scale.getModelScaler().setMarkerFileName(os.path.join(direc, 'static', f'{i}_{j}_static.trc'))
    		scale.getModelScaler().setTimeRange(time_range)
    		scale.getMarkerPlacer().setMarkerFileName(os.path.join(direc, 'static', f'{i}_{j}_static.trc'))
    		scale.getMarkerPlacer().setTimeRange(time_range)
    		scale.getMarkerPlacer().setOutputMotionFileName(os.path.join(direc, 'static', f'{i}_{j}_static_position.mot'))
    		scale.getMarkerPlacer().setOutputModelFileName(os.path.join(direc, 'static', f'{i}_{j}_scaled.osim'))
    		scale.printToXML(os.path.join(direc, 'static', f'{i}_{j}_setupScale.xml'))
            # execute scale tool and create log
            try:
                f = open(os.path.join(direc, 'static', f'{i}_{j}_logScale.log'), 'w')
                call(['opensim-cmd', 'run-tool', os.path.join(direc, 'static', f'{i}_{j}_setupScale.xml')], stdout=f) #cwd=direc, 
                f.close()
            except:
                print(i, j, 'scale failed')
            # read the scale log to check the markers error 
    		with open(os.path.join(direc, 'static', f'{i}_{j}_logScale.log'), 'r') as f:
    			a = csv.reader(f, delimiter=',')
    			b = [ii for ii in a for jj in ii if '[info] Frame at' in jj]
    		print(i, j, '\t', b[0][1], b[0][2])
    		# add the boot/shoe mass difference to calcn segments
    		if j == 'boot':
    			model = osim.Model(os.path.join(direc, 'static', f'{i}_{j}_scaled.osim'))
    			mass = model.getBodySet().get('calcn_r').getMass() + dmass
    			model.getBodySet().get('calcn_r').setMass(mass)
                mass = model.getBodySet().get('calcn_l').getMass() + dmass
    			model.getBodySet().get('calcn_l').setMass(mass)
    			model.printToXML(os.path.join(direc, 'static', f'{i}_{j}_scaled.osim'))
        # 
        # 
        # 
        # loop for IK, ID, Anlayze 
        for k in ['T1', 'T2', 'T3', 'T4']:
            print(i,j,k)
            # directory to trials folder
            direc = os.path.join(parent, i, j, k)
            try: os.mkdir(os.path.join(direc, 'results'))
            except: pass
            # 
            # ###############################################################################
            # opensim IK tool
            # ###############################################################################
            if ikExec:
                ik = osim.InverseKinematicsTool(os.path.join(parent, 'osim', 'setupIKDefault.xml'))
                ik.setName(f'{i}_{j}_{k}')
                ik.setResultsDir('')
                ik.set_model_file(os.path.join(parent, i, j, 'static', f'{i}_{j}_scaled.osim'))
                ik.setStartTime(0)
                ik.setEndTime(100)
                ik.set_output_motion_file(os.path.join(direc, 'results',f'{i}_{j}_{k}_inverse_kinematics.mot'))
                ik.set_report_errors(True)
                ik.set_marker_file(os.path.join(direc, 'exp', f'{i}_{j}_{k}_markers.trc'))
                ik.printToXML(os.path.join(direc, f'{i}_{j}_{k}_setupIK.xml'))
                # scale.run()
                # osim.Logger.setLevel(6) # off
                # execute IK tool and create log
                try:
                    f = open(os.path.join(direc, f'{i}_{j}_{k}_logIK.log'), 'w')
                    call(['opensim-cmd', 'run-tool', os.path.join(direc, f'{i}_{j}_{k}_setupIK.xml')], stdout=f) #cwd=direc, 
                    f.close()
                except:
                    print(i, j, k, 'ik failed')
            # 
            # ###############################################################################
            # opensim ID tool
            # ###############################################################################
            if idExec:
                ind = osim.InverseDynamicsTool('E:\\MMMMM\\osim\\setupIDDefault.xml')
                ind.setName(i+'_'+j+'_'+k)
                ind.setModelFileName(os.path.join(parent, i, j, 'static', f'{i}_{j}_scaled.osim'))
                ind.setStartTime(0)
                final = osim.Storage(os.path.join(direc, 'results', f'{i}_{j}_{k}_inverse_kinematics.mot')).getLastTime()
                ind.setEndTime(final)
                ind.setCoordinatesFileName(os.path.join(direc, 'results', f'{i}_{j}_{k}_inverse_kinematics.mot'))
                ind.setExternalLoadsFileName(os.path.join(direc, f'{i}_{j}_{k}_setupExtLoads.xml'))
                ind.setLowpassCutoffFrequency(20)
                ind.setResultsDir(os.path.join(direc, 'results'))
                ind.setOutputGenForceFileName(f'{i}_{j}_{k}_inverse_dynamics.sto')
                fexclude = osim.ArrayStr()
                fexclude.set(0, 'Muscles')
                fexclude.set(1, 'Actuators')
                ind.setExcludedForces(fexclude)
                # ind.set_joints_to_report_body_forces('All')
                # ind.set_output_body_forces_file(f'{i}_{j}_{k}_body_forces_at_joints.sto')
                ind.printToXML(os.path.join(direc, f'{i}_{j}_{k}_setupID.xml'))
                # execute ID tool and create log
                try:
                    f = open(os.path.join(direc, f'{i}_{j}_{k}_logID.log'), 'w')
                    call(['opensim-cmd', 'run-tool', os.path.join(direc, f'{i}_{j}_{k}_setupID.xml')], stdout=f) #cwd=direc, 
                    f.close()
                except:
                    print(i, j, k, 'id failed')
            # 
            # ###############################################################################
            # opensim Analyze tool
            # ###############################################################################
            if analyseExec:
                analyze = osim.AnalyzeTool()
                analyze.setName(i+'_'+j+'_'+k)
                analyze.setModelFilename(os.path.join(parent, i, j, 'static', f'{i}_{j}_scaled.osim'))
                analyze.setResultsDir(os.path.join(direc, 'results'))
                analyze.setCoordinatesFileName(os.path.join(direc, 'results', f'{i}_{j}_{k}_inverse_kinematics.mot'))
                analyze.setExternalLoadsFileName(os.path.join(direc, f'{i}_{j}_{k}_setupExtLoads.xml'))
                final = osim.Storage(os.path.join(direc, 'results', f'{i}_{j}_{k}_inverse_kinematics.mot')).getLastTime()
                analyze.setInitialTime(0)
                analyze.setFinalTime(final)
                analyze.setLowpassCutoffFrequency(20)
                analyze.setSolveForEquilibrium(False)
                # kinematics
                kin = osim.Kinematics()
                kin.setStartTime(0)
                kin.setEndTime(final)
                # body kinematics
                bkin = osim.BodyKinematics()
                bkin.setStartTime(0)
                bkin.setEndTime(final)
                analyze.getAnalysisSet().cloneAndAppend(kin)
                analyze.getAnalysisSet().cloneAndAppend(bkin)
                analyze.printToXML(os.path.join(direc, f'{i}_{j}_{k}_setupAnalyze.xml'))
                # execute analyze tool and create log
                try:
                    f = open(os.path.join(direc, f'{i}_{j}_{k}_logAnalyze.log'), 'w')
                    call(['opensim-cmd', 'run-tool', os.path.join(direc, f'{i}_{j}_{k}_setupAnalyze.xml')], stdout=f) #cwd=direc, 
                    f.close()
                except:
                    print(i, j, k, 'analyze failed')