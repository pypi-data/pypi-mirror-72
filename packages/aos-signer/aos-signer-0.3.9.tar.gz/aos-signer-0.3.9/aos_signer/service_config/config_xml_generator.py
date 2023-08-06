#
#  Copyright (c) 2018-2019 Renesas Inc.
#  Copyright (c) 2018-2019 EPAM Systems Inc.
#

import logging
from enum import Enum

from signxml import XMLSigner
from lxml.etree import Element, SubElement

from aos_signer.service_config.keys_manager import KeysManager
from aos_signer.service_config.configuration import Configuration, ConfigurationKeys

logger = logging.getLogger(__name__)


class ConfigGeneratorException(Exception):
    pass


class ConfigItemType(Enum):
    OBJECT = "object"
    LIST = "list"
    TEXT = "text"


class ConfigXMLGenerator:
    ATTRS = "attrs"
    LIST_ITEM_TAG = "item"
    ITEM_TYPE = "type"

    def __init__(self):
        self._configuration = Configuration()

    def generate(self, file_details) -> Element:
        key_manager = KeysManager()
        certificate = key_manager['meta/' + self._configuration.get_sign_certificate()]
        private_key = key_manager['meta/' + self._configuration.get_sign_key()]
        signed_root = XMLSigner().sign(self._root_element(file_details=file_details), key=private_key, cert=certificate)
        return signed_root

    def _root_element(self, file_details) -> Element:
        root = Element("root")
        root.append(self._file_details_element(file_details=file_details))
        root.append(self._info_element())
        root.append(self._quotas_element())
        return root

    def _info_element(self) -> Element:
        info = Element("info")

        # for child_key, child_data in self._configuration[ConfigurationKeys.META].items():
        #     info.append(self._generate_tree(key=child_key, data=child_data))

        return info

    def _quotas_element(self) -> Element:
        result = Element("quotas")
        quotas = self._configuration.get_quotas()
        if quotas:
            for quota_name, quota_value in quotas.items():
                try:
                    quota_value = int(quota_value)
                except Exception:
                    raise ConfigGeneratorException("Quota value should be integer, got '{}'.".format(quota_value))

                if quota_value <= 0:
                    raise ConfigGeneratorException("Quota value should be above zero, got '{}'.".format(quota_value))

                SubElement(result, quota_name).text = str(quota_value)

        return result

    def _generate_tree(self, key: str, data: dict) -> Element:
        if not isinstance(key, str):
            message = "Info key is not a string, got '{}'.".format(type(key).__name__)
            logger.error(message)
            raise ConfigGeneratorException(message)

        try:
            if isinstance(data, dict):
                attrs = {k: str(v) for k, v in data.get(self.ATTRS, {}).items()}
                attrs[self.ITEM_TYPE] = ConfigItemType.OBJECT.value
                result = Element(key, attrib=attrs)
                for child_key, child_data in data.items():
                    if child_key == self.ATTRS:
                        continue
                    result.append(self._generate_tree(key=child_key, data=child_data))
            elif isinstance(data, list):
                attrs = {"items": self.LIST_ITEM_TAG, self.ITEM_TYPE: ConfigItemType.LIST.value}
                result = Element(key, attrib=attrs)
                for child_data in data:
                    result.append(self._generate_tree(key=self.LIST_ITEM_TAG, data=child_data))
            else:
                attrs = {self.ITEM_TYPE: ConfigItemType.TEXT.value}
                child_data = str(data)
                result = Element(key, attrib=attrs)
                result.text = child_data
        except ValueError:
            message = "Bad key: '{}'.".format(key)
            logger.error(message)
            raise ConfigGeneratorException(message)

        return result

    def _file_details_element(self, file_details) -> Element:
        files = Element("files")
        for fd in file_details:
            SubElement(files, "file", attrib={
                "name": fd.name,
                "size": str(fd.size),
                "hash": fd.hash
            })
        return files
