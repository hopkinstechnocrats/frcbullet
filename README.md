# FRCBullet
## Summary
This project is intended to be used by FRC teams, and provides an interface between the desktop simulation feature of WPILib and the PyBullet Physics Simulator. 

## Design
WPILib desktop simulation has a Websockets interface documented [here](https://github.com/wpilibsuite/allwpilib/blob/main/simulation/halsim_ws_core/doc/hardware_ws_api.md). Control information and sensor inputs at the hardware layer are passed through this websocket server. This program connects to that Websocket server as a client and performs the following actions:
1. Reads control information from the WPILib desktop simulation and sends it to the Bullet Physics Engine
2. Reads joint state information from the Bullet Physics Engine and sends it back to the WPILib desktop simulation as sensor inputs.
To use this program, you need to create a URDF file describing your robot's properties. Instructions for working with URDF files can be found [here](http://wiki.ros.org/urdf/Tutorials)

## Installation 
Note: This project is still under development and a stable version has not been released yet.
1. Install Pybullet
2. Follow WPILib instructions to install WPILib and VSCode

## Usage
In the future, this program will be packaged as a Command Line Interface application, but for now it can be tested by starting the desktop simulation for your robot code, then running the `frcbullet.core.main` python module.
