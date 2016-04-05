# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="panos"
__date__ ="$Apr 5, 2016 1:21:16 PM$"
import json,urllib2, base64
import datetime,time,logging
from logging.handlers import RotatingFileHandler
import time, threading
from configure import configuration


def init():
    global prometh_server
    global cadvisor
    global node_name
    global node_exporter
    global logger
        
    #read configuration
    conf = configuration("node.conf")
    cadvisor = conf.ConfigSectionMap("vm_node")['cadvisor']
    prometh_server = conf.ConfigSectionMap("Prometheus")['server_url']
    node_name = conf.ConfigSectionMap("vm_node")['node_name']
    node_exporter = conf.ConfigSectionMap("vm_node")['node_exporter']

    logger = logging.getLogger('dataCollector')
    hdlr = RotatingFileHandler('dataCollector.log', maxBytes=10000, backupCount=5)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.WARNING)
    logger.setLevel(logging.INFO)
    logger.info('Node Data Collector')
    logger.info('Promth Server '+prometh_server)
    logger.info('Monitoring Node '+node_name)


def getData(exporter_):
    try: 
        url = "http://"+exporter_+"/metrics"
        req = urllib2.Request(url)
        response=urllib2.urlopen(req)
        code = response.code
        logger.info('Response code from: '+exporter_+'('+str(code)+')')
        data = response.read()
        return data
        
    except urllib2.HTTPError, e:

        logger.warning('Error: '+str(e))
    except urllib2.URLError, e:

        logger.warning('Error: '+str(e))
    except ValueError, e:

        logger.warning('Error: '+str(e))
        
def postNode(node_,type_, data_):
    url = prometh_server+"/job/"+type_+"/instance/"+node_
    
    logger.info('Post on: \n'+url)
    
    try: 
        req = urllib2.Request(url)
        req.add_header('Content-Type','text/html')
        req.get_method = lambda: 'PUT'
        response=urllib2.urlopen(req,data_)
        code = response.code
        logger.info('Response Code: '+str(code))      
    except urllib2.HTTPError, e:
        logger.warning('Error: '+str(e))
    except urllib2.URLError, e:
        logger.warning('Error: '+str(e))

def collectData():
    cAd_dt = getData(cadvisor)
    Nd_dt = getData(node_exporter)
    postNode(node_name,"containers",cAd_dt)
    postNode(node_name,"vm",Nd_dt)
    threading.Timer(3, collectData).start()



if __name__ == "__main__":
    init()
    collectData()

