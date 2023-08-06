from .config_chapter import ConfigChapter


class Configuration(ConfigChapter):
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
                "description": "Service OS. Currently, spec support linux only",
                "maxLength": 255
            },
            "arch": {
                "type": "string",
                "title": "Service architecture.",
                "description": "Possible variants: amd64, arm",
                "maxLength": 255
            },
            "sign_key": {
                "type": "string",
                "title": "Path to Sign key",
                "description": "Path to the service provider key file for sign.",
                "maxLength": 255
            },
            "sign_certificate": {
                "type": "string",
                "title": "Path to Sign certificate",
                "description": "Path to the service provider certificate file, used for sign process.",
                "maxLength": 255
            },
            "remove_non_regular_files": {
                "type": "boolean",
                "title": "Author Company",
                "description": "Default value: true. When set to true - the file links do not copied to the produced container",

                "maxLength": 255
            },
            "context": {
                "type": "string",
                "title": "Author Company",
                "description": "Developer Company, Division etc.",
                "maxLength": 255
            },
        },
    }

    @staticmethod
    def from_yaml(input_dict):
        p = Configuration()
        if p.validate(input_dict):
            p.author = input_dict.get('author')
            p.company = input_dict.get('company')
            return p
