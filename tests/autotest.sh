#!/bin/bash
set -e

VOLUMES_PATH=/var/mocker/volumes
MOCKER=${1:-mocker}

CGROUP_PREFIX=cgroup_

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
TEST_RESOURCES_DIR=$SCRIPT_DIR/resources
HELLO_DIR=$TEST_RESOURCES_DIR/hello
GOODBYE_DIR=$TEST_RESOURCES_DIR/goodbye
BUSYBOX_DIR=$TEST_RESOURCES_DIR/busybox


function clean() {
    echo "--- Cleaning After Tests ---"
    sudo $MOCKER clean
    echo "--- Cleaned ---"
    echo ""
}


function test_help() {
    echo -e "\n=== Testing help ==="

    $MOCKER help
    echo ""

    clean
}


function test_init() {
    echo -e "\n=== Testing init ==="

    $MOCKER init $HELLO_DIR
    echo "[ls src] $(ls -1 $HELLO_DIR | tr '\n' ' ')"
    echo "[ls img] $(ls -1 $VOLUMES_PATH/img_0 | tr '\n' ' ')"
    echo "[cat .mocker_src] $(cat $VOLUMES_PATH/img_0/.mocker_src)"
    echo ""

    $MOCKER init $GOODBYE_DIR
    echo "[ls src] $(ls -1 $GOODBYE_DIR | tr '\n' ' ')"
    echo "[ls img] $(ls -1 $VOLUMES_PATH/img_1 | tr '\n' ' ')"
    echo "[cat .mocker_src] $(cat $VOLUMES_PATH/img_1/.mocker_src)"
    echo ""

    $MOCKER init $BUSYBOX_DIR
    echo "[ls src] $(ls -1 $BUSYBOX_DIR | tr '\n' ' ')"
    echo "[ls img] $(ls -1 $VOLUMES_PATH/img_2 | tr '\n' ' ')"
    echo "[cat .mocker_src] $(cat $VOLUMES_PATH/img_2/.mocker_src)"
    echo ""

    clean
}

function test_images() {
    echo -e "\n=== Testing images ==="

    $MOCKER images
    echo ""
    $MOCKER init $HELLO_DIR
    echo ""
    $MOCKER images
    echo ""
    $MOCKER init $GOODBYE_DIR
    echo ""
    $MOCKER images
    echo ""
    $MOCKER init $BUSYBOX_DIR
    echo ""
    $MOCKER images
    echo ""

    clean
}

function test_rmi() {
    echo -e "\n=== Testing rmi ==="

    $MOCKER init $HELLO_DIR
    $MOCKER init $HELLO_DIR
    $MOCKER init $HELLO_DIR
    echo ""

    $MOCKER images
    echo ""

    $MOCKER rmi 1
    $MOCKER rmi 0
    echo ""

    $MOCKER images
    echo ""

    clean
}


function test_pull() {
    echo -e "\n=== Testing pull ==="

    $MOCKER pull hello-world
    echo "[ls img] $(ls -1 $VOLUMES_PATH/img_0 | tr '\n' ' ')"
    echo ""

    $MOCKER pull alpine
    echo "[ls img] $(ls -1 $VOLUMES_PATH/img_1 | tr '\n' ' ')"
    echo ""

    clean
}


