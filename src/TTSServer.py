import torch
from TTS.api import TTS

import socket
from threading import Thread

import sounddevice
import soundfile
# from rvc_infer import rvc_convert


device = 'cpu'
if torch.cuda.is_available():
    device = 'cuda'

# coquiTextToSpeech = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
coquiTextToSpeech = TTS("tts_models/en/ljspeech/vits").to(device)
# coquiTextToSpeech = TTS("tts_models/en/vctk/vits").to(device)
# coquiTextToSpeech = TTS("tts_models/en/multi-dataset/tortoise-v2").to(device) # doesnt work
# coquiTextToSpeech = TTS("tts_models/multilingual/multi-dataset/bark").to(device) # doesnt work


def textToSpeech(text, filename = 'tts.wav'):
    coquiTextToSpeech.tts_to_file(text=text, file_path=filename) # language="en"


def play_audio(filename, device=None):
    data, samplerate = soundfile.read(filename)
    sounddevice.play(data, samplerate, blocking=True, device=device)


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

    def run(self):
        text = self.socket.recv(bufferSize).decode()

        textToSpeech(text)
        print('Generation finished')

        play_audio('tts.wav', device='CABLE Input (VB-Audio Virtual C')

        # rvc_convert(model_path="model.pth",
        #             f0_up_key=0,
        #             input_path='tts.wav')

        self.socket.close()


def main():
    print('Ready')

    while True:
        # wait for connection
        connectionSocket, addr = serverSocket.accept()

        # handle current connection
        sessionThread(connectionSocket).start()


if __name__ == '__main__':
    main()
