#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Newton laws Integrator and real time display
# Author: David Sousa david@pos.iq.ufrj.br 
# Method: Velocity Verlet
# License: Creative Commons

# 1 fixed and two mobile bodies
# Importing Libraries ##################################################
import pygame
import sys
from pygame.locals import *
import numpy as np
from math import pi, sqrt

# Simulation - Initial Data ############################################
# Uncomment the initial data set you want, or create your own.

# initial
#d1=(1.,1.,1.,-1,6.29) 
#d2=(0.1,2.,0.,-1,0.1)
#d3=(0.5e-3,40)
#d4=(1.0)

# Colision earth!
#d1=(1.,0.,1.,-1,6.29) 
#d2=(0.01,1.,1.5,-3.5,12)
#d3=(0.5e-3,40)
#d4=(1.0)

# Colision moon!
#d1=(1.,1.,0.,-1,6.29) 
#d2=(0.01,1.5,0.0,-3.5,12)
#d3=(0.5e-3,40)
#d4=(1.0)

# crazy dance
#d1=(1.00,3.0,0.0,0.0,3.0) 
#d2=(0.01,3.5,0.0,0.0,6.0)
#d3=(0.5e-3,40)
#d4=(1.0)

# almost there...
#d1=(1.00,3.0,0.0,0.0,3.0) 
#d2=(0.01,3.25,0.0,0.0,9.0)
#d3=(0.5e-3,40)
#d4=(1.0)

# PERFECT!
#d1=(1.00,3.0,0.0,0.0,3.0) 
#d2=(0.01,3.25,0.0,0.0,15.0)
#d3=(0.5e-3,40)
#d4=(1.0)

# projectile satellite
#d1=(1.00,3.0,2.50,-0.5,-3.3) 
#d2=(0.01,3.25,2.0,-1.5,-6.0)
#d3=(0.5e-3,40)
#d4=(1.0)

# accelerated
#d1=(1.00,1.0,0.0,0.0,6.28) 
#d2=(0.1,2.25,0.0,0.0,6.28)
#d3=(0.5e-3,40)
#d4=(1.0)

# just two regular planets
#d1=(0.01,1.0,0.0,0.0,5.) 
#d2=(0.001,3.25,0.0,0.0,3.)
#d3=(0.5e-4,40)
#d4=(1.0)

# circular perfection
#d1=(0.01,2000,0.0,0.0,10.) 
#d2=(0.1,3.,0.0,0.0,3.6)
#d3=(0.5e-4,40)
#d4=(1.0)

# dance for me baby
#d1=(0.01,1.5,0.0,0.5,5.) 
#d2=(0.10,3.0,0.0,0.0,3.6)
#d3=(0.5e-4,40)
#d4=(1.0)

# front colision
d1=(2.0,0.0, 2.0,-1.5, 1.5) 
d2=(2.0,0.0,-2.0, 2.5,-2.5)
d3=(0.5e-4,40)
d4=(1.0)

clocktick=0 # 0 for fastest animation, microseconds elapsed between steps

m1,x01,y01,vx01,vy01 = d1
m2,x02,y02,vx02,vy02 = d2
h,tf = d3
M = d4

G=-4*pi**2

# E = K1 + V1 + K2 + V2 + V12
E0 = m1*(0.5*(vx01**2 + vy01**2) + G*M/sqrt(x01**2 + y01**2))
E0+= m2*(0.5*(vx02**2 + vy02**2) + G*M/sqrt(x02**2 + y02**2))
E0+= G*m1*m2/sqrt((x01-x02)**2+(y01-y02)**2)

# Initializing variables ###############################################
# Main Loop:
#	 Data: x[n] , v[n]
#	 Calculate a[n] = -(1/m)*(d/dx) V{ x[n] } = (1/m)F{ x[n] }
#	 x[n+1] = x[n] + h*v[n] + h*h/2*a[n]
#	 Calculate a[n+1] = -(1/m)*(d/dx) V{ x[n+1] } = (1/m)F{ x[n+1] }
#	 v[n+1] = v[n] + h*(a[n+1] + a[n])/2

x1= [x01]; y1= [y01]; vx1=[vx01]; vy1=[vy01]
x2= [x02]; y2= [y02]; vx2=[vx02]; vy2=[vy02]
E=[E0]; e=[0.0]

i=0

ax1=[ G*M*x1[i]/(x1[i]**2+y1[i]**2)**1.5 + G*m2*(x1[i]-x2[i])/((x1[i]-x2[i])**2+(y1[i]-y2[i])**2)**1.5]
ay1=[ G*M*y1[i]/(x1[i]**2+y1[i]**2)**1.5 + G*m2*(y1[i]-y2[i])/((x1[i]-x2[i])**2+(y1[i]-y2[i])**2)**1.5]
ax2=[ G*M*x2[i]/(x2[i]**2+y2[i]**2)**1.5 + G*m1*(x2[i]-x1[i])/((x2[i]-x1[i])**2+(y2[i]-y1[i])**2)**1.5]
ay2=[ G*M*y2[i]/(x2[i]**2+y2[i]**2)**1.5 + G*m1*(y2[i]-y1[i])/((x2[i]-x1[i])**2+(y2[i]-y1[i])**2)**1.5]

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
pygame.display.set_caption( 'Sun + 2 Planets by DavidSousa' )