function test_run() {
    echo -e "\n=== Testing run ==="

    echo "--- Testing run: hello-world ---"
    $MOCKER pull hello-world
    echo ""
    sudo $MOCKER run 0 ./hello
    echo ""

    clean

    echo "--- Testing run: busybox ---"

    $MOCKER init $BUSYBOX_DIR
    echo ""

    sudo $MOCKER run 0 ./busybox ls
    echo "[cat .mocker_cmd] $(cat $VOLUMES_PATH/ps_2/.mocker_cmd)"
    echo ""

    sudo $MOCKER run 0 ./busybox cat download
    echo "[cat .mocker_cmd] $(cat $VOLUMES_PATH/ps_3/.mocker_cmd)"
    echo ""

    echo "--- Testing run: cgroups ---"
    CGROUPS_PATH=/sys/fs/cgroup
    CGROUPS_CPU_PATH=$CGROUPS_PATH/cpu/root
    CGROUPS_MEM_PATH=$CGROUPS_PATH/memory/root

    sudo $MOCKER run 0 ./busybox ls
    CGROUP=${CGROUP_PREFIX}4
    echo "[cat cpu limit] $(cat $CGROUPS_CPU_PATH/$CGROUP/cpu.shares)"
    echo "[cat mem limit] $(cat $CGROUPS_MEM_PATH/$CGROUP/memory.limit_in_bytes)"
    echo ""

    sudo $MOCKER run 0 -c 50 -m 2048 ./busybox ls
    CGROUP=${CGROUP_PREFIX}5
    echo "[cat cpu limit] $(cat $CGROUPS_CPU_PATH/$CGROUP/cpu.shares)"
    echo "[cat mem limit] $(cat $CGROUPS_MEM_PATH/$CGROUP/memory.limit_in_bytes)"
    echo ""

    echo "--- Testing run: netns ---"
    echo "Show interfaces"
    sudo mocker run 0 ./busybox ip address show
    echo ""
    echo "Ping Loopback"
    sudo mocker run 0 -- ./busybox ping -c 3 127.0.0.1
    echo ""
    echo "Ping Self"
    sudo mocker run 0 -- ./busybox ping -c 3 10.0.0.8
    echo ""

    clean

    echo "--- Testing run: alpine ---"
    $MOCKER pull alpine
    echo ""

    sudo $MOCKER run 0 -- ls
    echo ""

    echo "--- Testing run: pid namespace ---"
    sudo $MOCKER run 0 -- ps aux
    echo ""

    clean
}

function test_ps() {
    echo -e "\n=== Testing ps ==="

    $MOCKER init $BUSYBOX_DIR
    echo ""

    $MOCKER ps
    echo ""
    sudo $MOCKER run 0 ./busybox ls
    echo ""
    $MOCKER ps
    echo ""
    sudo $MOCKER run 0 ./busybox cat download
    echo ""
    $MOCKER ps
    echo ""
    sudo $MOCKER run 0 ./busybox ls
    echo ""
    $MOCKER ps
    echo ""

    clean
}

function test_rm() {
    echo -e "\n=== Testing rm ==="

    $MOCKER init $BUSYBOX_DIR
    echo ""

    sudo $MOCKER run 0 ./busybox ls
    sudo $MOCKER run 0 ./busybox ls
    sudo $MOCKER run 0 ./busybox ls
    echo ""

    $MOCKER ps
    echo ""

    sudo $MOCKER rm 2
    sudo $MOCKER rm 4
    echo ""

    $MOCKER ps
    echo ""

    clean
}


function test_logs() {
    echo -e "\n=== Testing logs ==="

    $MOCKER init $BUSYBOX_DIR
    echo ""

    sudo $MOCKER run 0 ./busybox ls
    echo "[cat src]"
    ls -1 $BUSYBOX_DIR
    echo "[cat log]"
    cat $VOLUMES_PATH/ps_2/.log
    echo ""

    sudo $MOCKER run 0 ./busybox cat download
    echo "[cat src] $(cat $BUSYBOX_DIR/download)"
    echo "[cat log] $(cat $VOLUMES_PATH/ps_3/.log)"
    echo ""

    clean
}

function test_commit() {
    echo -e "\n=== Testing commit ==="

    $MOCKER init $BUSYBOX_DIR
    echo "[ls  img dir] $(ls -a1 $VOLUMES_PATH/img_0 | tr '\n' ' ')"
    echo ""

    sudo $MOCKER run 0 ./busybox cat download
    echo ""
    $MOCKER commit 2 0
    echo "[ls  img dir] $(ls -a1 $VOLUMES_PATH/img_0 | tr '\n' ' ')"
    echo "[cat img cmd] $(cat $VOLUMES_PATH/img_0/.mocker_cmd)"
    echo ""

    sudo $MOCKER run 0 ./busybox ls
    echo ""
    $MOCKER commit 3 0
    echo "[ls  img dir] $(ls -a1 $VOLUMES_PATH/img_0 | tr '\n' ' ')"
    echo "[cat img cmd] $(cat $VOLUMES_PATH/img_0/.mocker_cmd)"
    echo ""

    clean
}


function test_exec() {
    echo -e "\n=== Testing exec ==="

    $MOCKER pull alpine
    echo ""

    sudo $MOCKER run 0 -- sleep 5 &
    echo ""
    sleep 1

    sudo $MOCKER exec 2 -- ls -
    echo ""

    sudo $MOCKER exec 2 -- cat /.mocker_cmd
    echo ""

    sudo $MOCKER exec 2 -- ps aux
    echo ""

    sleep 4
    clean
}


test_help

test_init
test_images
test_rmi

test_pull

test_run
test_ps
test_rm

test_logs
test_commit

test_exec
