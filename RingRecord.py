

# import openCV library and numpy
from collections import deque
from datetime import datetime
from email.mime import audio
import cv2
import numpy
import pyaudio
import wave
import threading
import ffmpeg


#
#
#       GENERAL VARIABLES
#
#

# set a variable to store file save location
file_save_location = "/home/nathan/Videos/RingRecord/"
audio_filename = ""
video_filename = ""

#
#
#       VIDEO VARIABLES
#
#

# define a video capture object
vid = cv2.VideoCapture(0)
# When 0 is placed in as the parameter to VideoCapture(), this connects to the default webcam of our computer


# set width and height of imported video to variables
width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

# try getting FPS
fps_float = vid.get(cv2.CAP_PROP_FPS)
fps = int(fps_float)
# print(fps) # print FPS to terminal


# set a variable for the fourcc video codec
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

# Will the video save by default?
doYouWantToSave = True

#
#
#       AUDIO VARIABLES
#
#
chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second
seconds = 5

def start_recording_video():
    # notify thread that video_filename is globale
    global video_filename
    # Will the video save by default?
    doYouWantToSave = True
    
    # this is the video in a buffer storing past 10 seconds.
    vid_frames = deque(maxlen=(seconds * fps))


    def save_to_vid(video):
        global video_filename #notify method that video_filename is global

        # get current date and time for filename
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y_%H:%M:%S")
        video_filename = file_save_location + 'raw_video/rawVideo_' + dt_string + '.mp4'
        writer = cv2.VideoWriter(video_filename, fourcc, fps, (width, height))
        print("Saving at: " + video_filename)
        for frame in vid_frames:
            writer.write(frame)
        writer.release()
        print("Done writing video!")


    while (recording.is_set()):  # Once per frame

        # Render this frame
        ret, frame = vid.read()

        vid_frames.append(frame)

        # Display the resulting frame
        cv2.imshow('Live Camera Feed', frame)

        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord('q'):
            recording.clear()
            break
#        elif cv2.waitKey(1) & 0xFF == ord('y'):
#            doYouWantToSave = True
#            print("Saving video on end. ")
#        elif cv2.waitKey(1) & 0xFF == ord('n'):
#            doYouWantToSave = False
#            print("Not saving on end.")


    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()


    if doYouWantToSave:
        save_to_vid(vid_frames)
        
    else:
        del vid_frames


def start_recording_audio(): 
    p = pyaudio.PyAudio()  # Create an interface to PortAudio
    global audio_filename # notify thread that audio_filename is global

    print('Recording audio...')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = deque(maxlen=int(fs / chunk * seconds))  # Initialize array to store frames

    # Store data in chunks for X seconds
    #try:
    #    while True:
    #        data = stream.read(chunk)
    #       frames.append(data)
    #except KeyboardInterrupt:
    #    pass

    while (recording.is_set()):
            data = stream.read(chunk)
            frames.append(data)



    # print(len(frames))

    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # get current date and time for filename
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H:%M:%S")
    # Save the recorded data as a WAV file
    audio_filename = file_save_location + 'raw_audio/rawAudio_' + dt_string + '.wav'
    wf = wave.open(audio_filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()


    
    print("Saved audio at: " + audio_filename)

if __name__ =="__main__":
    # create recording event
    recording = threading.Event()
    recording.set()
    # creating thread
    t1 = threading.Thread(target=start_recording_audio)
    t2 = threading.Thread(target=start_recording_video)

    # starting thread 1
    t1.start()
    # starting thread 2
    t2.start()

    # Allows you to press 'q' on video feed or ctrl-c
    # to end recording of both threads cleanly
    try:
        while (recording.is_set()):
            pass
    except KeyboardInterrupt:
        recording.clear()
        pass

    # wait until thread 1 is completely executed
    t1.join()
    # wait until thread 2 is completely executed
    t2.join()

    # Combine audio and video files into one file
    
    input_video = ffmpeg.input(video_filename)

    input_audio = ffmpeg.input(audio_filename)


    # get current date and time for filename
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H:%M:%S")

    combined_filename = file_save_location + 'output/video_' + dt_string + '.mp4'

    ffmpeg.concat(input_video, input_audio, v=1, a=1).output(combined_filename).run()

    #print(video_filename)
    #print(audio_filename)
    print(combined_filename)


    # both threads completely executed
    print("DONE WITH THREADS!")