from collections import deque
import pyaudio
import wave
import cv2

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second
seconds = 5
filename = "/home/nathan/Videos/RingRecord/output.wav"

# Uses default selected audio device.

p = pyaudio.PyAudio()  # Create an interface to PortAudio

print('Recording')

stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

frames = deque(maxlen=int(fs / chunk * seconds))  # Initialize array to store frames

# Store data in chunks for X seconds
try:
    while True:
        data = stream.read(chunk)
        frames.append(data)
except KeyboardInterrupt:
    pass



# print(len(frames))

# Stop and close the stream 
stream.stop_stream()
stream.close()
# Terminate the PortAudio interface
p.terminate()

print('Finished recording')

# Save the recorded data as a WAV file
wf = wave.open(filename, 'wb')
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(sample_format))
wf.setframerate(fs)
wf.writeframes(b''.join(frames))
wf.close()
