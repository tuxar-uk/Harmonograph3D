#!/usr/bin/python
'''    3D Spectral Harmonographs   Copyright 2014 Alan Richmond (Tuxar.uk)
    Uses Vpython. Hold down right mouse button and move mouse or trackball to rotate.
    Press any key for next harmonograph (e.g. space bar).
    MIT License.
'''
from visual import *
from math import sin
import sys, random as r

width,height=1280,720       # YouTube HD
#width,height=1920,1080      # my left monitor
width,height=1280,1024      # my right monitor
depth=1080
hui=.159
dec=0.99996
dt=0.01
mx=4
sd=0.005
#   Amplitudes & scales
def scale(length):
    while True:
        a1,a2=r.randint(-mx,mx),r.randint(-mx,mx)
        max=abs(a1)+abs(a2)
        if max>0: break
    return a1,a2,length/(2*max)
while True:
    d=display(title='3D Spectral Harmonograph',width=width,height=height)
    trail=curve()
    d .visible=True
    ax1,ax2,xscale=scale(width)
    ay1,ay2,yscale=scale(height)
    az1,az2,zscale=scale(depth)
    #   Frequencies
    fx1, fx2 =  r.randint(1,mx) + r.gauss(0,sd), r.randint(1,mx) + r.gauss(0,sd)
    fy1, fy2 =  r.randint(1,mx) + r.gauss(0,sd), r.randint(1,mx) + r.gauss(0,sd)
    fz1, fz2 =  r.randint(1,mx) + r.gauss(0,sd), r.randint(1,mx) + r.gauss(0,sd)
    #   Phases
    px1, px2 =  r.uniform(0,2*pi), r.uniform(0,2*pi)
    py1, py2 =  r.uniform(0,2*pi), r.uniform(0,2*pi)
    pz1, pz2 =  r.uniform(0,2*pi), r.uniform(0,2*pi)
    print   ax1,ax2,ay1,ay2
    print   fx1,fx2,fy1,fy2
    print   px1,px2,py1,py2
    first=True
    x=y=z=0.0
    k=1
    hue=0
    t=0
    #   Note that there are 2 nested loops here, where 1 should suffice BUT curve() only takes
    #   1000 points before dropping some. See bottom of http://vpython.org/contents/docs/curve.html
    #   My solution is to start a new trail every 1000 points.
    for j in range (50):
        if not first: trail=curve(pos=(x,y,z),color=color.hsv_to_rgb((hue,1,1)))
        for i in range (1000):
            rate(100000)
            x = xscale * k * (ax1*sin(t * fx1 + px1) + ax2*sin(t * fx2 + px2))
            y = yscale * k * (ay1*sin(t * fy1 + py1) + ay2*sin(t * fy2 + py2))
            z = zscale * k * (az1*sin(t * fz1 + pz1) + az2*sin(t * fz2 + pz2))
            trail.append(pos=(x,y,z),color=color.hsv_to_rgb((hue,1,1)))
            hue = (hue + dt*hui) % 360      # cycle hue
            t+=dt
            first=False
            k*=dec
    key = d.kb.getkey() # wait for and get keyboard info
    trail.visible=0