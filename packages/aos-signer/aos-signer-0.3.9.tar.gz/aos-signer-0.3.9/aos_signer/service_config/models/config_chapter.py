from abc import ABC, abstractmethod
from jsonschema import validate
from jsonschema import exceptions


class ConfigChapter(ABC):
    validation_schema = ''

    @staticmethod
    @abstractmethod
    def from_yaml(input_dict):
        ConfigChapter.validate(input_dict)

    # @abstractmethod
    # def to_json(self):
    #     return NotImplemented

    # @abstractmethod
    @staticmethod
    def validate(received_chapter, validation_schema):
        try:
            return validate(received_chapter, schema=validation_schema)
        except exceptions.ValidationError as ex:
            print(ex)
            raise ex
