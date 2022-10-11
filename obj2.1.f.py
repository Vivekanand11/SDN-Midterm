from pyparsing import html
from flask import Flask, render_template
from scapy.all import *
import regex
from scapy.contrib.openflow import OpenFlow
import numpy as np
import pandas
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/test', methods=['POST', 'GET'])
def chartTest():
  read_packets = rdpcap('vivek.pcap')
  print(read_packets)
  a=[]

  for i in read_packets:

    b=i.show(dump=True)
    if "type      = OFPT_PACKET_IN" in b:
      l=regex.findall("len       = \d+",b)
      a.append(l[1])

  data={}
  for i in range(len(a)):
    data[i]=int(a[i].split('=')[1])

  plt.plot(list(data.keys()),list(data.values()))
  plt.xlabel('packet_in count')
  plt.ylabel('packet_count')
  plt.savefig('./static/images/new_plot1.png')

  return render_template('untitled1.html', name = 'new_plot', url ='/static/images/new_plot1.png')

if __name__ == '__main__':
   app.run(debug=True)

