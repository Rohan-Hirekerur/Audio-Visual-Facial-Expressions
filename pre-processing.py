import cv2
import os
from glob import glob
import moviepy.editor as mp
import matplotlib.pyplot as plt
from scipy.io import wavfile as wav
from scipy.fftpack import fft
import numpy as np

input_path = "res/video"
audio_path = "res/audio"
video_frames_path = "res/video-frames"
audio_frames_path = "res/audio-frames"

if not os.path.exists(video_frames_path):
    os.mkdir(video_frames_path)

if not os.path.exists(audio_frames_path):
    os.mkdir(audio_frames_path)

if not os.path.exists(audio_path):
    os.mkdir(audio_path)

types = ("*.mp4")
video_path_list = []

for file in types:
    video_path_list.extend(glob(os.path.join(input_path, file)))

total = len(video_path_list)

for i, input_file in enumerate(video_path_list):
    print("Generating video frames for {}".format(input_file))
    file_name = input_file[10:-4]

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


    print("Extracting audio clips from {}".format(input_file))
    clip = mp.VideoFileClip(input_file)
    clip.audio.write_audiofile(audio_path + "/{}.wav".format(file_name))


    print("Generating audio frames for {}".format(input_file))

    if not os.path.exists(audio_frames_path + "/{}".format(file_name)):
        os.mkdir(audio_frames_path + "/{}".format(file_name))

    rate, data = wav.read(audio_path + "/{}.wav".format(file_name))
    fft_out = fft(data)
    ff = np.array(np.real(fft_out))
    frame_points_array = np.array_split(ff,count)

    count = 0
    for audio_frame in frame_points_array:
        plt.plot(audio_frame)
        plt.savefig(audio_frames_path + "/{}/frame{}.jpg".format(file_name,count))
        plt.clf()
        count += 1

    print("Done!\n")



