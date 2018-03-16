#! /bin/sh
ps -ef | grep start_old.py | grep -v grep | awk  '{print $2}' | xargs  kill -9 >/dev/null 2>&1
rm -rf myapp.log
python start_old.py
