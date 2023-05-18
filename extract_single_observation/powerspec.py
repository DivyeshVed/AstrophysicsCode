from astropy.io import fits
import numpy
import scipy
import scipy.fftpack
import pandas as pd

###Import data from fits file and save light curve as text file
def readfits(infile):
    lc = fits.open('%s.lc'%infile)
    scidata = lc[1].data
    lc_len=(scidata.shape[0])
    print("Length is",lc_len)
    obsbegin_time=scidata[0][0]
    dt = scidata[1][0]-scidata[0][0]

    print(dt)
    tim=[]
    count_s=[]
    count_bin=[]
    for i in range(lc_len):
        fracexp = scidata[i][3]
        tim.append(scidata[i][0] - obsbegin_time)
        count_s.append(scidata[i][1] * fracexp)
        count_bin.append(scidata[i][1] * dt * fracexp) #Caution, multiplying by dt converts from counts/s to counts/bin!!
    lc.close()

    data=numpy.column_stack((tim,count_s,count_bin))
    numpy.savetxt('%s.txt'%infile,data,delimiter='\t',header='TIME;COUNT/SEC;COUNT/BIN')

###Generate power spectrum of lightcurve with Leahy normalisation
def powerspec(infile,seglength,norm='leahy'):
    f1=[]
    ####read lightcurve
    tim,term=numpy.genfromtxt('%s.txt'%infile,delimiter='\t', dtype=None, unpack=True,usecols =(0,2))
    lc_length = len(term)
    time_step = tim[1]-tim[0]

    ####Segment time series
    if seglength > lc_length:
        seglength = lc_length
        num_segments = 1
    else:
        num_segments = int(lc_length/seglength)
    segnum=numpy.arange(0,num_segments)
    power_spec = numpy.zeros([seglength])

    ####Calculate Fourier Frequencies
    seg_freq = numpy.fft.fftfreq(seglength, d=time_step)
    positive = seg_freq >= 0

    for s in segnum:
        start = s*seglength
        end = start+seglength
        current_term = term[start:end]
        current_time = tim[start:end]

        ####FFT of segment
        seg_ps = scipy.fftpack.fft(current_term)
        N_ph = sum(current_term) #number of photons
        t_seg = seglength * time_step #length of segment in seconds
        power_spec_current = numpy.absolute(seg_ps * numpy.conj(seg_ps))

        ####Normalise, Leahy
        if norm == 'leahy':
            power_spec_current = power_spec_current*2.0/N_ph

        ####Normalize, Fractional rms
        elif norm == 'frac_rms':
            power_spec_current = power_spec_current*2.0*t_seg/(N_ph**2.0)

        ####Normalize, absolute rms
        elif norm == 'abs_rms':
            mean_rate = N_ph/t_seg
            power_spec_current = power_spec_current*2.0*mean_rate/N_ph

        power_spec += power_spec_current

    ####Average power spectra
    power_spec = (power_spec)/num_segments

    ####Get error on power
    power_err = power_spec/numpy.sqrt(num_segments)

    ####Return results
    return seg_freq[positive], power_spec[positive], power_err[positive]

#### Code to logarithimically rebin power spectrum
def log_rebin(frequency, power, power_error, rebin_fac=1.02):
    '''
    Returns logarithmically binned power spectra, where each bin is rebin_fac times bigger than the previous.
    rebin_fac must be greater than 1.

    '''
    freq_bins = [frequency[0], frequency[1]] #first bin
    df = frequency[1] - frequency[0] #size of initial frequency bin

    #### Computing the frequencies of log bins
    max_freq = frequency[-1]
    while freq_bins[-1] <= max_freq:
        freq_bins.append(freq_bins[-1] + (df * rebin_fac))
        df = freq_bins[-1] - freq_bins[-2]


    #### Make into pandas dataframe for easy subsetting and calculation of values
    powerspec_data = pd.DataFrame({'FREQ':frequency , 'POWER': power, 'POWER_ERR': power_error}, columns=['FREQ', 'POWER', 'POWER_ERR'])

    #### Create empty lists for output
    rebin_freq=[]
    rebin_power=[]
    rebin_power_err=[]
    rebin_fmin=[]
    rebin_fmax=[]

    #### Subset the data so that each iteration gets the relevant (new) bin.
    for i in range(len(freq_bins)-1):
        fmin = freq_bins[i]
        rebin_fmin.append(fmin)
        fmax = freq_bins[i+1]
        rebin_fmax.append(fmax)

        data_subset = powerspec_data[(powerspec_data['FREQ'] < fmax) & (powerspec_data['FREQ'] >= fmin)]

        #### Compute the mean value of the frequency in each of the new log bins
        rebin_freq.append(data_subset['FREQ'].mean())

        #### Compute the mean value of the power in each of the new log bins
        rebin_power.append(data_subset['POWER'].mean())

        #### Compute the mean value of the power error in each of the new log bins using std error prop.
        rebin_power_err.append(numpy.sqrt(numpy.sum(data_subset['POWER_ERR']**2.0)/len(data_subset['POWER_ERR'])))


    return rebin_fmin, rebin_fmax, rebin_freq, rebin_power, rebin_power_err


