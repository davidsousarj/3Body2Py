#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Newton laws Integrator and real time display
# Author: David Sousa david@pos.iq.ufrj.br 
# Method: Velocity Verlet
# License: Creative Commons

# 3-Body Euler Problem: 2 fixed bodies
# Importing Libraries ##################################################
import pygame
import sys
from pygame.locals import *
import numpy as np
from math import pi, sqrt

# Simulation - Initial Data ############################################
# Uncomment the initial data set you want, or create your own.

# Default and beautiful initial data
d1=(1,1,-1,6.29)
d2=(0.5e-3,40)
d3=(2,0)

# 1 sun, eliptic orbit
#d1=(1,1,-1,3) 
#d2=(0.5e-3,40)
#d3=(1000,1000)

# 1 sun, circular orbit
#d1=(1,0,0,2*pi) 
#d2=(0.5e-3,40)
#d3=(1000,1000)

# Colision test
#d1=(1,1,-1.,6.28)
#d2=(0.5e-3,40)
#d3=(0,2)

x0,y0,vx0,vy0 = d1
h,tf          = d2
XR1,YR1       = d3

k=-4*pi**2         #equals to -G*M*(s/year)^2/(R)^3

# planet mass = 1
# E = K + V1 + V2
E0=(vx0**2+vy0**2)/2+k/sqrt(x0**2+y0**2)+k/sqrt((x0-XR1)**2+(y0-YR1)**2)

# Initializing variables ###############################################
# Main Loop:
#	 Data: x[n] , v[n]
#	 Calculate a[n] = -(1/m)*(d/dx) V{ x[n] } = (1/m)F{ x[n] }
#	 x[n+1] = x[n] + h*v[n] + h*h/2*a[n]
#	 Calculate a[n+1] = -(1/m)*(d/dx) V{ x[n+1] } = (1/m)F{ x[n+1] }
#	 v[n+1] = v[n] + h*(a[n+1] + a[n])/2

x= [x0]; y= [y0]; vx=[vx0]; vy=[vy0]; E=[E0]; e=[0.0]
i=0
ax=[ k*x[i]/(x[i]**2+y[i]**2)**1.5 + k*(x[i]-XR1)/((x[i]-XR1)**2+(y[i]-YR1)**2)**1.5]
ay=[ k*y[i]/(x[i]**2+y[i]**2)**1.5 + k*(y[i]-YR1)/((x[i]-XR1)**2+(y[i]-YR1)**2)**1.5]
t=np.arange(0,tf,h)

# Initialize the screen ################################################
w=255
red,green,blue,white,black = (w,0,0),(0,w,0),(0,0,w),(w,w,w),(0,0,0)

sizex =600; sizey =600
sizeqx = 2; sizeqy = 2
margin=15

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((sizex,sizey))
myfont = pygame.font.SysFont("Sans", 20)
pygame.display.set_caption( 'Euler Three-Body Problem by DavidSousa' )

score=pygame.Rect(margin,550,sizex-2*margin,40)
gameover=pygame.Rect(200,200,300,50)

#screen.fill(white)
#sun = pygame.Rect(sizex//2-5, sizey//2-5, 10, 10)
#sun2= pygame.Rect(sizex/2.+sizex/2.*XR1/4.,sizey/2.+sizey/2.*YR1/4., 10, 10) 
#pygame.draw.rect(screen, red, sun, 2)
#pygame.draw.rect(screen, green, sun2, 2)

screen.fill((200,200,200))
pygame.draw.rect(screen, white, (margin,margin,sizex-2*margin, sizey-2*margin-50), 0)
pygame.draw.circle(screen, red, (sizex//2-5, sizey//2-5), 10)
pygame.draw.circle(screen, green, (int(sizex/2.+sizex/2.*XR1/4.),int(sizey/2.+sizey/2.*YR1/4.)), 10)

pygame.display.update()

collide=-1

# Integration process ##################################################
for i in xrange(0,len(t)-1): 
	x.append(  x[i]  + h*vx[i] + h*h*ax[i]/2     )
	y.append(  y[i]  + h*vy[i] + h*h*ay[i]/2     )

	ax.append( k*x[i+1]/(x[i+1]**2+y[i+1]**2)**1.5 +  k*(x[i+1]-XR1)/((x[i+1]-XR1)**2+(y[i+1]-YR1)**2)**1.5 )
	ay.append( k*y[i+1]/(x[i+1]**2+y[i+1]**2)**1.5 +  k*(y[i+1]-YR1)/((x[i+1]-XR1)**2+(y[i+1]-YR1)**2)**1.5 )

	vx.append( vx[i] + h*(ax[i+1] + ax[i] )/2 )
	vy.append( vy[i] + h*(ay[i+1] + ay[i] )/2 )

	E.append(  0.5*(vx[i]**2+vy[i]**2)+k/sqrt(x[i]**2+y[i]**2)+k/sqrt((x[i]-XR1)**2+(y[i]-YR1)**2) )
	e.append(  100*( E[i] - E0 )/E0 )

# Drawing the screen ###################################################
	# Close event
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit(); sys.exit();

	msElapsed = clock.tick(120)

	X = int( sizex/2.+sizex/2.*x[i]/4. )
	Y = int( sizey/2.-sizey/2.*y[i]/4. )

	planet = pygame.Rect(X,Y,sizeqx,sizeqy)
	pygame.draw.rect(screen, black, planet, 0)
	pygame.draw.rect(screen, white, score, 0)
	error="Erro = %.6f %%" %e[i]
	tempo="Tempo = %.3f / %.3f Anos" %(t[i],t[-1])
	label1 = myfont.render(error, 1, blue, white)
	label2 = myfont.render(tempo, 1, blue, white)
	screen.blit(label1, (margin, 550))
	screen.blit(label2, (250, 550))

	pygame.display.update([planet,score])

	if e[i] > 5.0: #collide
		collide = i
	if collide > 0:
		label3 = myfont.render(u"Colisão!", 1, red, white)
		screen.blit(label3, (200, 200))
		pygame.display.update([planet,score,gameover])
		break
print 'Fim'
while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit(); sys.exit();
