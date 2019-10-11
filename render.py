import numpy as np
import cv2
import glob
import os

path = "res/landmarks/mcem0_sx408/"

# C:\Users\rohan\PycharmProjects\Audio-Visual Facial Expressions\res\audio-frames\mcem0_sx408


def sorted_nicely(strings):
    "Sort strings the way humans are said to expect."
    return sorted(strings, key=natural_sort_key)


def natural_sort_key(key):
    import re
    return [int(t) if t.isdigit() else t for t in re.split(r'(\d+)', key)]


types = ('*.txt')
landmarks_list= []
for files in types:
    landmarks_list.extend(glob.glob(os.path.join(path, files)))
total_num = len(landmarks_list)

landmarks_list = sorted_nicely(landmarks_list)
landmarks_list = landmarks_list[1:]

frames = []
for i, landmark_path in enumerate(landmarks_list):
    file = open(landmark_path)
    frame = []

    for line in file:
        x, y = line.split(" ")
        frame.append([float(x), float(y)])

    frames.append(frame)


size = (2000, 2000)
img_array = []
for frame in frames:
    image = np.zeros(shape=(2000, 2000, 3), dtype=np.uint8)
    prev = None
    count = 1
    last_pt = None
    for x, y in frame:
        x *= 13
        y *= 15
        if count not in [18, 23, 28, 32, 37, 43, 49, 61]:
            if prev is not None:
                image = cv2.line(image, (int(prev[0] / 2), int(prev[1] / 2)), (int(x / 2), int(y / 2)),
                                 color=(0, 0, 255), thickness=3)
        else:
            if last_pt is not None and count not in [23, 28, 32]:
                image = cv2.line(image, (int(last_pt[0] / 2), int(last_pt[1] / 2)), (int(prev[0]/2),int(prev[1]/2)), color=(0, 0, 255), thickness=3)
            last_pt = [x, y]
        # image = cv2.circle(image, (int(x/2),int(y/2)), radius=2, color=(0, 0, 255))
        prev = [x, y]
        count += 1

    image = cv2.line(image, (int(last_pt[0] / 2), int(last_pt[1] / 2)), (int(prev[0] / 2), int(prev[1] / 2)),
                     color=(0, 0, 255), thickness=3)
    # cv2.imshow("test", image)
    # cv2.waitKey(0)
    img_array.append(image)


out = cv2.VideoWriter('project_line.avi', cv2.VideoWriter_fourcc(*'DIVX'), 25, size)

for i in range(len(img_array)):
    out.write(image=img_array[i])
out.release()



import moviepy.editor as mpe
my_clip = mpe.VideoFileClip('project_line.avi')
audio_background = mpe.AudioFileClip('res/audio/mcem0_sx408.wav')
# print(audio_background, my_clip.audio)
# final_audio = mpe.CompositeAudioClip([my_clip.audio, audio_background])
final_clip = my_clip.set_audio(audio_background)
final_clip.write_videofile("movie.mp4",fps=25)
os.remove("project_line.avi")