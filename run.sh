#!/bin/bash
/opt/Monitoring/nodeExporter/node_exporter >/dev/null 2>&1 & 
/opt/Monitoring/cadvisor/cadvisor >/dev/null 2>&1 &  
cd /opt/Monitoring/nodeCollector
sleep 5 &&
python node_collector.py  >/dev/null 2>&1 &

tail -f /dev/null
