import sys
import os
import logging
import time
import uuid
import wave
import json
import grpc
import grpc.experimental.gevent as grpc_gevent
from google.protobuf.json_format import MessageToJson

from locust import events, User, task
from locust.exception import LocustError
from locust.contrib.fasthttp import FastHttpUser

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from proto.wenet_pb2 import Request
from proto.wenet_pb2_grpc import ASRStub

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

grpc_gevent.init_gevent()

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


audio_data = get_audio_data_without_header("./test.wav")


class GrpcClient(object):

    def __init__(self, stub):
        self._stub_class = stub.__class__
        self._stub = stub

    def __getattr__(self, name):
        func = self._stub_class.__getattribute__(self._stub, name)

        def wrapper(*args, **kwargs):
            request_meta = {
                "request_type": "asr_grpc",
                "name": name,
                "response_length": 0,
                "response": None,
                "exception": None,
                "context": None,
            }

            try:
                t0 = time.perf_counter()
                response = func(*args, **kwargs)
                tr = (time.perf_counter() - t0) * 1000

                # if RPC streaming iterator
                if isinstance(response, grpc._channel._MultiThreadedRendezvous):
                    rsp_list = []
                    t0 = time.perf_counter()
                    for i, rsp in enumerate(response):
                        request_meta["response_time"] = (time.perf_counter() - t0) * 1000
                        request_meta["name"] = name
                        events.request.fire(**request_meta)

                        rsp_list.append(rsp)
                        t0 = time.monotonic()
                    request_meta["response"] = rsp_list
                    request_meta["response_length"] = len(request_meta["response"])
                else:
                    request_meta["response"] = response
                    request_meta["response_time"] = tr
            except grpc.RpcError as e:
                logger.error(f"=> Error on call {name}")
                request_meta["exception"] = e

            events.request.fire(**request_meta)
            return request_meta["response"]

        return wrapper


class GrpcEvent(User):
    # If abstract is True, the class is meant to be subclassed, and locust will not
    # spawn users of this class during a test.
    abstract = True
    stub_class = None

    def __init__(self, environment):
        super().__init__(environment)
        for attr_value, attr_name in ((self.host, "host"), (self.stub_class, "stub_class")):
            if attr_value is None:
                raise LocustError(f"You must specify the {attr_name}.")
        self._channel = grpc.insecure_channel(self.host)
        self._channel_closed = False
        stub = self.stub_class(self._channel)
        self.client = GrpcClient(stub)

    def stop(self, force=False):
        self._channel_closed = True
        time.sleep(1)
        self._channel.close()
        super().stop(force=True)


class ASRGrpcEvent(GrpcEvent):
    host = GRPC_SERVICE_ADDR
    stub_class = ASRStub
    count = 0

    @task
    def asr_task(self):
        if not self._channel_closed:

            def generate_request():
                off, size = 0, SEND_FRAME_SIZE
                start_flag = False
                while off < len(audio_data):
                    if not start_flag:
                        req = Request(
                            decode_config=Request.DecodeConfig(nbest_config=1, continuous_decoding_config=False))
                        start_flag = True
                    else:
                        if len(audio_data) <= off + size:
                            size = len(audio_data) - off
                        au_data = audio_data[off:off + size]
                        off += size
                        req = Request(audio_data=au_data)
                        time.sleep(SEND_WAIT_SECOND)
                    yield req

            t0 = time.time()
            for rsp in self.client.Recognize(generate_request()):
                t1 = time.time()
                # print("time cost: {:.5f} ms".format((t1 - t0) * 1000))
                # t0 = time.time()

            serialized = MessageToJson(rsp)
            result = json.loads(serialized)
            print("result sentence:", result['nbest'][0]['sentence'])
        print("\n")
