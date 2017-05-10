export PYTHONPATH=$(cd ..; pwd)
cd ../src/monitor/
nohup python3.5 run.py >> $PYTHONPATH/logs/monitor.log &
nohup python3.5 -u run_tcp_server.py >> $PYTHONPATH/logs/monitor_tcp.log &
