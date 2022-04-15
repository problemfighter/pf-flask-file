from pf_flask_file.pfff_ffmpeg_helper import FFMPEGHelper

path = ""
output_thumb = ""
audio_file = ""

ffmpeg_helper = FFMPEGHelper()
ffmpeg_helper.set_vdo_file(path)
ffmpeg_helper.export_vdo_thumb(output_thumb)

print(ffmpeg_helper.get_vdo_duration())

ffmpeg_helper.set_audio_file(audio_file)
print(ffmpeg_helper.get_audio_duration())
