from homeauto import app
from flask import redirect, render_template, request, url_for

import os

import serial
import eiscp
import time
import subprocess

# Get the Onkyo
r = eiscp.eISCP(eiscp.eISCP.discover()[0].host)

# get the Projector
s = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

#enable adb server
os.system("adb start-server")

firetv_events = {
    'up':'19',
    'down':'20',
    'left':'21',
    'right':'22',
    'enter':'66',
    'back':'4',
    'home':'3',
    'menu':'1',
    'play':'85',
    'pause':'85',
    'prev':'88',
    'previous':'88',
    'next':'87',
    }


def status(s, command):
    b = b''
    cmd = '\r*' + command + '#\r'
    
    s.write(cmd.encode('ascii'))
    time.sleep(1)
    while s.inWaiting() > 0:
        b += s.read()
    return b

@app.route('/')
def index():
    return render_template('index.jade')

# Projector API

@app.route('/api/v1/projector/proj_power')
def proj_power():
    pwr = request.args.get('pwr')
    if not pwr:
        pwr = 'off'

    return_status = status(s, 'pow=' + pwr)
    return return_status

@app.route('/api/v1/projector/proj_eco')
def proj_eco():
    proj_eco = request.args.get('proj_eco')
    if not proj_eco:
        proj_eco = 'on'

    return_status = status(s, 'blank=' + proj_eco)
    return return_status

# Onkyo API

@app.route('/api/v1/onkyo/onkyo_pwr')
def onkyo_power():
    pwr = request.args.get('pwr')
    if not pwr:
        pwr = 'standby'

    return_status = r.command('system-power ' + pwr)
    print(return_status)
    return str(return_status[1])

@app.route('/api/v1/onkyo/onkyo_src')
def onkyo_source():
    pwr = request.args.get('src')
    if not pwr:
        pwr = 'cbl'

    return_status = r.command('input-selector ' + pwr)
    print(return_status)
    return str(return_status[1])

@app.route('/api/v1/onkyo/onkyo_vol')
def onkyo_volume():
    vol = request.args.get('vol')
    if not vol:
        vol = '20'

    return_status = r.command('master-volume ' + vol)
    print(int(return_status[1],16))
    return str(int(return_status[1],16))

# Control FiteTV Devices
@app.route('/api/v1/amazon/firetv/device_query')
def get_connected_device():
    return  str(subprocess.check_output(['adb', 'devices'])).split('\\n')[1].split('\\t')[0]

@app.route('/api/v1/amazon/firetv/connect')
def connect_firetv():
    ipaddress = request.args.get('ip')
    if not ipaddress:
        return 'failed'
    
    return str(subprocess.check_output(['adb', 'connect', ipaddress]))

@app.route('/api/v1/amazon/firetv/disconnect')
def disconnect_firetv():
    ipaddress = request.args.get('ip')
    if not ipaddress:
        return 'failed'
    
    return str(subprocess.check_output(['adb', 'disconnect', ipaddress]))

@app.route('/api/v1/amazon/firetv/control')
def control_firetv():
    event_id = firetv_events[request.args.get('event')] 

    return str(subprocess.check_output(['adb', 'shell', 'input', 'keyevent', event_id]))

