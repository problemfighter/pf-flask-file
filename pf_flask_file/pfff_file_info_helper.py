from pf_flask_file.pfff_ffmpeg_helper import FFMPEGHelper
from pf_flask_file.pfff_image_helper import ImageHelper


class FileInfoHelper:

    @staticmethod
    def set_file_info(image_path, model):
        if hasattr(model, "size"):
            setattr(model, "size", ImageHelper.file_size(image_path))
        return model

    @staticmethod
    def set_audio_or_video_info(file_path, model, file_type="audio"):
        ffmpeg_helper = FFMPEGHelper()
        model = FileInfoHelper.set_file_info(file_path, model)

        duration = None
        if file_type == "audio":
            ffmpeg_helper.set_audio_file(file_path)
            duration = ffmpeg_helper.get_audio_duration()
        else:
            ffmpeg_helper.set_vdo_file(file_path)
            duration = ffmpeg_helper.get_vdo_duration()

        if hasattr(model, "duration"):
            setattr(model, "duration", duration)
        return model

    @staticmethod
    def set_audio_info(file_path, model):
        return FileInfoHelper.set_audio_or_video_info(file_path, model)

    @staticmethod
    def set_video_info(file_path, model):
        return FileInfoHelper.set_audio_or_video_info(file_path, model, "video")
