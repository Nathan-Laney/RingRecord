# following https://www.geeksforgeeks.org/python-opencv-capture-video-from-camera/

# import openCV library
import cv2 as cv2

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

writer= cv2.VideoWriter( file_save_loaction + 'basicvideo.mp4', fourcc, fps, (width,height))


while (True): # Once per frame

    # Render this frame
    ret, frame = vid.read()

    # using writer, save the frame 
    writer.write(frame)

    # Display the resulting frame
    cv2.imshow('frame', frame)

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# and the writer object
writer.release()
# Destroy all the windows
cv2.destroyAllWindows()
