#! /bin/sh
rm -rf myapp.log
ps -ef | grep start_new.py | grep -v grep | awk  '{print $2}' | xargs  kill -9 >/dev/null 2>&1
python start_new.py
