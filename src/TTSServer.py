import torch
from TTS.api import TTS

import socket
from threading import Thread

import sounddevice
import soundfile
# from rvc_infer import rvc_convert

import pyvts
import asyncio
import numpy
import time
from concurrent.futures import ThreadPoolExecutor


def textToSpeech(coquiTextToSpeech, text, filename = 'tts.wav'):
    coquiTextToSpeech.tts_to_file(text=text, file_path=filename)


def play_audio(data, samplerate, device=None):
    sounddevice.play(data, samplerate, blocking=False, device=device)


def rms(index, blocksize, blocks):
    block = blocks[index:index + blocksize]
    return numpy.sqrt(numpy.mean(block * block))


async def animate_mouth(vts, filename):
    authenticate_task = asyncio.create_task(vts.request_authenticate()) # use token

    #---------------------------------------------
    # read audio file and compute rms while waiting for authentication

    parameter = 'AIVoiceVolume'
    overlap = 0
    data, samplerate = soundfile.read(filename)

    blockDuration = 0.025 # seconds
    blocksize = int(blockDuration * samplerate + overlap)

    # blocksize = 1024
    # blockDuration = (blocksize - overlap) / samplerate # seconds

    executor = ThreadPoolExecutor()
    levels = [executor.submit(rms, i, blocksize, data) for i in range(0, len(data), blocksize - overlap)]

    #---------------------------------------------

    await authenticate_task

    #---------------------------------------------
    # play audio and send audio levels simultaneously

    start_time = time.time()
    end_time = len(levels) * blockDuration + start_time
    play_audio(data, samplerate)

    while end_time > time.time():
        current_time = time.time()
        current_block = int((current_time - start_time) / blockDuration)
        next_time = (current_block + 1) * blockDuration + start_time
        sleep_time = next_time - current_time

        try:
            current_level = levels[current_block].result(timeout=sleep_time)

            request = vts.vts_request.requestSetParameterValue(parameter=parameter, value=current_level)
            await vts.request(request)

            sleep_time = next_time - time.time()
            if sleep_time > 0: # dont sleep if request took longer than block duration
                await asyncio.sleep(sleep_time)
        except:
            continue

    executor.shutdown(wait=False, cancel_futures=True)
    request = vts.vts_request.requestSetParameterValue(parameter=parameter, value=0)
    await vts.request(request)
    await vts.close()


async def generate_and_speak(coquiTextToSpeech, text, vts, filename):
    connect_task = asyncio.create_task(vts.connect())

    #---------------------------------------------
    # generate wav while waiting for connection

    textToSpeech(coquiTextToSpeech, text, filename=filename)
    print('Generation finished')

    #---------------------------------------------

    await connect_task

    #---------------------------------------------

    await animate_mouth(vts, filename)


class sessionThread(Thread):
    def __init__(self, socket, bufferSize, coquiTextToSpeech, vts):
        Thread.__init__(self)
        self.socket = socket
        self.coquiTextToSpeech = coquiTextToSpeech
        self.vts = vts
        self.bufferSize = bufferSize


    def run(self):
        text = self.socket.recv(self.bufferSize).decode()
        filename = 'tts.wav'

        # rvc_convert(model_path='model.pth',
        #             f0_up_key=0,
        #             input_path='tts.wav')

        asyncio.run(generate_and_speak(self.coquiTextToSpeech, text, self.vts, filename))

        self.socket.close()


async def main():
    device = 'cpu'
    if torch.cuda.is_available():
        device = 'cuda'

    coquiTextToSpeech = TTS('tts_models/en/ljspeech/vits').to(device)
    # coquiTextToSpeech = TTS('tts_models/en/vctk/vits').to(device) # speaker='p225'

    #---------------------------------------------

    ip = '127.0.0.1'
    port = 12000
    address = (ip, port)
    bufferSize = 1024

    # use tcp
    serverSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    serverSocket.bind(address)
    serverSocket.listen(1)

    #---------------------------------------------

    plugin_info = {
        'plugin_name': 'AI Vtuber Voice',
        'developer': 'TelevisionNinja',
        'authentication_token_path': './token.txt'
    }
    vts = pyvts.vts(plugin_info=plugin_info)

    #---------------------------------------------

    await vts.connect()
    await vts.request_authenticate_token()  # get token
    await vts.request_authenticate()  # use token
    await vts.request(vts.vts_request.requestCustomParameter('AIVoiceVolume'))
    await vts.close()

    #---------------------------------------------

    print('Ready')

    while True:
        # wait for connection
        connectionSocket, addr = serverSocket.accept()

        # handle current connection
        sessionThread(connectionSocket, bufferSize, coquiTextToSpeech, vts).start()


if __name__ == '__main__':
    asyncio.run(main())
