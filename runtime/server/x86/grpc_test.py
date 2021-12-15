"""
python -m grpc_tools.protoc --python_out=. --grpc_python_out=. -I. proto/wenet.proto
"""

import sys
import os
import json
import time
import logging
import grpc
import uuid
import wave
from google.protobuf.json_format import MessageToJson
from pprint import pprint

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from proto.wenet_pb2 import Request
from proto.wenet_pb2_grpc import ASRStub

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

GRPC_SERVICE_ADDR = '127.0.0.1:10086'
SEND_FRAME_SIZE = 16000  # 500ms
SEND_WAIT_SECOND = 0.5  # s


def get_audio_data_without_header(wav_file):
    audio_size = 0  # default
    with wave.open(wav_file, 'rb') as f:
        sampwidth = f.getsampwidth()
        nframes = f.getnframes()
        framerate = f.getframerate()
        assert framerate == 16000, 'frame rate must be 16000, {}'.format(framerate)
        audio_size = nframes * sampwidth

    with open(wav_file, 'rb') as f:
        data = f.read()
    header_size = len(data) - audio_size
    logger.debug("wav header: {}".format(header_size))
    return data[header_size:]


def grpc_test(wav_file):
    audio_data = get_audio_data_without_header(wav_file)

    channel = grpc.insecure_channel(GRPC_SERVICE_ADDR)
    stub = ASRStub(channel)

    def generate_request():
        off, size = 0, SEND_FRAME_SIZE
        start_flag = False
        while off < len(audio_data):
            if not start_flag:
                req = Request(decode_config=Request.DecodeConfig(nbest_config=1, continuous_decoding_config=False))
                start_flag = True
            else:
                if len(audio_data) <= off + size:
                    size = len(audio_data) - off
                au_data = audio_data[off:off + size]
                off += size
                req = Request(audio_data=au_data)
                # time.sleep(SEND_WAIT_SECOND)
            yield req

    t0 = time.time()
    for rsp in stub.Recognize(generate_request()):
        t1 = time.time()
        print("time cost: {:.5f} ms".format((t1 - t0) * 1000))
        t0 = time.time()

    serialized = MessageToJson(rsp)
    result = json.loads(serialized)
    print("result sentence:", result['nbest'][0]['sentence'])

    channel.close()


if __name__ == '__main__':
    grpc_test("./test.wav")
