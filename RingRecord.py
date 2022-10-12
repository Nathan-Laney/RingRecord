

# import openCV library and numpy
from collections import deque
import cv2 
import numpy 




# define a video capture object
vid = cv2.VideoCapture(0)
# When 0 is placed in as the parameter to VideoCapture(), this connects to the default webcam of our computer



# set width and height of imported video to variables
width= int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
height= int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

# try getting FPS
fps_float = vid.get(cv2.CAP_PROP_FPS)
fps = int(fps_float)
# print(fps) # print FPS to terminal 

# set a variable to store file save location
file_save_loaction = "/home/nathan/Videos/RingRecord/"

# set a variable for the fourcc video codec
fourcc = cv2.VideoWriter_fourcc('m','p','4','v')

# this is the video in a buffer storing past 10 seconds.
frames = deque(maxlen=(5 * fps)) 

# Will the video save by default? 
doYouWantToSave = True

def save_to_vid(video):

    writer= cv2.VideoWriter( file_save_loaction + 'basicvideo.mp4', fourcc, fps, (width,height))
    for frame in frames:
        writer.write(frame)

    writer.release()

while (True): # Once per frame

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
    if cv2.waitKey(1) & 0xFF == ord('y'):
        doYouWantToSave = True
        print("Saving video on end. ")
    if cv2.waitKey(1) & 0xFF == ord('n'):
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




