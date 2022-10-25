#!/usr/bin/envpython
from flask import *
import argparse
import sys
import os
import validateIP
import re
import sshinfo
from netmiko import *
import json
import random
import requests

app = Flask(__name__)

page = "1"
StaticFlow = {"DPID": "switch", "DestIP": "ipv4_dst", "SourceIP": "ipv4_src", "InPort": "in_port"}
url = 'http://192.168.56.4:8080/wm/staticflowpusher/json'


def CheckConditions(form):
    if 'SourceIP' in form and form['SourceIP'] != '':
        print(form['SourceIP'])
        valid = validateIP.validate_IP(str(form['SourceIP']))
        if not valid:
            return (1)
    if 'DestIP' in form and form['DestIP'] != '':
        valid = validateIP.validate_IP(str(form['DestIP']))
        if not valid:
            return (2)
    if 'DPID' in form and form['DPID'] == '' and form['selection'] == 'Static':
        return (3)
    elif 'DPID' in form:
        DPID = re.findall('([0-9 A-F][0-9 A-F][:]*)', str(form['DPID']))
        if len(DPID) != 8 and form['selection'] == 'Static':
            return (3)
        else:
            return (form)


def sendCurl(data, curlurl=url):
    print(data)
    for x in data:
        print(x)
        response = requests.post(curlurl, data='{}'.format(x))
    return (response)


@app.route('/', methods=['GET', 'POST'])
def index():
    global page
    try:

        if request.form['page']:
            page = request.form['page']
            print(page)
    except:
        pass
    if page == "1":

        return render_template('index.html', page="1")
    elif page == "2":

        selection = request.form['selection']
        if selection == "Static Flows":
            return render_template('index.html', page="2", selection='Static', output="0")
        elif selection == "Firewall":
            curlCommand = []
            curlCommand.append(json.dumps({"switch": "00:00:00:00:00:00:00:01", "name": "firewall11", "priority": 500}))
            curlCommand.append(json.dumps({"switch": "00:00:00:00:00:00:00:02", "name": "firewall22", "priority": 500}))
            output = sendCurl(curlCommand)
            return render_template('index.html', page="2", selection='Firewall', output="0")
    else:
        Attributes = {}
        form = request.form
        if form['Protocol'].lower() not in ['arp', 'ipv4', 'tcp', 'udp']:
            return render_template('index.html', page="2", selection=form['selection'], output=str(4))

        output = CheckConditions(form)
        if output != form:
            if output == 1:
                return render_template('index.html', page="2", selection=form['selection'], output=str(output))
            elif output == 2:
                return render_template('index.html', page="2", selection=form['selection'], output=str(output))
            elif output == 3:
                return render_template('index.html', page="2", selection=form['selection'], output=str(output))

        for x in form:
            if x not in ['selection', 'page'] and form[x] != '':

                if x in StaticFlow:

                    try:
                        Attributes[StaticFlow[x]] = int(form[x])
                    except ValueError:
                        Attributes[StaticFlow[x]] = str(form[x])

                else:
                    if x == 'Protocol':
                        if form['Protocol'].lower() in ['ipv4', 'tcp', 'udp']:
                            Attributes['eth_type'] = '0x0800'
                            if form['Protocol'].lower() == 'tcp':
                                Attributes['ip_proto'] = '0x06'
                            elif form['Protocol'].lower() == 'udp':
                                Attributes['ip_proto'] = '0x11'

                        else:
                            Attributes['eth_type'] = '0x0806'

                        continue
                    try:
                        Attributes[x] = int(form[x])
                    except ValueError:
                        Attributes[x] = str(form[x])
            elif x == 'Name':
                Attributes[x] = str(random.randint(1, 1000000000000))

        print(Attributes)
        Attributes = json.dumps(Attributes)

        # curlCommand = []
        # curlCommand.append("curl -X POST -d '{}' http://192.168.56.4:8080/wm/staticflowpusher/json".format(Attributes))
        output = sendCurl([Attributes])

        return render_template('index.html', page="2", selection=form['selection'], output=str(output))


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)
