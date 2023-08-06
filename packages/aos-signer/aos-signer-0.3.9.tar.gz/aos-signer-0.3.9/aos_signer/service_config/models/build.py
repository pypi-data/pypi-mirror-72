

from .config_chapter import ConfigChapter


class Build(ConfigChapter):
    validation_schema = {
        "type": "object",
        "required": [
            "os",
            "arch",
            "sign_key",
            "sign_certificate",
        ],
        "properties": {
            "os": {
                "type": "string",
                "title": "Service OS.",
                "description": "Currently, spec support 'linux' only",
                "maxLength": 255
            },
            "arch": {
                "type": "string",
                "title": "Service architecture.",
                "description": "Possible variants: amd64, arm.",
                "maxLength": 255
            },
            "sign_key": {
                "type": "string",
                "title": "Path to the service provider key file for sign relative from meta folder.",
                "description": "Path to the service provider key file for sign relative from meta folder.",
                "maxLength": 255
            },
            "sign_certificate": {
                "type": "string",
                "title": "Path to the service provider certificate file, used for sign process",
                "description": "Path to the service provider certificate file, used for sign process",
                "maxLength": 255
            },
            "remove_non_regular_files": {
                "type": "boolean",
                "title": "Default value: true. When set to true - the file links are not copied to the produced container",
                "description": "Default value: true. When set to true - the file links are not copied to the produced container",
                "maxLength": 255
            },
            "context": {
                "type": "string",
                "title": "Root path to the service sources",
                "description": "Root path to the service sources",
                "maxLength": 255
            },
        },
    }

    def __init__(self, os, arch, sign_key, sign_certificate, remove_non_regular_files, context):
        self._os = os
        self._arch = arch
        self._sign_key = sign_key
        self._sign_certificate = sign_certificate
        self._remove_non_regular_files = remove_non_regular_files
        self._context = context

    @staticmethod
    def from_yaml(input_dict):
        p = Build(
            os=input_dict.get('os'),
            arch=input_dict.get('arch'),
            sign_key=input_dict.get('sign_key'),
            sign_certificate=input_dict.get('sign_certificate'),
            remove_non_regular_files=input_dict.get('remove_non_regular_files'),
            context=input_dict.get('context'),
        )
        # p.validate(input_dict, validation_schema=p.validation_schema)
        # if p.validate(input_dict, validation_schema=p.validation_schema):
        # p._os = input_dict.get('os')
        # p._arch = input_dict.get('arch')
        # p._sign_key = input_dict.get('sign_key')
        # p._sign_certificate = input_dict.get('sign_certificate')
        # p._remove_non_regular_files = input_dict.get('remove_non_regular_files')
        # p._context = input_dict.get('context')
        return p

    @property
    def os(self):
        return self._os

    @property
    def arch(self):
        return self._arch

    @property
    def sign_key(self):
        return self._sign_key

    @property
    def sign_certificate(self):
        return self._sign_certificate

    @property
    def remove_non_regular_files(self) -> bool:
        return self._remove_non_regular_files

    @property
    def context(self):
        return self._context
