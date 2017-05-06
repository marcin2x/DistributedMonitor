export PYTHONPATH=$(cd ..; pwd)
cd ../src/authentication_service/
nohup python3.5 run.py >> $PYTHONPATH/logs/auth.log &
