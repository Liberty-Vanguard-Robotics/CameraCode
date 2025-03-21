#Camera_Code
import cv2

# Captures Video change the # to the device id
stream = cv2.VideoCapture(1)

# Check for stream
if not stream.isOpened():
    print("No Stream")
    exit()

while(True):
    ret, frame = stream.read()
    # Check for end stream
    if not ret:
        print("No more stream")
        break

    # quits when q is pressed
    cv2.imshow("Webcame", frame)
    if cv2.waitKey(1) == ord('q'):
        break

stream.release()
cv2.destroyAllWindows()