#!/usr/bin/bash

set -e
set -x

model_dir=$PWD/20210602_unified_transformer_server
docker run -it -p 10086:10086 -v $model_dir:/home/wenet/model mobvoiwenet/wenet:mini bash /home/run.sh

