import cv2
import os
from glob import glob
import moviepy.editor as mp


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

total = len(video_path_list)

for i, input_file in enumerate(video_path_list):
    print("Generating frames for {}".format(input_file))
    file_name = input_file[12:-4]
    if not os.path.exists(video_frames_path + "/{}".format(file_name)):
        os.mkdir(video_frames_path + "/{}".format(file_name))
    cap = cv2.VideoCapture(input_file)

    success, image = cap.read()
    count = 0
    while success:
        cv2.imwrite(video_frames_path + "/{}/frame%d.jpg".format(file_name) % count, image)  # save frame as JPEG file
        success, image = cap.read()
        # print('Read a new frame: ', success)
        count += 1

    print("Extracting audio from {}".format(input_file))
    clip = mp.VideoFileClip(input_file)
    clip.audio.write_audiofile(audio_frames_path + "/{}.wav".format(file_name))
    print("Done!\n")

# import matplotlib.pyplot as plt
# from scipy.io import wavfile as wav
# from scipy.fftpack import fft
# import numpy as np
# rate, data = wav.read("test.wav")
# fft_out = fft(data)
# print(fft_out)
# ff = np.array(np.real(fft_out))
# # ff = ff.astype(dtype=int)
# print(ff)
# # x, y = ff.T
# # plt.scatter(x,y)
# # print(ff,fft_out, np.abs(fft_out))
# plt.plot(ff)
# plt.show()

