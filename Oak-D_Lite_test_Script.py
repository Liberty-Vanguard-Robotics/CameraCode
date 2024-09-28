# Displays the Left and right Camera outputs
# press q to end the program and t to switch between overlaid and side by side streams

import cv2
import depthai as dai
import numpy as np

# returns Frames in form openCV can display
def getFrame(queue):
    frame = queue.get()
    return frame.getCvFrame()

def getMonoCamera(pipeline, isleft):
    # Configure Mono Camera
    mono = pipeline.createMonoCamera()
    
    #Set Camera Resolution
    mono.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)

    if isleft:
        #CAM_B is the left camera
        mono.setBoardSocket(dai.CameraBoardSocket.CAM_B)
    else : 
        #CAM_C is the right camera
        mono.setBoardSocket(dai.CameraBoardSocket.CAM_C)
    return mono

if __name__ == '__main__':

    # Create pipeline
    pipeline = dai.Pipeline()

    # Set up left and right Cameras
    monoLeft = getMonoCamera(pipeline, isleft= True)
    monoRight = getMonoCamera(pipeline, isleft= False)

    # Set up XLink for Left Camera
    xoutLeft = pipeline.createXLinkOut()
    xoutLeft.setStreamName("left")

    # Set up XLink for Right Camera
    xoutRight = pipeline.createXLinkOut()
    xoutRight.setStreamName("right")

    # Attach Cameras to respective XLinks
    monoLeft.out.link(xoutLeft.input)
    monoRight.out.link(xoutRight.input)

    with dai.Device(pipeline) as device:

        # Get output queues
        leftQueue = device.getOutputQueue(name = "left", maxSize = 1)
        rightQueue = device.getOutputQueue(name = "right", maxSize = 1)

        # Set display window Name
        cv2.namedWindow("Stereo Pair")
        sideBySide = True

        while True:
            # Get frames
            leftFrame = getFrame(leftQueue)
            rightFrame = getFrame(rightQueue)

            # Sets the output to stack or appear side by side
            if sideBySide:
                imOut = np.hstack((leftFrame, rightFrame))
            else:
                imOut = np.uint8(leftFrame/2 + rightFrame/2)

            # Display image
            cv2.imshow("Stereo Pair", imOut)

            # Ends Stream when q is pressed
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
            elif key == ord('t'):
                sideBySide = not sideBySide
