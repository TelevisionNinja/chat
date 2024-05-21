from tortoise import api_fast
from tortoise.utils.audio import load_voices
import torchaudio
import socket
from threading import Thread


tortoiseTextToSpeech = api_fast.TextToSpeech(kv_cache=True,
                                             half=True)


def textToSpeech(text, filename = 'tortoise.wav', voices=['emma',
                                                         'applejack',
                                                         'rainbow',
                                                         'halle',
                                                         'jlaw',
                                                         'mol']):
    voice_samples, conditioning_latents = load_voices(voices)
    pcmAudio = tortoiseTextToSpeech.tts(text=text, voice_samples=voice_samples, conditioning_latents=conditioning_latents)

    torchaudio.save(uri=filename,
                    src=pcmAudio.squeeze(0).cpu(),
                    sample_rate=24000)


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
        try:
            text = self.socket.recv(bufferSize).decode()

            textToSpeech(text)

            print('Generation finished')
        except:
            print('connection errored out')


def main():
    print('Ready')

    while True:
        # wait for connection
        connectionSocket, addr = serverSocket.accept()

        # handle current connection
        sessionThread(connectionSocket).start()


if __name__ == '__main__':
    main()
