# Football Player Robot - Raspberry Pi

A robotic football player built using Raspberry Pi 4, controlled via VNC and programmed in Python. This project was developed as part of a robotics course in Fall 2023.

## 👥 Team Members

- **Amir Ali Mirzaei**
- **Mahdi Borhani**
- **Esmaeil Bagheri**
- **Babak Fathi**

## 📋 Hardware Requirements

### Main Components:
1. **Metal Chassis and Wheels** - 7 chassis pieces (6 bent pieces and 1 flat piece)
2. **DC Motors** - For robot movement
3. **Servo Motors** - For ball manipulation and control
4. **Raspberry Pi 4** - Main controller board
5. **Motor Driver** - For controlling DC motors
6. **Power Supply** - Battery pack for powering the robot
7. **Screws and Spacers** - For mounting electronic components (spacers needed for metal chassis to prevent short circuits; not required for plastic chassis)

## 🔧 Software Requirements

- Raspberry Pi OS
- Python 3.x
- VNC Server (for remote access)
- VNC Viewer (for computer-side remote control)
- RPi.GPIO library

## 🚀 Setup Instructions

### 1. Raspberry Pi OS Installation

1. Insert your SD card into an SD card reader and connect it to your computer
2. Open Raspberry Pi Imager program
3. Select the desired operating system for installation
4. Select your memory card in the software
5. Choose the "write" option (this may take a few minutes)

### 2. VNC Setup for Remote Access

**On Raspberry Pi:**
```bash
# Install VNC Server
sudo apt-get install real-vnc-server

# Update system
sudo apt-get update

# Enable VNC through configuration
sudo raspi-config

Navigate to Interface Options → VNC → Enable

**On Your Computer:**
1. Install VNC Viewer
2. Enter the Raspberry Pi's IP address in VNC Viewer
3. Login with your Raspberry Pi username and password
4. Access your Raspberry Pi system remotely

### 3. GPIO Setup

The project uses GPIO BCM mode for pin configuration. All required pins are initialized in the `MyController` class, including:
- DC motor control pins
- Servo motor control pins
- Sensor input pins (if applicable)

## 📁 Project Structure


footballplayer-raspberry-pi--main/
├── final.py                    # Main Python code (194 lines)
├── Document(english).pdf       # English documentation
├── document(persian).pdf       # Persian documentation
└── README.md                   # This file

## 🎮 Robot Functionality

The robot includes the following movement capabilities:
- **Forward/Backward movement**
- **Right turn rotation**
- **Left turn rotation**
- **Servo-controlled ball handling**

All movements are controlled through the `MyController` class which manages GPIO pins and motor operations.

## 💻 Running the Code

bash
# Navigate to project directory
cd footballplayer-raspberry-pi--main

# Run the main program
python3 final.py

## 📖 Code Structure

The main code (`final.py`) consists of:
- **MyController Class**: Handles GPIO setup and initialization
- **Motor Control Functions**: Manage DC motor movements
- **Servo Control Functions**: Control servo motors for ball manipulation
- **Main Function**: Coordinates robot behavior and decision-making

## 🔌 GPIO Pin Configuration

All pins are configured in BCM mode. Refer to the code comments in `final.py` for specific pin assignments.

## 📚 Documentation

For detailed hardware assembly, circuit diagrams, and in-depth code explanations, please refer to:
- `Document(english).pdf` - Complete English documentation
- `document(persian).pdf` - Complete Persian documentation
