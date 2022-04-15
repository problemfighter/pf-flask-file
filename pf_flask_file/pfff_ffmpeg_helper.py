import os
from PIL import Image
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from pf_py_common.pf_exception import PFException
from pf_py_file.pfpf_file_util import PFPFFileUtil
from time import strftime
from time import gmtime


class FFMPEGHelper:

    video_file_clip: VideoFileClip
    audio_file_clip: AudioFileClip

    def set_vdo_file(self, file):
        if not PFPFFileUtil.is_exist(file):
            raise PFException("File not found!")
        self.video_file_clip = VideoFileClip(file)

    def set_audio_file(self, file):
        if not PFPFFileUtil.is_exist(file):
            raise PFException("File not found!")
        self.audio_file_clip = AudioFileClip(file)

    def get_vdo_duration(self):
        return strftime("%H:%M:%S", gmtime(self.video_file_clip.duration))

    def export_vdo_thumb(self, output_file, frame_at_second=12):
        dir_name = os.path.dirname(output_file)
        PFPFFileUtil.create_directories(dir_name)
        frame = self.video_file_clip.get_frame(frame_at_second)
        new_image = Image.fromarray(frame)
        new_image.save(output_file)
        return output_file

    def get_audio_duration(self):
        return strftime("%H:%M:%S", gmtime(self.audio_file_clip.duration))
