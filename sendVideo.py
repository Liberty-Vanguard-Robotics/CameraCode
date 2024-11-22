# Displays the Left and right Camera outputs
# press q to end the program and t to switch between overlaid and side by side streams


import depthai as dai
import numpy as np
import socket
import cv2
import pickle
import struct


# def sendFrame(frame):
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client_socket.connect(('192.168.168.206', 65432))

#     _, frame_encoded = cv2.imencode('.jpg', frame)
#     data = pickle.dumps(frame_encoded)
        
#     # Send message length first, then data
#     #Pay attention to this
#     client_socket.sendall(struct.pack("L", len(data)) + data)
#     client_socket.close()

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

def getStereoPair(pipeline, monoLeft, monoRight):
    stereo = pipeline.createStereoDepth()
    stereo.setLeftRightCheck(True)

    monoLeft.out.link(stereo.left)
    monoRight.out.link(stereo.right)

    return stereo

def mouseCallBack(event,x,y,flags,param):
    global mouseX, mouseY
    if event == cv2.EVENT_LBUTTONDOWN:
        mouseX = x
        mouseY = y

if __name__ == '__main__':


    mouseX = 0
    mouseY = 640
    # Create pipeline
    pipeline = dai.Pipeline()

    # Set up left and right Cameras
    monoLeft = getMonoCamera(pipeline, isleft= True)
    monoRight = getMonoCamera(pipeline, isleft= False)

    # Combine left and right cameras
    stereo = getStereoPair(pipeline, monoLeft, monoRight)

    # Set up XLink for Stereo Camera
    xoutDepth = pipeline.createXLinkOut()
    xoutDepth.setStreamName("depth")

    xoutDisp = pipeline.createXLinkOut()
    xoutDisp.setStreamName("disparity")

    xoutRectLeft = pipeline.createXLinkOut()
    xoutRectLeft.setStreamName("rectLeft")

    xoutRectRight = pipeline.createXLinkOut()
    xoutRectRight.setStreamName("rectRight")

    stereo.disparity.link(xoutDisp.input)

    stereo.rectifiedLeft.link(xoutRectLeft.input)
    stereo.rectifiedRight.link(xoutRectRight.input)

    # Pipeline is defined

    with dai.Device(pipeline) as device:

        # Get output queues
        disparityQueue = device.getOutputQueue(name = "disparity", maxSize = 1, blocking = False)
        rectLeftQueue = device.getOutputQueue(name = "rectLeft", maxSize = 1, blocking = False)
        rectRightQueue = device.getOutputQueue(name = "rectRight", maxSize = 1, blocking = False)

        # Calculate the colormap
        disparityMultiplier = 255 / stereo.getMaxDisparity()

        # Set display window Name
        cv2.namedWindow("Stereo Pair")
        cv2.setMouseCallback("Stereo Pair", mouseCallBack)

        sideBySide = False

        #setting up to send video
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('192.168.168.206', 65432))
        except:
            print("Couldn't conenct")

        while True:
            # Get frames
            disparity = getFrame(disparityQueue)
            Var = disparityQueue.get()
            VarToSend = Var.getFrame()

            # ColorMap for disparity view
            disparity = (disparity * disparityMultiplier).astype(np.uint8)
            disparity = cv2.applyColorMap(disparity, cv2.COLORMAP_JET)

            # Get left and right frames
            leftFrame = getFrame(rectLeftQueue)
            rightFrame = getFrame(rectRightQueue)

            imOut = leftFrame
            #Send imOut!
            imOut = cv2.cvtColor(imOut, cv2.COLOR_GRAY2RGB)

            imOut = cv2.line(imOut, (mouseX, mouseY), (1280, mouseY), (0, 0, 255), 2)
            imOut = cv2.circle(imOut, (mouseX, mouseY), 2, (255, 255, 128), 2)

            #sending video
        
            # Compress frame to JPEG format 
            _, frame_encoded = cv2.imencode('.jpg', imOut)
        
            # Serialize the compressed frame
            data = pickle.dumps(frame_encoded)
        
            # Send message length first, then data
            #Pay attention to this
            client_socket.sendall(struct.pack("L", len(data)) + data)

            cv2.imshow("Stereo Pair", imOut) #send this one
            cv2.imshow("Disparity", disparity)



            # Ends Stream when q is pressed
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
                client_socket.close()
            elif key == ord('t'):
                sideBySide = not sideBySide




# import socket
# import cv2
# import pickle
# import struct

# def send_video():
#     # Initialize camera
#     cap = cv2.VideoCapture(0)  # 0 is usually the default camera

#     # Setup client socket
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client_socket.connect(('192.168.168.2', 65432))

#     while cap.isOpened():
#         # Capture frame-by-frame
#         ret, frame = cap.read()
#         if not ret:
#             break
        
#         # Compress frame to JPEG format
#         _, frame_encoded = cv2.imencode('.jpg', frame)
        
#         # Serialize the compressed frame
#         data = pickle.dumps(frame_encoded)
        
#         # Send message length first, then data
#         client_socket.sendall(struct.pack("L", len(data)) + data)
    
#     # Release the camera and close the socket
#     cap.release()
#     client_socket.close()

# # Run the client
# send_video()
