# Import modules
import matplotlib.pyplot as plt
import numpy as np
import svg_points as svg
import signal_gen as gen

def draw_signal(signal1,signal2): #for debuging drawing signal
    plt.plot(signal1,signal2,'-o')
    plt.ylim(-10, 300)
    plt.xlim(-10, 300)
    plt.show()

#const value
scale=1
freq=615000
time=0.0001

result=svg.svg_elipse_arc(160.61709,160.61709,0,0,0,56.330078,56.330078,169.50977,9.2871094) #rx,ry,phi,fa,fs,x2,y2,x1,y1
result2=svg.svg_elipse_arc(160.61709,160.61709,0,0,0,52.867188,279.9043,56.330078,56.330078) #rx,ry,phi,fa,fs,x2,y2,x1,y1
result3=np.array([127.61523,-205.17383])
result4=np.array([78.205078,-155.76172])
result5=np.array([60.527344,-173.43945])
result6=svg.svg_bezier(58.62807,175.33874,55.569195,175.33873,53.669922,173.43945,60.527344,173.43945)#pcs_x,pcs_y,pce_x,pce_y,x2,y2,x1,y1
result7=np.array([53.369141,-173.13867])
result8=svg.svg_bezier(51.469868,171.2394,51.55776,168.26842,53.457031,166.36914,53.369141,173.13867)#pcs_x,pcs_y,pce_x,pce_y,x2,y2,x1,y1
result9=np.array([74.669922,-145.15625])
result10=svg.svg_bezier(75.619561,144.2066,76.78802,143.27539,78.027344,143.27539,74.669922,145.15625)#pcs_x,pcs_y,pce_x,pce_y,x2,y2,x1,y1
result11=svg.svg_bezier(79.266681,143.27538,80.792554,144.20662,81.742188,145.15625,78.027344,143.27539)#pcs_x,pcs_y,pce_x,pce_y,x2,y2,x1,y1

result0=np.concatenate((result[0],result2[0],result3[0],result4[0],result5[0],result6[0],result7[0],result8[0],result9[0],result10[0],result11[0]),axis=None)
result1=np.concatenate((result[1],result2[1],result3[1],result4[1],result5[1],result6[1],result7[1],result8[1],result9[1],result10[1],result11[1]),axis=None)
#print(result0,result1)
#result0=np.array([9,9,3,9,4,9,6,9,8,10,12,11,14,11,16,11,17,11,11])
#result1=np.array([3,6,6,10,10,14,14,17,17,19,17,17,14,14,10,10,6,6,3])
result=svg.shape_alignment(result0,result1)
draw_signal(result[0],result[1])
pwm_org_x=result[0]*scale
pwm_org_y=result[1]*scale
testx=gen.dac_gen(freq,time,pwm_org_x)
testy=gen.dac_gen(freq,time,pwm_org_y)
gen.wav_file(testx[0],testy[0],freq)