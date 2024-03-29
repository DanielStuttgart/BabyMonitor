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

Look for record device `arecord -l`
```
**** Liste der Hardware-Geräte (CAPTURE) ****
Karte 1: GoMic [Samson GoMic], Gerät 0: USB Audio [USB Audio]
  Sub-Geräte: 1/1
  Sub-Gerät #0: subdevice #0
```
This means, --alsadev hw:1,0` is used.

## Setup PiCam Module
[Link to PiCam-Github](https://github.com/iizukanao/picam.git)
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
HTML-Folder `/var/www/html`

### Player for HLS 
```bash
cd /var/www/html
sudo git clone https://github.com/kamranayub/picam-viewer.git .
./picam -o /run/shm/hls --alsadev hw:1,0
```
For more details see https://docs.videojs.com/

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
cd ~/node-rtsp-rtmp-server
./start_server.sh &
```
Start PiCam `./picam --alsadev hw:2,0 --rtspout -w 800 -h 480 -v 500000 -f 20 &`
Start PiCam `./picam --alsadev hw:1,0 --rtspout -w 800 -h 480 -v 500000 -f 20 --hooksdir /var/www/html/hooks`

Show strem `rtsp://192.168.1.3:80/live/picam`

The RTSP-/RTMP-Server supports HTML-server and RTMP-server as well. If you are using NGINX, it will not be possible to post both streams onto HTTP-Port 80. You can deactivate NGiNX by ```sudo /etc/init.d/nginx stop```. You can as well change the *config.coffee*-file and set HTTP- / RTMP-Server to false. The custom receiver needs to be set to true. I changed the server port to ```8080``` s.t. NGINX server can be run in parallel.

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

Add process to startup: 
/etc/rc.local

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

### Build from sources
```
sudo apt-get install git libasound2-dev libssl-dev libfontconfig1-dev libharfbuzz-dev
wget -O fdk-aac-2.0.1.tar.gz https://sourceforge.net/projects/opencore-amr/files/fdk-aac/fdk-aac-2.0.1.tar.gz

tar zxvf fdk-aac-0.1.6.tar.gz
cd fdk-aac-0.1.6
./configure
make -j4
 (takes 3-4 minutes)
sudo make install

git clone https://git.ffmpeg.org/ffmpeg.git
cd ffmpeg
./configure --enable-libfdk-aac 
  (old, some problems with definitions)
./configure --extra-ldflags="-latomic" --arch=armel --target-os=linux --enable-gpl --enable-omx --enable-omx-rpi --enable-nonfree --enable-libfdk-aac
(takes about one minute)
make -j4
sudo make install

sudo ldconfig

cd /opt/vc/src/hello_pi/libs/ilclient
make

git clone https://github.com/iizukanao/picam.git
cd picam
make -j4
  (I encountered a problem with latomic (__atomic_store_8 undefined), so I added -latomic to LDFLAGS in Makefile)
```

