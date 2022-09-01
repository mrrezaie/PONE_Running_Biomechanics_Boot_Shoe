import os
from shutil import move

folders = ['s%02i' % i for i in range(1,21)]
trials = ['T%i' %i for i in range(1,6)]
parent = 'E:\\MMMMM'

for i in folders:
    os.chdir(os.path.join(parent, i))
    path = os.getcwd()
    print(path)
    c3d = [j for j in os.listdir() if j.endswith('.c3d')]
    boot = [j for j in c3d if 'boot' in j]
    shoe = [j for j in c3d if 'shoe' in j]
    for j,T in zip(boot, trials):
        q = j[:-4]+'.qtm'
        if 'static' in j:
            try:
                move(path+'\\'+j, path+'\\boot\\static')
                move(path+'\\'+q, path+'\\boot\\static')
            except: pass
        else:
            try:
                move(path+'\\'+j, path+'\\boot\\'+T+'\\exp')
                move(path+'\\'+q, path+'\\boot\\'+T+'\\exp')
            except: pass
    for j,T in zip(shoe, trials):
        q = j[:-4]+'.qtm'
        if 'static' in j:
            try:
                move(path+'\\'+j, path+'\\shoe\\static')
                move(path+'\\'+q, path+'\\shoe\\static')
            except: pass
        else:
            try:
                move(path+'\\'+j, path+'\\shoe\\'+T+'\\exp')
                move(path+'\\'+q, path+'\\shoe\\'+T+'\\exp')
            except: pass

