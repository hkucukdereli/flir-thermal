import numpy as np
from tqdm import tqdm
import cv2
import ffmpeg

import fnv
import fnv.reduce
from fnv.file import ImagerFile

class flirVideo(ImagerFile):
    def __init__(self, video_path):
        if type(video_path)!=str:
            video_path = str(video_path)

        super().__init__(video_path)

        self.path = video_path

        # set desired units
        if self.has_unit(fnv.Unit.TEMPERATURE_FACTORY):
            # set units to temperature, if available
            self.unit = fnv.Unit.TEMPERATURE_FACTORY
            self.temp_type = fnv.TempType.CELSIUS         # set temperature unit
        else:
            # if file has no temperature calibration, use counts instead
            self.unit = fnv.Unit.COUNTS

        self.has_data = False

    @property
    def size(self):
        if self.has_data:
            print(f'Num frames: {self.num_frames}, height: {self.height}, width: {self.width}')
            return None
        else:
            print('No video data found.')
            return None

    @property
    def metadata(self):
        if self.has_data:
            print(f'Video is {self.duration} seconds long recorded at {self.fps} Hz.\nNumber of frames: {self.num_frames}, height: {self.height}, width: {self.width}')
            return None
        else:
            print('No video data found.')
            return None

    def read_video(self):
        self.data = np.zeros((self.num_frames, self.height, self.width)) + np.nan
        self.time = []

        frames = np.arange(self.num_frames)
        for i in tqdm(frames, total=len(frames), desc='Loading video...'):
            self.get_frame(i)
            self.data[i] = np.array(self.final, copy=False).reshape((self.height, self.width))
            self.time.append(self.frame_info.time)

        self.duration = (self.time[-1] - self.time[0]).total_seconds() # video duration in seconds
        fps = self.num_frames / self.duration
        state = np.argmin([np.abs(fps-60), np.abs(fps-30)])
        if state==0:
            self.fps = 60
        else:
            self.fps = 30

        if len(self.data)>0:
            self.has_data = True

        return self.time, self.data

    def save_video(self, save_path, vcodec='libx264'):
        if self.has_data:
            process = (
                ffmpeg
                    .input('pipe:', format='rawvideo', pix_fmt='gray8', s='{}x{}'.format(self.width, self.height))
                    .output(save_path, pix_fmt='yuv420p', vcodec=vcodec, r=self.fps)
                    .overwrite_output()
                    .run_async(pipe_stdin=True)
            )

            for frame in self.data:
                process.stdin.write(
                    frame
                        .astype(np.uint8)
                        .tobytes()
                )
            process.stdin.close()
            process.wait()
        else:
            raise MissingValueError('Video data has not been loaded. Run < read_video > first.')
