import pyaudio
import wave
from array import array
import struct
import matplotlib.pyplot as plt
import numpy as np


FORMAT = pyaudio.paInt16
CHANNELS = 1

CHUNK = 2**11
RATE = 44100
count = 0
RECORD_SECONDS = 5
FRAMESIZE = 1024
NOFFRAMES = 220
WAVE_OUTPUT_FILENAME = "recordedFile.wav"
device_index = 2
audio = pyaudio.PyAudio()

print("----------------------record device list---------------------")
info = audio.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')
for i in range(0, numdevices):
        if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print ("Input Device id ", i, " - ", audio.get_device_info_by_host_api_device_index(0, i).get('name'))

print("-------------------------------------------------------------")

index = int(input())
print("recording via index "+str(index))

stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,input_device_index = index,
                frames_per_buffer=CHUNK)
print ("recording started")
Recordframes = []
import numpy as np

# for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
while True:
    # print int(RATE / CHUNK * RECORD_SECONDS)
    data = stream.read(CHUNK)
    # print(array('h',data))
    frequencies = np.fromstring(data,dtype=np.int16)
    peak=np.average(np.abs(frequencies))*2
    temp = int(50*peak/2**16)
    if temp == 0:

        count += 1
    else:
        count = 0
    print ("count: " + str(count))
    if count ==100:
        print ("mic inactive")
        break

    bars="#"*int(50*peak/2**16)
    print("%04d %05d %s"%(i,peak,bars))
    decoded = np.fromstring(data,'int');
    print (max(decoded))
    # break
    Recordframes.append(data)
    # print stream
print ("recording stopped")

stream.stop_stream()
stream.close()
audio.terminate()
# plt.plot(decoded)
# plt.show()


waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(Recordframes))
waveFile.close()