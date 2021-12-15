#!/bin/bash

set -e
set -x

export GLOG_logtostderr=1
export GLOG_v=2
wget http://mobvoi-speech-public.ufile.ucloud.cn/public/wenet/test.wav
wav_path=./test.wav
./build/websocket_client_main \
    --host 127.0.0.1 \
    --port 10086 \
    --wav_path $wav_path 2>&1 | tee websocket_client.log


