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


device = 'cpu'
if torch.cuda.is_available():
    device = 'cuda'

# coquiTextToSpeech = TTS('tts_models/multilingual/multi-dataset/xtts_v2').to(device)
coquiTextToSpeech = TTS('tts_models/en/ljspeech/vits').to(device)
# coquiTextToSpeech = TTS('tts_models/en/vctk/vits').to(device)
# coquiTextToSpeech = TTS('tts_models/en/multi-dataset/tortoise-v2').to(device) # doesnt work
# coquiTextToSpeech = TTS('tts_models/multilingual/multi-dataset/bark').to(device) # doesnt work


def textToSpeech(text, filename = 'tts.wav'):
    coquiTextToSpeech.tts_to_file(text=text, file_path=filename)


def play_audio(data, samplerate, device=None):
    sounddevice.play(data, samplerate, blocking=False, device=device)


plugin_info = {
    'plugin_name': 'AI Vtuber Voice',
    'developer': 'TelevisionNinja',
    'authentication_token_path': './token.txt'
}
vts = pyvts.vts(plugin_info=plugin_info)

ip = '127.0.0.1'
port = 12000
address = (ip, port)
bufferSize = 1024

# use tcp
serverSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
serverSocket.bind(address)
serverSocket.listen(1)


class sessionThread(Thread):
    def __init__(self, socket):
        Thread.__init__(self)
        self.socket = socket


    async def animate_mouth(self, filename):
        parameter = 'AIVoiceVolume'
        overlap = 512
        data, samplerate = soundfile.read(filename)

        blockDuration = 0.01 # seconds
        blocksize = int(blockDuration * samplerate + overlap)

        # blocksize = 1024
        # blockDuration = (blocksize - overlap) / samplerate # seconds
        blockGenerator = soundfile.blocks(filename, blocksize=blocksize, overlap=overlap)

        await vts.connect()
        await vts.request_authenticate()  # use token

        play_audio(data, samplerate)

        for block in blockGenerator:
            level = numpy.sqrt(numpy.mean(block * block)) # rms
            request = vts.vts_request.requestSetParameterValue(parameter=parameter, value=level)
            await vts.request(request)
            await asyncio.sleep(blockDuration)

        request = vts.vts_request.requestSetParameterValue(parameter=parameter, value=0)
        await vts.request(request)
        await vts.close()


    def run(self):
        text = self.socket.recv(bufferSize).decode()
        filename = 'tts.wav'

        textToSpeech(text, filename=filename)
        print('Generation finished')

        # rvc_convert(model_path='model.pth',
        #             f0_up_key=0,
        #             input_path='tts.wav')

        asyncio.run(self.animate_mouth(filename))

        self.socket.close()


async def main():
    await vts.connect()
    await vts.request_authenticate_token()  # get token
    await vts.request_authenticate()  # use token
    await vts.request(vts.vts_request.requestCustomParameter('AIVoiceVolume'))
    await vts.close()

    print('Ready')

    while True:
        # wait for connection
        connectionSocket, addr = serverSocket.accept()

        # handle current connection
        sessionThread(connectionSocket).start()


if __name__ == '__main__':
    asyncio.run(main())
