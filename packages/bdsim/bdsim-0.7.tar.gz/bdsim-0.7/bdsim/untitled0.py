#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 09:09:53 2020

@author: corkep
"""

import bdsim
from bdsim.components import SinkBlockGraphics

import numpy as np
from math import sin, cos, pi
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class QuadRotorPlot(SinkBlockGraphics):

    # Flyer plot, lovingly coded by Paul Pounds, first coded 17/4/02
    # version 2 2004 added scaling and ground display
    # version 3 2010 improved rotor rendering and fixed mirroring bug
    #
    # Displays X-4 flyer position and attitude in a 3D plot.
    # GREEN ROTOR POINTS NORTH
    # BLUE ROTOR POINTS EAST
    
    # PARAMETERS
    # s defines the plot size in meters
    # swi controls flyer attitude plot; 1 = on, otherwise off.
    
    # INPUTS
    # 1 Center X position
    # 2 Center Y position
    # 3 Center Z position
    # 4 Yaw angle in rad
    # 5 Pitch angle in rad
    # 6 Roll angle in rad
     
    def __init__(self, model, scale=2, projection='ortho', **kwargs):
        super().__init__(**kwargs)
        self.type = 'quadrotorplot'
        self.model = model
        self.scale = scale
        self.nrotors = model['nrotors']
        self.projection = projection

    def start(self):
        quad = self.model
        
        # vehicle dimensons
        d = quad['d'];  # Hub displacement from COG
        r = quad['r'];  # Rotor radius

        #C = np.zeros((3, self.nrotors))   ## WHERE USED?
        self.D = np.zeros((3,self.nrotors))

        for i in range(0, self.nrotors):
            theta = i / self.nrotors * 2 * pi
            #  Di      Rotor hub displacements (1x3)
            # first rotor is on the x-axis, clockwise order looking down from above
            self.D[:,i] = np.r_[ quad['d'] * cos(theta), quad['d'] * sin(theta), quad['h']]
        
        #draw ground
        self.fig = plt.figure()
        # no axes in the figure, create a 3D axes
        self.ax = self.fig.add_subplot(111, projection='3d', proj_type=self.projection)

        # ax.set_aspect('equal')
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('-Z (height above ground)')
        
        # TODO allow user to set maximum height of plot volume
        self.ax.set_xlim(-self.scale, self.scale)
        self.ax.set_ylim(-self.scale, self.scale)
        self.ax.set_zlim(0, self.scale)

        # plot the ground boundaries and the big cross
        s = self.scale
        self.ax.plot([-s, s], [-s, s], [0, 0], 'b-')
        self.ax.plot([-s, s], [s, -s], [0, 0], 'b-')
        self.ax.grid(True)
        
        self.shadow, = self.ax.plot([0, 0], [0, 0], 'k--')
        self.groundmark, = self.ax.plot([0], [0], [0], 'kx')
        
        self.arm = []
        self.disk = []
        for i in range(0, self.nrotors):
            h, = self.ax.plot([0], [0], [0])
            self.arm.append(h)
            h, = self.ax.plot([0], [0], [0], 'b-')
            self.disk.append(h)
            
        self.a1s = np.zeros((self.nrotors,))
        self.b1s = np.zeros((self.nrotors,))

    def step(self):

        def plot3(h, x, y, z):
            h.set_data(x, y)
            h.set_3d_properties(z)
            
        # READ STATE
        z = self.inputs[0][0:3]
        n = self.inputs[0][3:6]
        
        a1s = self.a1s
        b1s = self.b1s
        
        quad = self.model
        
        # vehicle dimensons
        d = quad['d'];  # Hub displacement from COG
        r = quad['r'];  # Rotor radius
        
        # PREPROCESS ROTATION MATRIX
        phi = n[0];    # Euler angles
        the = n[1];
        psi = n[2];
        
        # BBF > Inertial rotation matrix
        R = np.array([
                [cos(the) * cos(phi), sin(psi) * sin(the) * cos(phi) - cos(psi) * sin(phi), cos(psi) * sin(the) * cos(phi) + sin(psi) * sin(phi)],   
                [cos(the) * sin(phi), sin(psi) * sin(the) * sin(phi) + cos(psi) * cos(phi), cos(psi) * sin(the) * sin(phi) - sin(psi)*  cos(phi)],
                [-sin(the),           sin(psi)*cos(the),                                    cos(psi) * cos(the)]
            ])
        
        # Manual Construction
        #Q3 = [cos(psi) -sin(psi) 0;sin(psi) cos(psi) 0;0 0 1];   %Rotation mappings
        #Q2 = [cos(the) 0 sin(the);0 1 0;-sin(the) 0 cos(the)];
        #Q1 = [1 0 0;0 cos(phi) -sin(phi);0 sin(phi) cos(phi)];
        #R = Q3*Q2*Q1;    %Rotation matrix
        
        # CALCULATE FLYER TIP POSITONS USING COORDINATE FRAME ROTATION
        F = np.array([
                [1,  0,  0],
                [0, -1,  0],
                [0,  0, -1]
            ])
        
        # Draw flyer rotors
        theta = np.linspace(0, 2 * pi, 20)
        circle = np.zeros((3, 20))
        for j, t in enumerate(theta):
            circle[:,j] = np.r_[r * sin(t), r * cos(t), 0]
        
        hub = np.zeros((3, self.nrotors))
        tippath = np.zeros((3, 20, self.nrotors))
        for i in range(0, self.nrotors):
            hub[:,i] = F @ (z + R @ self.D[:,i])  # points in the inertial frame
            
            q = 1   # Flapping angle scaling for output display - makes it easier to see what flapping is occurring
            # Rotor -> Plot frame
            Rr = np.array([
                    [cos(q * a1s[i]),  sin(q * b1s[i]) * sin(q * a1s[i]),  cos(q * b1s[i]) * sin(q * a1s[i])],
                    [0,                cos(q * b1s[i]),                   -sin(q*b1s[i])],
                    [-sin(q * a1s[i]), sin(q * b1s[i]) * cos(q * a1s[i]),  cos(q * b1s[i]) * cos(q * a1s[i])]
                ])
            
            tippath[:,:,i] = F @ R @ Rr @ circle
            plot3(self.disk[i], hub[0,i] + tippath[0,:,i], hub[1,i] + tippath[1,:,i], hub[2,i] + tippath[2,:,i])

        # Draw flyer
        hub0 = F @ z  # centre of vehicle
        for i in range(0, self.nrotors):
            # line from hub to centre plot3([hub(1,N) hub(1,S)],[hub(2,N) hub(2,S)],[hub(3,N) hub(3,S)],'-b')
            plot3(self.arm[i], [hub[0,i], hub0[0]],[hub[1,i], hub0[1]],[hub[2,i], hub0[2]])
            
            # plot a circle at the hub itself
            #plot3([hub(1,i)],[hub(2,i)],[hub(3,i)],'o')

        
        # plot the vehicle's centroid on the ground plane
        plot3(self.shadow, [z[0], 0], [-z[1], 0], [0, 0])
        plot3(self.groundmark, z[0], -z[1], 0)



if __name__ == "__main__":
    
    from quad_model import quadrotor as qm
    
    b = QuadRotorPlot(qm)
    
    b.start()
    
    b.setinputs(np.r_[0.5, 0, -1, 0, 0, 0, 0,0,0,0,0,0])
    b.step()
    

