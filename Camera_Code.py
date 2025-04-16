#Camera_Code
import cv2

# Captures Video change the # to the device id
stream = cv2.VideoCapture(0)
output_width, output_height = 640, 480

# Check for stream
if not stream.isOpened():
    print("No Stream")
    exit()

while(True):
    ret, frame = stream.read()
    #encoded_frame = pickle.loads(data)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Use INTER_NEAREST for fastest, lowest-quality downsampling (no interpolation)
    reduced_frame = cv2.resize(gray, (80, 60))

    # Resize the reduced frame to the desired output resolution (e.g., 640x480)
    displayed_frame = cv2.resize(reduced_frame, (output_width, output_height))
    # Check for end stream
    if not ret:
        print("No more stream")
        break

    # quits when q is pressed
    cv2.imshow("Webcame", displayed_frame)
    if cv2.waitKey(1) == ord('q'):
        break

stream.release()
cv2.destroyAllWindows()