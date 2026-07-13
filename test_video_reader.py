import cv2

# Load the video
cap = cv2.VideoCapture("test_video.mp4")  # replace with your video file name

# Print total number of frames
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print("Total frames in video:", total_frames)

frame_number = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Video ended or failed at frame:", frame_number)
        break

    frame_number += 1
    print("Reading frame:", frame_number)

    resized_frame = cv2.resize(frame, (640, 480))
    cv2.imshow("Video Check", resized_frame)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
