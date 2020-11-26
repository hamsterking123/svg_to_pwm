import numpy as np

def svg_elipse_arc(rx,ry,phi,x1,y1,x2,y2):
    steps=0.03 #resolutino of angle
    #Calcuel cx and cy (center of ellipse)
    x_prim=np.cos(phi)*((x1-x2)/2)+np.sin(phi)*((y1-y2)/2)
    y_prim=-np.sin(phi)*((x1-x2)/2)+np.cos(phi)*((y1-y2)/2)

    #print("x_prim",x_prim)
    #print("y_prim",y_prim)

    c_scale_numerator=(rx*rx*ry*ry)-(rx*rx*y_prim*y_prim)-(ry*ry*x_prim*x_prim)
    c_scale_denumerator=rx*rx*y_prim*y_prim+ry*ry*x_prim*x_prim
    #print("c_scale_numerator",c_scale_numerator)
    #print("c_scale_denumerator",c_scale_denumerator)
    c_scale=-np.sqrt(c_scale_numerator/c_scale_denumerator)
    #print("c_scale",c_scale)
    cx_prim=c_scale*(rx*y_prim/ry)
    cy_prim=c_scale*(-ry*x_prim/rx)
    #print("cx_prim",cx_prim)
    #print("cy_prim",cy_prim)

    cx=np.cos(phi)*cx_prim-np.sin(phi)*cy_prim+((x1+x2)/2)
    cy=np.sin(phi)*cx_prim+np.cos(phi)*cy_prim+((y1+y2)/2)

    theta_numerator=(x_prim-cx_prim)/rx
    theta_denumerator=np.sqrt(1)*np.sqrt(np.power((x_prim-cx_prim)/rx,2)+np.power((y_prim-cy_prim)/ry,2))
    theta=np.arccos(theta_numerator/theta_denumerator)

    delta_theta_numerator=((x_prim-cx_prim)/rx)*((-x_prim-cx_prim)/rx)+((y_prim-cy_prim)/ry)*((-y_prim-cy_prim)/ry)
    delta_theta_denumerator=np.sqrt(np.power((x_prim-cx_prim)/rx,2)+np.power((y_prim-cy_prim)/ry,2))*np.sqrt(np.power((-x_prim-cx_prim)/rx,2)+np.power((y_prim-cy_prim)/ry,2))
    delta_theta=np.arccos(delta_theta_numerator/delta_theta_denumerator)%360
    #delta_theta=delta_theta*0.01745329252

    #print("cx,cy",cx,cy)
    #print("theta",theta)
    #print("delta_theta",delta_theta)

    size=round(delta_theta/steps) #size of list
    #list of angles values to thetha angle in radians
    xypi=np.empty(size)
    for i in range(size):
        xypi[i]=i*steps+theta

    xpoints=np.empty(size)
    ypoints=np.empty(size)
    for i in range (size):
        xpoints[i]=np.cos(phi)*rx*np.cos(xypi[i])-np.sin(phi)*ry*np.sin(xypi[i])+cx
        ypoints[i]=np.sin(phi)*rx*np.cos(xypi[i])+np.cos(phi)*ry*np.sin(xypi[i])+cy
    return(xpoints,ypoints)
    
def shape_alignment(xpoints,ypoints):
    #value of shift in x and y (shifting to 0)
    shift_x=min(xpoints)
    shift_y=min(ypoints)
    #value shifting shape in x and y
    for i in range (len(xpoints)):
        xpoints[i]=xpoints[i]-shift_x
        ypoints[i]=ypoints[i]-shift_y
    #scale the biggest value to 256 (ADC resolution)
    max_xy=max(max(xpoints),max(ypoints))
    scale=256/max_xy
    xpoints=xpoints*scale
    ypoints=ypoints*scale
    return(xpoints,ypoints)