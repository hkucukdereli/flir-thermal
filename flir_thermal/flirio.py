import numpy as np
from tqdm import tqdm
import ffmpeg

import fnv
from fnv.file import ImagerFile

class flirVideo(ImagerFile):
    def __init__(self, video_path):
        if type(video_path)!=str:
            self.video_path = str(video_path)
            
        # Check if the video file exists
        self.has_data = False
        if os.path.isfile(self.video_path):
            super().__init__(self.video_path)
            self.has_data = True

            # set desired units
            if self.has_unit(fnv.Unit.TEMPERATURE_FACTORY):
                # set units to temperature, if available
                self.unit = fnv.Unit.TEMPERATURE_FACTORY
                self.temp_type = fnv.TempType.CELSIUS         # set temperature unit
            else:
                # if file has no temperature calibration, use counts instead
                self.unit = fnv.Unit.COUNTS
        else:
            raise IOError(f"{self.path} is not found.")

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
            self.get_duration()
            self.get_fps()
            print(f'Video is {self.duration} seconds long recorded at {self.fps} Hz.\nNumber of frames: {self.num_frames}, height: {self.height}, width: {self.width}')
            return None
        else:
            print('No video data found.')
            return None

    def get_duration(self):
        if self.has_data:
            self.get_frame(0)
            time_begin = self.frame_info.time
            
            self.get_frame(self.num_frames)
            time_end = self.frame_info.time

            self.duration = (time_begin - time_end).total_seconds() # video duration in seconds

            return self.duration
        else:
            return None

    def get_duration(self)():
        try:
            self.get_duration()

            fps = self.num_frames / self.duration
            
            state = np.argmin([np.abs(fps-60), np.abs(fps-30)])
            if state==0:
                self.fps = 60
            else:
                self.fps = 30

            return self.fps
        except:
            return None

    def read_video(self, frames=[]):
        if self.has_data:
            data = np.zeros((frames, self.height, self.width)) + np.nan
            time = []
            index = np.zeros(len(frames))

            if len(frames)==0:
                frames = np.arange(self.num_frames)
            else:
                pass

            for i in tqdm(enumerate(frames), total=len(frames), desc='Loading video...'):
                self.get_frame(i)
                index[i] = i
                data[i] = np.array(self.final, copy=False).reshape((self.height, self.width))
                time.append(self.frame_info.time)

            return index, data, time
        else:
            print ('No video file is found.')

            return None, None, None

    def save_video(self, data, save_path, vcodec='libx264'):
        if self.has_data:
            process = (
                ffmpeg
                    .input('pipe:', format='rawvideo', pix_fmt='gray8', s='{}x{}'.format(self.width, self.height))
                    .output(save_path, pix_fmt='yuv420p', vcodec=vcodec, r=self.fps)
                    .overwrite_output()
                    .run_async(pipe_stdin=True)
            )

            for frame in data:
                process.stdin.write(
                    frame
                        .astype(np.uint8)
                        .tobytes()
                )
            process.stdin.close()
            process.wait()
        else:
            raise MissingValueError('Video data has not been loaded. Run < read_video > first.')
