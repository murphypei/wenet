#!/usr/bin/bash

set -e
set -x

export GLOG_logtostderr=1
export GLOG_v=2

wav_path=./test.wav

./build/grpc_client_main \
    --host 127.0.0.1 --port 10086 \
    --wav_path $wav_path 2>&1 | tee grpc_client.log


