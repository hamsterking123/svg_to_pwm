# Import modules
import matplotlib.pyplot as plt
import numpy as np
import svg_points as svg
import signal_gen as gen

def draw_signal(signal1,signal2): #for debuging drawing signal
    plt.plot(signal1,signal2,'-o')
    plt.ylim(-400, 350)
    plt.xlim(0, 300)
    plt.show()

#const value
scale=1
freq=615000
time=0.0001

result=svg.svg_elipse_arc(160.61709, 160.61709, 0, 169.50977, 9.2871094,56.330078,56.330078) #rx,ry,phi,x1,y1,x2,y2
result2=svg.svg_elipse_arc(160.61709, 160.61709, 0, 56.330078,56.330078,52.867188, 279.9043 ) #rx,ry,phi,x1,y1,x2,y2
result3=np.array([127.61523,205.17383])
result4=np.array([78.205078,155.76172])
result5=np.array([60.527344,173.43945])

result0=np.concatenate((result[0]),axis=None)
result1=np.concatenate((result[1]),axis=None)
print(result0,result1)
draw_signal(result0,result1)
result=svg.shape_alignment(result0,result1)
pwm_org_x=result[0]*scale
pwm_org_y=result[1]*scale
testx=gen.dac_gen(freq,time,pwm_org_x)
testy=gen.dac_gen(freq,time,pwm_org_y)
gen.wav_file(testx[0],testy[0],freq)