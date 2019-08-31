import cv2
import os
from glob import glob

input_path = "res/video"
video_frames_path = "res/video-frames"
audio_frames_path = "res/audio-frames"

if not os.path.exists(video_frames_path):
    os.mkdir(video_frames_path)

if not os.path.exists(audio_frames_path):
    os.mkdir(audio_frames_path)

types = ("*.mp4")
video_path_list = []

for file in types:
    video_path_list.extend(glob(os.path.join(input_path, file)))

total =len(video_path_list)

for i, input_file in enumerate(video_path_list):
    cap = cv2.VideoCapture(input_file)

    success, image = cap.read()
    count = 0
    while success:
        cv2.imwrite(video_frames_path + "/frame%d.jpg" % count, image)  # save frame as JPEG file
        success, image = cap.read()
        print('Read a new frame: ', success)
        count += 1