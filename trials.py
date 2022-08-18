import glob

path = '/Users/rohanpunamiya/Desktop/Data/P93071/93071-04-01-00/qpo_fit'
for p in glob.glob('*.eps'):
    print(p)