## GUI by Server 
[GitHUB-Homepage D3](https://github.com/d3/d3)
[Project Homepage D3](https://d3js.org/)

## Temperature
![alt text](https://raw.githubusercontent.com/DanielStuttgart/BabyMonitor/master/temperature/luftfeuchtigkeit_DHT11_Steckplatine.png "Bread Board Layout DHT22 from [Tutorial](https://tutorials-raspberrypi.de/raspberry-pi-luftfeuchtigkeit-temperatur-messen-dht11-dht22/)")
Bread Board Layout DHT22 from [Tutorial](https://tutorials-raspberrypi.de/raspberry-pi-luftfeuchtigkeit-temperatur-messen-dht11-dht22/)
Install AdaFruit-Libraries for DHT22
```bash
git clone https://github.com/adafruit/Adafruit_Python_DHT.git && cd Adafruit_Python_DHT
sudo python setup.py install
```
```bash
cd examples
sudo ./AdafruitDHT.py 22 4
```
```python
import sys
import Adafruit_DHT
sensor = 22     # sensor DHT22 (alternatives 11 (DHT11), 2302 (DHT.AM2302))
pin = 4         # GPIO Pin used for signal-

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
else:
    print('Failed to get reading. Try again!')
    sys.exit(1)
```
In order to work with a local CSV file as a ring puffer, PANDAS is used. To install, use ```sudo apt-get install python-pandas```.

CSV ring puffer: 
```python
csv = pd.read_csv('/var/www/html/temp.csv')
if len(csv_new > 2000)
    csv = csv.drop(csv.index[0])
new_row = {'date': '02.08.2020-10:30:50', 'temperature': 20.0, 'humidity': 80.}
csv_new.append(new_row, ignore_index=True)
csv_new.to_csv('output.csv',index=False)
```

## Server
Files for server configuration
* config.coffee: configuration file for node-rtsp-rtmp-server
* default: configuration nginx (```/etc/nginx/sites-available/default```)
* nginx.conf: configuration nginx (```/etc/nginx/nginx.conf```)
Needed to add write access to www-user by ```chmod -R 777```
Added PHP-support by 
* ```sudo apt install php-fpm```
* add index.php to ```sites-enabled/default```
* uncoment PHP-section within ```sites-enabled/default```
* restart nginx ```sudo /etc/init.d/nginx reload``

## Misc
### Networking
Add Wifi-networks to Raspberry Pi without monitor: change ```/boot/wpa_supplicant.conf```
```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=DE

network={
 ssid="DanielsMate20Pro"
 psk="xxx"
 id_str="mobile"
}
network={
 ssid="o2-WLAN87_2"
 psk="xxx"
 id_str="home"
}
```
This file is copied to /etc/wpa_supplicant.conf afterwards. For converting to HEX, use echo "Réseau de XL1" | xxd -p | tr a-z A-Z 
For finding IP address, use nmap -sp 192.100.1.1/24

### Debugging
In order to start GDB, type ```gdb <program_executable>```
```
r [arg1] [arg2] # run program with 2x arguments; r == run
step / s # steps into function / executes line
next / n # step over function
continue / c # continue executing
break [filename]:[linenumer] # 
list # list source code around break point
run / r # run program
print [variable] # print variable content
set [variable] = [value] # set var to value
```

### Install geany with Debugging-Plugin for Raspberry Pi OS Buster
Information taken from [Forum](https://forum-raspberrypi.de/forum/thread/46925-geany-plugin-debugger-fuer-raspbian-buster-nachruesten/)
```
Base OS Image:Raspbian  2020-02-13-raspbian-buster.img

Source code:
The source code downloaded from https://github.com/geany will fail.
Also you cannot install from apt-get repositry.
Please follow to the following instruction.

Important:
In the geany plugin configuration, the extract destination is "/usr/local" by default, so set this to "/usr".

1. Purge geany
$ sudo apt-get purge -y geany*

2. Additional library instalation 
$ sudo apt-get install -y libgtk-3-dev
$ sudo apt-get install -y intltool
$ sudo apt-get install -y libvte-2.91-dev

3. *** Geany install ***

### make dir on /home/pi/Downloads ###
pi@raspberrypi:~ $ cd Downloads
pi@raspberrypi:~/Downloads $ mkdir geany-1.36
pi@raspberrypi:~/Downloads $ mkdir geany-plugins

pi@raspberrypi:~/Downloads $ cd geany-1.36
pi@raspberrypi:~/Downloads/geany-1.36 $ wget https://download.geany.org/geany-1.36.tar.gz
pi@raspberrypi:~/Downloads/geany-1.36 $ tar -zxvf geany-1.36.tar.gz
pi@raspberrypi:~/Downloads/geany-1.36 $ cd geany-1.36
pi@raspberrypi:~/Downloads/geany-1.36/geany-1.36 $ ./configure
pi@raspberrypi:~/Downloads/geany-1.36/geany-1.36 $ make
pi@raspberrypi:~/Downloads/geany-1.36/geany-1.36 $ sudo make install

4. *** Geany Plugin install ***
pi@raspberrypi:~/Downloads $  cd /home/pi/Downloads/geany-plugins
pi@raspberrypi:~/Downloads/geany-plugins $ wget https://plugins.geany.org/geany-plugins/geany-plugins-1.36.tar.gz
pi@raspberrypi:~/Downloads/geany-1.36 $ tar -zxvf geany-plugins-1.36.tar.gz
pi@raspberrypi:~/Downloads/geany-1.36 $ cd geany-plugins-1.36
pi@raspberrypi:~/Downloads/geany-plugins/geany-plugins-1.36 $ ./configure --prefix=/usr
pi@raspberrypi:~/Downloads/geany-1.36/geany-1.36 $ make
pi@raspberrypi:~/Downloads/geany-1.36/geany-1.36 $ sudo make install

$sudo reboot
```

Kill Python Processes: sudo pkill pyhon
rc-local: sudo nano /etc/rc.local
