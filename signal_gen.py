import numpy as np
from scipy.io import wavfile

def pwm_gen(freq,delay,prec): #PWM signal generation (frequency, delay for one signal, precent od PWM signal [Arduino Analog Write values])
    dt=0.000001 #time resolution in secounds
    cycle=1/freq #cycle of PWN
    limit=cycle/dt #number of samples for one pulse width of PWM signal
    con=1/256 #conversion Arduino PWM value into precents
    time_delay=delay*len(prec) #total time for PWM signal
    
    num_sample=time_delay/dt #total number of samples in whole signal
    pwm=np.empty(int(num_sample)) #empty list for PWM signal values

    #Convert Arduino PWM signal into dutycycle of PWM signal in precents
    z=0
    k=0
    prec_sampl=np.empty(int(num_sample))
    for i in range(int(num_sample)):
        prec_sampl[i]=(limit*prec[z]*con)
        if(k<delay/dt):
            k=k+1
        else:
            z=z+1
            k=0
    
    #Convert save PWM values into list
    for i in range(int(num_sample)):
        if(i%limit<prec_sampl[i]):
            pwm[i]=1
        else:
            pwm[i]=0
    return pwm,time_delay

def dac_gen(freq,delay,prec): #Simple DAC signal generation (frequency, delay for one signal, precent od PWM signal [Arduino Analog Write values])
    # Constants
    dt=0.000001 #time resolution in secounds
    con=1/256 #conversion Arduino PWM value into precents

    time_delay=delay*len(prec) #total time of DAC signal 
    num_sample=time_delay/dt #total number of samples in whole signal
    dac=np.empty(int(num_sample)) #empty list of DAC signal values to fill

    #Convert Arduino PWM signal into dutycycle of PWM signal in precents
    z=0
    k=0
    prec_sampl=np.empty(int(num_sample))
    for i in range(int(num_sample)):
        prec_sampl[i]=prec[z]*con
        if(k<delay/dt):
            k=k+1
        else:
            z=z+1
            k=0
    #Convert precents into voltage (D*V, where: D dutycycle of PWM signal in precents and V is max voltage, here 5V)
    for i in range(int(num_sample)):
        dac[i]=prec_sampl[i]*5
    return dac,time_delay


def wav_file(x_channel,y_channel,samplingFrequency):
    # A 2D array where the left and right tones are contained in their respective rows
    tone_y_stereo=np.vstack((x_channel, y_channel))

    # Reshape 2D array so that the left and right tones are contained in their respective columns
    tone_y_stereo=tone_y_stereo.transpose()

    # Produce an audio file that contains stereo sound
    wavfile.write('stereoAudio.wav', samplingFrequency, tone_y_stereo)
    wavfile.write('monoAudio.wav', samplingFrequency, x_channel)