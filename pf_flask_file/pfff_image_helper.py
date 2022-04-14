from pf_py_file.pfpf_file_util import PFPFFileUtil
from pf_py_file.pfpf_image_util import ImageUtil


class ImageHelper:

    @staticmethod
    def make_thumb(image_path):
        return ImageUtil.make_thumb(image_path, (200, 200))

    @staticmethod
    def file_size(image_path):
        size = PFPFFileUtil.file_size_into_byte(image_path)
        if not size:
            return "0"
        return PFPFFileUtil.human_readable_file_size(size)
