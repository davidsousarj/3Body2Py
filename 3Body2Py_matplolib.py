#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Newton laws Integrator and real time display
# Author: David Sousa david@pos.iq.ufrj.br 
# Method: Velocity Verlet
# License: Creative Commons

# 3-Body Euler Problem: 2 fixed bodies
# This version uses matplotlib instead PyGame
# Importing Libraries ##################################################
import sys
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation as anim
pi=np.pi
sqrt=np.sqrt

# Simulation - Global Initial Data ######################################
# Uncomment the initial data set you want, or create your own.
d1=(1,1,-1,6.28,2,0,0.5e-3)         # Default beautiful initial data
#d1=(1,1,-1,3,1000,1000,0.5e-3)     # 1 sun, eliptic orbit
#d1=(1,0,0,2*pi,1000,1000,0.5e-3)   # 1 sun, circular orbit
#d1=(1,1,-1.,6.28,0,2,1e-3)         # Colision test

# x0,y0,vx0,vy0,2nd Sun X,2nd Sun Y,timestep
x,y,vx,vy,XR1,YR1,h = d1

k=-4*pi**2    #equals to -G*M*(s/year)^2/(R)^3

# planet mass = 1
# E = K + V1 + V2
E0=(vx**2+vy**2)/2+k/sqrt(x**2+y**2)+k/sqrt((x-XR1)**2+(y-YR1)**2)

ax=k*x/(x**2+y**2)**1.5 + k*(x-XR1)/((x-XR1)**2+(y-YR1)**2)**1.5
ay=k*y/(x**2+y**2)**1.5 + k*(y-YR1)/((x-XR1)**2+(y-YR1)**2)**1.5

X,Y=[],[] #trajectory
t=0.0
e=0.0

# Initialize the screen ################################################
fig = plt.figure()
axis  = plt.axes( xlim=(-4,4), ylim=(-4,4))
plt.grid()
plt.plot(0,0,'ro',XR1,YR1,'go')
traj, = axis.plot([],[], 'b-', lw=2)
time_text= axis.text(1,-3,"")
error_text=axis.text(1,-3.5,"")

# Integration process ##################################################
def new_position(x,y,vx,vy,ax,ay,t):
	# Main Loop:
	#	 Data: x[n] , v[n]
	#	 Calculate a[n] = -(1/m)*(d/dx) V{ x[n] } = (1/m)F{ x[n] }
	#	 x[n+1] = x[n] + h*v[n] + h*h/2*a[n]
	#	 Calculate a[n+1] = -(1/m)*(d/dx) V{ x[n+1] } = (1/m)F{ x[n+1] }
	#	 v[n+1] = v[n] + h*(a[n+1] + a[n])/2
	x =  x  + h*vx + h*h*ax/2     
	y =  y  + h*vy + h*h*ay/2     
	axN = k*x/(x**2+y**2)**1.5 +  k*(x-XR1)/((x-XR1)**2+(y-YR1)**2)**1.5 
	ayN = k*y/(x**2+y**2)**1.5 +  k*(y-YR1)/((x-XR1)**2+(y-YR1)**2)**1.5 
	vx = vx + h*(axN + ax )/2 
	vy = vy + h*(ayN + ay )/2 
	ax=axN
	ay=ayN
	E = 0.5*(vx**2+vy**2)+k/sqrt(x**2+y**2)+k/sqrt((x-XR1)**2+(y-YR1)**2) 
	e = 100*( E - E0 )/E0 
	t+=h
	X.append(x); Y.append(y)
	
	# Detect collision	
	if e > 5.0:
		cl=plt.text(2,2,u"Colisão!")
		plt.draw()
		return 0,0,0,0,0,0,0,0,0 # Raise error in integration
	
	return x,y,vx,vy,ax,ay,t,E,e

# Drawing on the screen #################################################

def init():
	traj.set_data([],[])
	return traj,

def animate(i):
	global x,y,vx,vy,ax,ay,t,E,e,X,Y
	x,y,vx,vy,ax,ay,t,E,e = new_position(x,y,vx,vy,ax,ay,t)
	traj.set_data(X,Y)
	time_text.set_text("Error = %.6f %%" %e)
	error_text.set_text("Time = %.3f Years" %t)
	return traj,time_text,error_text

anim = anim.FuncAnimation(fig,animate,init_func=init,frames=200,interval=0.1,blit=True)
plt.show()
# End
#anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
