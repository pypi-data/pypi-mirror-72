from .config_chapter import ConfigChapter


class Publish(ConfigChapter):
    validation_schema = {
        "type": "object",
        "required": [
            "service_uid",
        ],
        "properties": {
            "url": {
                "type": "string",
                "title": "URI for service publishing.",
                "description": "URI to publish. Default: aoscloud.io.",
                "maxLength": 255
            },
            "service_uid": {
                "type": "string",
                "title": "Service UID (provided by Aos cloud).",
                "description": "Service UID (provided by Aos cloud).",
                "maxLength": 255
            },
            "tls_key": {
                "type": "string",
                "title": "Path to the key file for TLS connetion. If absent - sign_key is used.",
                "description": "Path to the key file for TLS connetion. If absent - sign_key is used.",
                "maxLength": 255
            },
            "tls_certificate": {
                "type": "string",
                "title": "Path to the certificate file for TLS connetion. If absent - sign_certificate is used",
                "description": "Path to the certificate file for TLS connetion. If absent - sign_certificate is used",
                "maxLength": 255
            },
            "version": {
                "type": "string",
                "title": "Service Version",
                "description": "User-defined service version",
                "maxLength": 255
            },
        },
    }

    @staticmethod
    def from_yaml(input_dict):
        p = Publish()
        p.validate(input_dict, validation_schema=p.validation_schema)
        p._url = input_dict.get('url')
        p._service_uid = input_dict.get('service_uid')
        p._tls_key = input_dict.get('tls_key')
        p._tls_certificate = input_dict.get('tls_certificate')
        p._version = input_dict.get('version')
        return p

    @property
    def url(self):
        return self._url

    @property
    def service_uid(self):
        return self._service_uid

    @property
    def tls_key(self):
        return self._tls_key

    @property
    def tls_certificate(self):
        return self._tls_certificate

    @property
    def version(self):
        return self._version
