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

Control PiCam
```bash
start/stop Picam recording
touch hooks/start_record
touch hooks/stop_record

```

### Install nginx server
```bash
install nginx
sudo apt-get install nginx
sudo nano /etc/nginx/sites-available/default
```
Start server 
```bash
sudo /etc/init.d/nginx start
sudo service nginx restart
```

### Player for HLS 
```bash
cd /var/www/html
sudo git clone https://github.com/kamranayub/picam-viewer.git .
```

### HLS-Streaming
Change nginx to stream rtmp (*/etc/nginx/sites-available/default*) 
```bash
location /hls/ {
    root /run/shm;
}
```

### RTSP-Streaming
For further [details](https://hmbd.wordpress.com/2016/08/01/raspberry-pi-video-and-audio-recording-and-streaming-guide/)
Setup
```bash
sudo apt-get install npm
sudo npm install coffee-script -g
git clone https://github.com/iizukanao/node-rtsp-rtmp-server.git
cd node-rtsp-rtmp-server
npm install -d
sudo /etc/init.d/nginx stop
cd ~/node-rtsp-rtmp-server
./start_server.sh &
```
Start PiCam `./picam --alsadev hw:2,0 --rtspout -w 800 -h 480 -v 500000 -f 20 &`

Show strem `rtsp://192.168.1.3:80/live/picam`

### RTMP-Streaming with nginx
```bash
which ffmpeg --> /usr/bin/ffmpeg # find path to ffmpeg
sudo apt-get update
sudo apt-get install libnginx-mod-rtmp
```
Change nginx to stream rtmp (*nginx.conf*)
```bash
rtmp {
    server {
        listen 1935;
        chunk_size 4000;
        application webcam {
            live on;

            exec_static /path/to/ffmpeg -i tcp://127.0.0.1:8181?listen
                                        -c:v copy -ar 44100 -ab 40000
                                        -f flv rtmp://localhost:1935/webcam/mystream;
        }
    }
}
```
Start PiCam `./picam --alsadev hw:2,0 --tcpout tcp://127.0.0.1:8181 -w 800 -h 480 -v 500000 -f 20`

Show stream `rtmp://192.168.1.3/webcam/mystream`

### Evaluation
With my configuration with
* Raspberry Pi 2 B
* Raspberry Pi Camea Module
* external USB Microphone Samson
* USB WiFi Module

I got following result (ordered by latency from low to high)
1. RTSP
2. RTMP
3. HLS
