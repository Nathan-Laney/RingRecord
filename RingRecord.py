

# import openCV library and numpy
from collections import deque
from datetime import datetime
import cv2
import numpy
import pyaudio
import wave


#
#
#       GENERAL VARIABLES
#
#

# set a variable to store file save location
file_save_loaction = "/home/nathan/Videos/RingRecord/"

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
    # Will the video save by default?
    doYouWantToSave = True
    
    # this is the video in a buffer storing past 10 seconds.
    vid_frames = deque(maxlen=(seconds * fps))


    def save_to_vid(video):

        # get current date and time for filename
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y_%H:%M:%S")
        writer = cv2.VideoWriter(file_save_loaction + 'rawVideo_' +
                                dt_string + '.mp4', fourcc, fps, (width, height))
        print("Saving at: " + file_save_loaction +
            'rawVideo_' + dt_string + '.mp4')
        for frame in vid_frames:
            writer.write(frame)

        writer.release()
        print("Done!")


    while (True):  # Once per frame

        # Render this frame
        ret, frame = vid.read()

        vid_frames.append(frame)

        # Display the resulting frame
        cv2.imshow('frame', frame)

        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        elif cv2.waitKey(1) & 0xFF == ord('y'):
            doYouWantToSave = True
            print("Saving video on end. ")
        elif cv2.waitKey(1) & 0xFF == ord('n'):
            doYouWantToSave = False
            print("Not saving on end.")


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

    # get current date and time for filename
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H:%M:%S")
    # Save the recorded data as a WAV file
    wf = wave.open(file_save_loaction +
            'rawAudio_' + dt_string + '.wav', 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()


    
    print("Saved at: " + file_save_loaction +
            'rawAudio_' + dt_string + '.mp4')

start_recording_video()
start_recording_audio()