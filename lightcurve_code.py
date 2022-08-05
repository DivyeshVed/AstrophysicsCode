import sys
from astropy.io import fits
import matplotlib.pyplot as plt
#type 128lc_a
spectrum = sys.argv[1]
path = "/Users/erinhorbacz/Downloads/Research/testData/P10408/10408-01-25-00/"
pathfile = '%s%s'%(path, spectrum)
rate = []
time = []
#extract data from fits file
with fits.open(pathfile) as file:
    print("file open")
    data = file[1].data
    for line in data:
        time.append(line[0])
        rate.append(line[1])
#plot light curve
plt.loglog(time, rate)
plt.title("Light Curve")
plt.xlabel("Time")
plt.ylabel("Rate")
plt.savefig('%s_lightcurve.png'%(spectrum))
print("closing the file...")
plt.close()
print("finished creating light curve")
