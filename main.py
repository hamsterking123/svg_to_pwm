# Import modules
import matplotlib.pyplot as plt
import numpy as np
import svg_points as svg
import signal_gen as gen

def draw_signal(signal1,signal2): #for debuging drawing signal
    plt.plot(signal1,signal2,'-o')
    plt.ylim(-1, 8)
    plt.xlim(-1, 8)
    plt.show()


#const value
scale=1
freq_pwm=900
freq=320000
time=0.0001

resultxy=svg.file_read("poseidon_svg_full.txt")
result=svg.shape_alignment(resultxy[0],resultxy[1])
pwm_org_x=result[0]*scale
pwm_org_y=result[1]*scale
testx=gen.dac_gen(freq_pwm,time,pwm_org_x)
testy=gen.dac_gen(freq_pwm,time,pwm_org_y)
gen.wav_file(testx[0],testy[0],freq)
print("x",testx[0],len(testx[0]))
print("y",testy[0],len(testy[0]))
draw_signal(testx[0],testy[0])