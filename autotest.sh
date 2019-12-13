#!/bin/bash

MOCKER=./mocker.py
IMAGE_ID=12345
CONTAINER_ID=67890

$MOCKER init directory
echo ""

$MOCKER pull image
echo ""

$MOCKER rmi $IMAGE_ID
echo ""

$MOCKER images
echo ""

$MOCKER ps
echo ""

$MOCKER run $IMAGE_ID command command_arg1 command_arg2 command_arg3
echo ""

$MOCKER exec $CONTAINER_ID command command_arg1 command_arg2 command_arg3
echo ""

$MOCKER logs $CONTAINER_ID
echo ""

$MOCKER rm $CONTAINER_ID
echo ""

$MOCKER commit $CONTAINER_ID $IMAGE_ID
echo ""

$MOCKER help
echo ""
