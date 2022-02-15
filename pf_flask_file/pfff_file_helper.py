from werkzeug.datastructures import FileStorage
from pf_py_file.pfpf_string_util import PFPFStringUtil


class PFFFFileHelper:

    @staticmethod
    def get_file_size(file_object: FileStorage, default=0):
        if file_object.content_length:
            return file_object.content_length

        try:
            current_position = file_object.tell()
            file_object.seek(0, 2)
            size = file_object.tell()
            file_object.seek(current_position)
            return size
        except (AttributeError, IOError):
            pass

        return default

    @staticmethod
    def is_validate_file_size(file_object: FileStorage, max_size_kb):
        size = PFFFFileHelper.get_file_size(file_object)
        size_in_kb = size * 1000
        if size_in_kb <= max_size_kb:
            return True
        return False

    @staticmethod
    def get_file_extension(filename):
        if '.' in filename:
            return filename.rsplit('.', 1)[1].lower()

    @staticmethod
    def allowed_file(filename, file_extensions: list):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in file_extensions

    @staticmethod
    def process_file_name(file_name: str):
        if file_name:
            file_name = PFPFStringUtil.camelcase_to(file_name, "-")
            file_name = PFPFStringUtil.find_and_replace_with(file_name, "_", "-")
            file_name = PFPFStringUtil.replace_space_with(file_name, "-")
            file_name = file_name.lower()
        return file_name
