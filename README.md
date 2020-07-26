# BabyMonitor
Baby Monitor with camera, microphone, temperature and GUI modules

## General Setup for Raspberry PI

### Setup SSH and Camera @ Raspberry PI
Go to **Raspberry PI Configuration**, then **Interfaces** and set **SSH** and **Camera** to *activated*. 

### Connect via SSH
Use *ssh*-command:
```bash
ssh pi@<ip-address>
ssh -Y piq<ip-address> # for x-Window-support
```
### Copy files by command
Syntax:
```bash
scp <source> <destination>
```
To copy a file from B to A while logged into B:
```bash
scp /path/to/file username@a:/path/to/destination
```
To copy a file from B to A while logged into A:
```bash
scp username@b:/path/to/file /path/to/destination
```
### Copy files by mounting Raspberry locally
Install `sudo apt-get install sshfs`
Connect `sshfs pi@<ip-address>:/folder/on/pi /folder/on/local`
Unmount `fusermount -u ~/raspberry`

### Setup Audio
List usb-devices to get Audio ID `lsusb -t`
Install LibAudio `sudo apt-get install libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev`
Install pyAduio `sudo pip3 install pyaudio`

## Setup PiCam Module
GIT-clone `git clone https://github.com/iizukanao/picam.git`
Run with Audio-Device and resolution 640 x 480 `./picam --alsadev hw:2,0 -w 640 -h 480`