#### Code to calculate the QPO rms (with error)
def qpo_rms(freq, lc, lc_err, sigma, sigma_err, ln, ln_err, df):
    ''' Computes the integral of the QPO Lorentzian, and returns its rms along with the error
    Lorentzian profile is defined in the same way as XSPEC, which is use for the fitting routine.
    '''
    l = []
    l_err = []
    for i in range(len(freq)):
        num = ln * (sigma / (2.0 * numpy.pi))
        den = (freq[i] - lc)**2.0 + (sigma / 2.0)**2.0
        loren = num/den
        l.append(loren * df)

        #### calculating the error
        err_num = numpy.sqrt(((ln_err / ln)**2.0 )+ ((sigma_err / sigma)**2.0)) * num
        err_den = numpy.sqrt(((2.0*lc_err*(freq[i]-lc))**2.0) + ((sigma_err*sigma/2.0)**2.0))
        err_total = numpy.sqrt(((err_num/ num)**2.0) + ((err_den / den)**2.0)) * loren
        l_err.append(err_total * df)
        #print(l[i], l_err[i], l_err[i]/l[i])

    #Calculate the integral, which gives the rms
    I = numpy.sqrt(numpy.sum(numpy.array(l)))

    #Calculate the error on the integral
    l_err = numpy.array(l_err)
    l_err_sq = l_err ** 2.0
    l_err_total = numpy.sqrt(numpy.sum(l_err_sq))

    I_err = I * 0.5 * (numpy.sqrt(numpy.sum(l_err_sq))) / numpy.sum(numpy.array(l))

    #print(numpy.sum(numpy.array(l)), l_err_total, l_err_total/numpy.sum(numpy.array(l)))
    #print(I, I_err, I_err/I)
    return I, I_err


###Calculate the cross spectrum and the phase lag of two lightcurves
def phaselag(infile1, infile2, seglength=2048):
    ''' Calculates the cross spectrum of two light curves, and returns the frequency, cross spectrum
        and the phase lags as numpy arrays
    '''

    ####read lightcurve
    tim1,term1=numpy.genfromtxt('%s.txt'%infile1,delimiter='\t', dtype=None, unpack=True,usecols =(0,2))
    tim2,term2=numpy.genfromtxt('%s.txt'%infile2,delimiter='\t', dtype=None, unpack=True,usecols =(0,2))
    lc_length = len(term1)
    time_step = tim1[1]-tim1[0]

    ####Segment time series
    if seglength > lc_length:
        seglength = lc_length
        num_segments = 1
    else:
        num_segments = int(lc_length/seglength)
    segnum=numpy.arange(0,num_segments)
    cross_spec = numpy.zeros([seglength], dtype=numpy.complex_)

    ####Calculate Fourier Frequencies
    seg_freq = numpy.fft.fftfreq(seglength, d=time_step)
    positive = seg_freq >= 0

    for s in segnum:
        start = s*seglength
        end = start+seglength
        current_term1 = term1[start:end]
        current_term2 = term2[start:end]
        current_time = tim1[start:end]

        ####FFT of segment
        fft1 = scipy.fftpack.fft(current_term1)
        fft2 = scipy.fftpack.fft(current_term2)
        #N_ph = sum(current_term) #number of photons
        #t_seg = seglength * time_step #length of segment in seconds
        cross_spec_current = fft1 * numpy.conj(fft2)

        cross_spec += cross_spec_current

    ####Average cross spectra
    cross_spec = (cross_spec)/num_segments

    #### Normalise cross spectra
    cross_spec = cross_spec / (numpy.mean(term1) * numpy.mean(term2))

    #### Calculate phase lag
    phase_lag = numpy.angle(cross_spec) / (2.0 * numpy.pi)

    ####Return results
    return seg_freq[positive], cross_spec[positive], phase_lag[positive]

#### Code to logarithimically rebin cross spectra
def log_rebin_phase(frequency, cross, rebin_fac=1.02):
    '''
    Code to logarithmically bin cross spectra, where each bin is rebin_fac times bigger than the previous.
    rebin_fac must be greater than 1.

    Returns Binned phase lags along with errors

    '''
    freq_bins = [frequency[0], frequency[1]] #first bin
    df = frequency[1] - frequency[0] #size of initial frequency bin

    #### Computing the frequencies of log bins
    max_freq = frequency[-1]
    while freq_bins[-1] <= max_freq:
        freq_bins.append(freq_bins[-1] + (df * rebin_fac))
        df = freq_bins[-1] - freq_bins[-2]


    #### Make into pandas dataframe for easy subsetting and calculation of values
    powerspec_data = pd.DataFrame({'FREQ':frequency , 'CROSS_SPEC': cross}, columns=['FREQ', 'CROSS_SPEC'])

    #### Create empty lists for output
    rebin_freq=[]
    rebin_cross=[]
    rebin_phase=[]
    rebin_phase_err=[]
    rebin_fmin=[]
    rebin_fmax=[]

    #### Subset the data so that each iteration gets the relevant (new) bin.
    for i in range(len(freq_bins)-1):
        fmin = freq_bins[i]
        rebin_fmin.append(fmin)
        fmax = freq_bins[i+1]
        rebin_fmax.append(fmax)

        data_subset = powerspec_data[(powerspec_data['FREQ'] < fmax) & (powerspec_data['FREQ'] >= fmin)]

        #### Compute the mean value of the frequency in each of the new log bins
        rebin_freq.append(data_subset['FREQ'].mean())

        #### Compute the mean value of the cross in each of the new log bins
        #### and calculate the avg.angle (i.e the avg phase lag) in each bin
        mean_val = data_subset['CROSS_SPEC'].mean()
        rebin_cross.append(mean_val)
        rebin_phase.append(numpy.angle(mean_val))

        #### Compute the error on phase lag as the stdev of the phase lags in each bin.
        rebin_phase_err.append(numpy.std(numpy.angle(data_subset['CROSS_SPEC'])))

    return rebin_fmin, rebin_fmax, rebin_freq, rebin_phase, rebin_phase_err
