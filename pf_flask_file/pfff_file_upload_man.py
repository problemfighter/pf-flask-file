from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from pf_flask_file.pfff_file_helper import PFFFFileHelper
from pf_flask_file.pfff_message import PFFFMessage
from pf_flask_rest_com.api_def import APIDef, FileField
from pf_flask_rest_com.common.pffr_exception import pffrc_exception
from pf_py_file.pfpf_file_util import PFPFFileUtil


class PFFFFileUploadMan:

    def _get_file_input(self, name: str, api_def: APIDef):
        if name in api_def.fields:
            field = api_def.fields[name]
            if isinstance(field, FileField):
                return field
        return None

    def validate_file_size(self, file_storage: FileStorage, field: FileField):
        if field.max_size_kb and not PFFFFileHelper.is_validate_file_size(file_storage, field.max_size_kb):
            raise pffrc_exception.error_message_exception(PFFFMessage.FILE_SIZE_NOT_MATCH)
        return True

    def validate_file_extension(self, file_storage: FileStorage, field: FileField):
        if field.allowed_extensions and not PFFFFileHelper.allowed_file(file_storage.filename, field.allowed_extensions):
            raise pffrc_exception.error_message_exception(PFFFMessage.INVALID_EXTENSION)
        return True

    def upload_file(self, input_name, file_storage: FileStorage, upload_path, override_name: dict = None, override: bool = True):
        filename = secure_filename(file_storage.filename.lower())
        filename = PFFFFileHelper.process_file_name(filename)
        if override_name and input_name in override_name:
            filename = override_name[input_name] + "." + PFFFFileHelper.get_file_extension(filename)
        if filename:
            filename = filename.lower()
        PFPFFileUtil.create_directories(upload_path)
        file_upload_path = PFPFFileUtil.join_path(upload_path, filename)
        if override:
            PFPFFileUtil.delete_file(file_upload_path)
            file_storage.save(file_upload_path)
        return filename

    def _get_file_name_from_list(self, index, list_data: list, default_name: str = "file"):
        try:
            if not list_data:
                return None
            return list_data[index]
        except IndexError:
            return default_name + str(index)

    def _get_upload_file_override_name(self, input_name, override_name: dict, index=0):
        if not override_name:
            return None
        file_name = None
        if input_name in override_name:
            if isinstance(override_name[input_name], list):
                file_name = self._get_file_name_from_list(index, override_name[input_name])
            else:
                file_name = override_name[input_name]
        return file_name

    def validate_and_upload_multiple(self, files: dict, api_def: APIDef, upload_path, override_name: dict = None, override: bool = True):
        response_file_name_dict = {}

        for input_name in files:
            file_list = files[input_name]

            if not isinstance(file_list, list):
                file_list = [file_list]

            override_name_index = 0
            uploaded_file_names = []
            file_name = self._get_upload_file_override_name(input_name, override_name, override_name_index)
            if file_name:
                uploaded_file_names = {}

            for file in file_list:
                file_name = self._get_upload_file_override_name(input_name, override_name, override_name_index)
                override_name_index += 1
                _override_name = None

                if file_name:
                    _override_name = {input_name: file_name}
                response = self.validate_and_upload(
                    files={input_name: file},
                    api_def=api_def,
                    upload_path=upload_path,
                    override_name=_override_name,
                    override=override)

                if isinstance(uploaded_file_names, list):
                    uploaded_file_names.append(response[input_name])
                elif isinstance(uploaded_file_names, dict) and file_name:
                    uploaded_file_names[file_name] = response[input_name]

            response_file_name_dict.update({input_name: uploaded_file_names})
        return response_file_name_dict

    def validate_and_upload(self, files: dict, api_def: APIDef, upload_path, override_name: dict = None, override: bool = True):
        errors = {}
        if not upload_path:
            raise pffrc_exception.error_details_exception(PFFFMessage.INVALID_UPLOAD_PATH, errors)

        for input_name in files:
            try:
                field: FileField = self._get_file_input(input_name, api_def)
                if field and isinstance(files[input_name], FileStorage):
                    file_storage: FileStorage = files[input_name]
                    self.validate_file_size(file_storage, field)
                    self.validate_file_extension(file_storage, field)
                    files[input_name] = self.upload_file(input_name, file_storage, upload_path, override_name, override)
            except Exception as e:
                errors[input_name] = str(e)
        if errors:
            raise pffrc_exception.error_details_exception(PFFFMessage.VALIDATION_ERROR, errors)
        return files
