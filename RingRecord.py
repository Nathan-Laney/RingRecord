

# import openCV library and numpy
from collections import deque
from datetime import datetime
import cv2
import numpy


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

# set a variable to store file save location
file_save_loaction = "/home/nathan/Videos/RingRecord/"

# set a variable for the fourcc video codec
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

# how many seconds to save
seconds = 5
# this is the video in a buffer storing past 10 seconds.
frames = deque(maxlen=(seconds * fps))

# Will the video save by default?
doYouWantToSave = True

def save_to_vid(video):

    # get current date and time for filename
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H:%M:%S")
    writer = cv2.VideoWriter(file_save_loaction + 'rawVideo_' +
                             dt_string + '.mp4', fourcc, fps, (width, height))
    print("Saving at: " + file_save_loaction +
          'rawVideo_' + dt_string + '.mp4')
    for frame in frames:
        writer.write(frame)

    writer.release()
    print("Done!")


while (True):  # Once per frame

    # Render this frame
    ret, frame = vid.read()

    frames.append(frame)

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
    save_to_vid(frames)
    
else:
    del frames