score=pygame.Rect(margin,550,sizex-2*margin,40)
gameover=pygame.Rect(200,200,300,50)

screen.fill((200,200,200))
pygame.draw.rect(screen, white, (margin,margin,sizex-2*margin, sizey-2*margin-50), 0)
pygame.draw.circle(screen, red, (sizex//2-5, sizey//2-5), 10)

pygame.display.update()

collide=-1

# Integration process ##################################################
for i in xrange(0,len(t)-1): 
	x1.append(  x1[i]  + h*vx1[i] + h*h*ax1[i]/2     )
	y1.append(  y1[i]  + h*vy1[i] + h*h*ay1[i]/2     )
	x2.append(  x2[i]  + h*vx2[i] + h*h*ax2[i]/2     )
	y2.append(  y2[i]  + h*vy2[i] + h*h*ay2[i]/2     )

	ax1.append( G*M*x1[i+1]/(x1[i+1]**2+y1[i+1]**2)**1.5 +  G*m2*(x1[i+1]-x2[i+1])/((x1[i+1]-x2[i+1])**2+(y1[i+1]-y2[i+1])**2)**1.5 )
	ay1.append( G*M*y1[i+1]/(x1[i+1]**2+y1[i+1]**2)**1.5 +  G*m2*(y1[i+1]-y2[i+1])/((x1[i+1]-x2[i+1])**2+(y1[i+1]-y2[i+1])**2)**1.5 )
	ax2.append( G*M*x2[i+1]/(x2[i+1]**2+y2[i+1]**2)**1.5 +  G*m1*(x2[i+1]-x1[i+1])/((x2[i+1]-x1[i+1])**2+(y2[i+1]-y1[i+1])**2)**1.5 )
	ay2.append( G*M*y2[i+1]/(x2[i+1]**2+y2[i+1]**2)**1.5 +  G*m1*(y2[i+1]-y1[i+1])/((x2[i+1]-x1[i+1])**2+(y2[i+1]-y1[i+1])**2)**1.5 )

	vx1.append( vx1[i] + h*(ax1[i+1] + ax1[i] )/2 )
	vy1.append( vy1[i] + h*(ay1[i+1] + ay1[i] )/2 )
	vx2.append( vx2[i] + h*(ax2[i+1] + ax2[i] )/2 )
	vy2.append( vy2[i] + h*(ay2[i+1] + ay2[i] )/2 )

	Etmp = m1*(0.5*(vx1[i]**2 + vy1[i]**2) + G*M/sqrt(x1[i]** 2+ y1[i]**2))
	Etmp+= m2*(0.5*(vx2[i]**2 + vy2[i]**2) + G*M/sqrt(x2[i]** 2+ y2[i]**2))
	Etmp+= G*m1*m2/sqrt((x1[i]-x2[i])**2+(y1[i]-y2[i])**2)

	E.append( Etmp )
	e.append( 100*( Etmp - E0 )/E0 )

# Drawing the screen ###################################################
	# Close event
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit(); sys.exit();

	msElapsed = clock.tick(clocktick)

	X1 = int( sizex/2.+sizex/2.*x1[i]/4. )
	Y1 = int( sizey/2.-sizey/2.*y1[i]/4. )
	X2 = int( sizex/2.+sizex/2.*x2[i]/4. )
	Y2 = int( sizey/2.-sizey/2.*y2[i]/4. )

	planet1 = pygame.Rect(X1,Y1,sizeqx,sizeqy)
	planet2 = pygame.Rect(X2,Y2,sizeqx,sizeqy)
	pygame.draw.rect(screen, black, planet1, 0)
	pygame.draw.rect(screen, blue , planet2, 0)
	pygame.draw.rect(screen, white, score, 0)
	error="Erro = %.6f %%" %e[i]
	tempo="Tempo = %.3f / %.3f Anos" %(t[i],t[-1])
	label1 = myfont.render(error, 1, blue, white)
	label2 = myfont.render(tempo, 1, blue, white)
	screen.blit(label1, (margin, 550))
	screen.blit(label2, (250, 550))

	pygame.display.update([planet1,planet2,score])

	if e[i] > 10.0: #collide
		collide = i
	if collide > 0:
		label3 = myfont.render(u"Colisão!", 1, red, white)
		screen.blit(label3, (200, 200))
		pygame.display.update([planet1,planet2,score,gameover])
		break
print 'Fim'
while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit(); sys.exit();
