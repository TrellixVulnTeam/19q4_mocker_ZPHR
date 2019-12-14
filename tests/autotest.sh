#!/bin/bash

BTRFS_PATH=/var/mocker
MOCKER=${1:-mocker}

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
TEST_RESOURCES_DIR=$SCRIPT_DIR/resources
HELLO_DIR=$TEST_RESOURCES_DIR/hello
GOODBYE_DIR=$TEST_RESOURCES_DIR/goodbye


function clean() {
    echo "--- Cleaning After Tests ---"
    btrfs subvolume delete /var/mocker/*
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
    echo "[ls img] $(ls -1 $BTRFS_PATH/img_0 | tr '\n' ' ')"
    echo "[cat .mocker_src] $(cat $BTRFS_PATH/img_0/.mocker_src)"
    echo ""

    $MOCKER init $GOODBYE_DIR
    echo "[ls src] $(ls -1 $GOODBYE_DIR | tr '\n' ' ')"
    echo "[ls img] $(ls -1 $BTRFS_PATH/img_1 | tr '\n' ' ')"
    echo "[cat .mocker_src] $(cat $BTRFS_PATH/img_1/.mocker_src)"
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
    echo "NOT IMPLEMENTED"

    $MOCKER pull hello-world

    clean
}

function test_run() {
    echo -e "\n=== Testing run ==="
    echo "NOT IMPLEMENTED"

    #$MOCKER run

    clean
}

function test_ps() {
    echo -e "\n=== Testing ps ==="
    echo "NOT IMPLEMENTED"

    #$MOCKER ps

    clean
}

function test_rm() {
    echo -e "\n=== Testing rm ==="
    echo "NOT IMPLEMENTED"

    #$MOCKER rm

    clean
}

function test_logs() {
    echo -e "\n=== Testing logs ==="
    echo "NOT IMPLEMENTED"

    #$MOCKER logs

    clean
}

function test_exec() {
    echo -e "\n=== Testing exec ==="
    echo "NOT IMPLEMENTED"

    #$MOCKER exec

    clean
}

function test_commit() {
    echo -e "\n=== Testing commit ==="
    echo "NOT IMPLEMENTED"

    #$MOCKER commit

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
test_exec

test_commit
