#!/bin/bash

. /etc/init.d/functions
export PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/opt/node/bin

base_dir=$(dirname $0)
PROC_NAME="opsap"
lockfile=/var/lock/subsys/${PROC_NAME}


start() {
    srv_start=$"Starting ${PROC_NAME} service:"

    if [ -f $lockfile ];then    
        echo "${PROC_NAME}  is running..."
        success "$srv_start"
    else
        daemon python $base_dir/manage.py runserver 0.0.0.0:80 &>> /tmp/opsap_runserver.log 2>&1 &
        daemon python $base_dir/manage.py celery worker -c 2 -l info &>> /tmp/opsap_celery.log 2>&1 &
        sleep 3

        echo -n "$srv_start"
        nums=0
        for i in runserver celery;do
            ps aux | grep "$i" | grep -v 'grep' &> /dev/null && let nums+=1  || echo "$i not running"
        done

        if [ "x$nums" == "x2" ];then
            success "$srv_start"
            touch "$lockfile"
            echo
        else
            failure "$srv_start"
            echo
        fi
    fi    
}


stop() {
    echo -n $"Stopping ${PROC_NAME} service:"

    ps aux | grep -E 'manage.py' | grep -v grep | awk '{print $2}' | xargs kill -15 &> /dev/null
    ret=$?

    if [ $ret -eq 0 ]; then
        echo_success
        echo
        rm -f "$lockfile"
    else
        echo_failure
        echo
        rm -f "$lockfile"
    fi
}


restart(){
    stop
    start
}


# See how we were called.
case "$1" in    
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    *)
        echo $"Usage: $0 {start|stop|restart}"
        exit 2
esac
