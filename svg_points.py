import numpy as np
steps=0.05 #resolutino of angle
def svg_elipse_arc(rx,ry,phi,fa,fs,x2,y2,x1,y1):
    #Const
    
    #sign using during center point calculation
    if(fa==fs):
        sign1=-1
    else:
        sign1=1

    #Calcuel cx and cy (center of ellipse)
    x_prim=np.cos(phi)*((x1-x2)/2)+np.sin(phi)*((y1-y2)/2)
    y_prim=-np.sin(phi)*((x1-x2)/2)+np.cos(phi)*((y1-y2)/2)

    c_scale_numerator=(rx*rx*ry*ry)-(rx*rx*y_prim*y_prim)-(ry*ry*x_prim*x_prim)
    c_scale_denumerator=rx*rx*y_prim*y_prim+ry*ry*x_prim*x_prim

    c_scale=sign1*np.sqrt(c_scale_numerator/c_scale_denumerator)
    cx_prim=c_scale*(rx*y_prim/ry)
    cy_prim=c_scale*(-ry*x_prim/rx)

    cx=np.cos(phi)*cx_prim-np.sin(phi)*cy_prim+((x1+x2)/2)
    cy=np.sin(phi)*cx_prim+np.cos(phi)*cy_prim+((y1+y2)/2)

    #Calculae theta and delta theta (angle of arc)
    ux_theta=1
    uy_theta=0
    vx_theta=(x_prim-cx_prim)/rx
    vy_theta=(y_prim-cy_prim)/ry
    #Sign of theta
    sign_theta=ux_theta*vy_theta-uy_theta*vx_theta
    if(sign_theta>=0):
        sign2=1
    else:
        sign2=-1

    theta_numerator=ux_theta*vx_theta+uy_theta*vy_theta
    theta_denumerator=np.sqrt(np.power(ux_theta,2)+np.power(uy_theta,2))*np.sqrt(np.power(vx_theta,2)+np.power(vy_theta,2))
    theta=sign2*np.arccos(theta_numerator/theta_denumerator)

    ux_delta_theta=(x_prim-cx_prim)/rx
    uy_delta_theta=(y_prim-cy_prim)/ry
    vx_delta_theta=(-x_prim-cx_prim)/rx
    vy_delta_theta=(-y_prim-cy_prim)/ry
    #Sign of theta
    sign_delta_theta=ux_delta_theta*vy_delta_theta-uy_delta_theta*vx_delta_theta
    if(sign_delta_theta>=0):
        sign3=1
    else:
        sign3=-1
    
    delta_theta_numerator=ux_delta_theta*vx_delta_theta+uy_delta_theta*vy_delta_theta
    delta_theta_denumerator=np.sqrt(np.power(ux_delta_theta,2)+np.power(uy_delta_theta,2))*np.sqrt(np.power(vx_delta_theta,2)+np.power(vy_delta_theta,2))
    delta_theta=sign3*np.arccos(delta_theta_numerator/delta_theta_denumerator)
    delta_theta=delta_theta%(2*np.pi)

    if(fs==0):
        if(delta_theta>0):
            delta_theta=delta_theta-2*np.pi
    else:
        if(delta_theta<0):
            delta_theta=delta_theta+2*np.pi

    size=round(abs(delta_theta)/steps)+1 #size of list
    #list of angles values to thetha angle in radians
    xypi=np.empty(size)
    if(delta_theta>=0):
        for i in range(size):
            xypi[i]=theta+i*steps
    else:
        for i in range(size):
            xypi[i]=theta-i*steps

    xpoints=np.empty(size)
    ypoints=np.empty(size)
    for i in range (size):
        xpoints[i]=np.cos(phi)*rx*np.cos(xypi[i])-np.sin(phi)*ry*np.sin(xypi[i])+cx
        ypoints[i]=np.sin(phi)*rx*np.cos(xypi[i])+np.cos(phi)*ry*np.sin(xypi[i])+cy
    return(xpoints,-ypoints)

def svg_bezier(pcs_x,pcs_y,pce_x,pce_y,x2,y2,x1,y1):
    #Const
    size=round(1/steps)+1
    xpoints=np.empty(size)
    ypoints=np.empty(size)
    #for i in range (size):
    for i in range(size):
        t=i/size
        xpoints[i]=np.power((1-t),3)*x1+3*t*np.power((1-t),2)*pcs_x+3*(1-t)*t*t*pce_x+t*t*t*x2
        ypoints[i]=np.power((1-t),3)*y1+3*t*np.power((1-t),2)*pcs_y+3*(1-t)*t*t*pce_y+t*t*t*y2
    return(xpoints,-ypoints)

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

def file_read(f_name):
    text_list=[]
    i=0
    start_temp=np.empty(2)
    resultxy=np.array([[],[]])

    with open(f_name,"r") as f:
        for line in f:
            text_list.extend(line.split())
    
    while i<len(text_list):
        if(text_list[i]=='M'):
            start_temp=[float(text_list[i+1]),float(text_list[i+2])]
            i=i+3
        elif(text_list[i]=="z"):
            i=i+1
        elif(text_list[i]=="L"):
            result=np.array([[float(text_list[i+1])],[-float(text_list[i+2])]])
            resultxy=np.concatenate((resultxy,result),axis=1)
            start_temp=[float(text_list[i+1]),float(text_list[i+2])]
            i=i+3
        elif(text_list[i]=="A"):
            result=svg_elipse_arc(float(text_list[i+1]),float(text_list[i+2]),float(text_list[i+3]),float(text_list[i+4]),float(text_list[i+5]),float(text_list[i+6]),float(text_list[i+7]),start_temp[0],start_temp[1])
            resultxy=np.concatenate((resultxy,result),axis=1)
            start_temp=[float(text_list[i+6]),float(text_list[i+7])]
            i=i+8
        else:
            result=svg_bezier(float(text_list[i+1]),float(text_list[i+2]),float(text_list[i+3]),float(text_list[i+4]),float(text_list[i+5]),float(text_list[i+6]),start_temp[0],start_temp[1])
            resultxy=np.concatenate((resultxy,result),axis=1)
            start_temp=[float(text_list[i+5]),float(text_list[i+6])]
            i=i+7
    return(resultxy)