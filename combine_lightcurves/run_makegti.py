import subprocess

pathname = "/Users/divyeshved/Desktop/visits/40017-02-06-00"
modetype = '1'

with open('%s/visit2.txt'%pathname, 'r') as f:
    for i, line in enumerate(f):
        outputname = 'v2'
        inputname = line.strip()
        print(inputname)
        subprocess.call(['./makegti2.sh' , pathname, modetype, inputname, outputname])