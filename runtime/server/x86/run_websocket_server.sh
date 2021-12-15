#!/bin/bash 

set -e
set -x

export GLOG_logtostderr=1
export GLOG_v=2
model_dir=./20210602_unified_transformer_server
./build/websocket_server_main \
    --port 10086 \
    --chunk_size 16 \
    --model_path $model_dir/final.zip \
    --dict_path $model_dir/words.txt 2>&1 | tee websocket_server.log

