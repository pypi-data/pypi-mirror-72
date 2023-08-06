from .models.publisher import Publisher
from .models.publish import Publish
from .models.build import Build
import ruamel.yaml


class ServiceConfigParser(object):

    def __init__(self, file_path):
        yaml = ruamel.yaml.YAML()
        yaml.register_class(Publisher)
        yaml.register_class(Publish)
        with open(file_path, 'r') as file:
            loaded = yaml.load(file)
            self._publisher = Publisher.from_yaml(loaded.get('publisher'))
            self._publish = Publish.from_yaml(loaded.get('publish'))
            self._build = Build.from_yaml(loaded.get('build'))

    @property
    def publish(self):
        return self._publish

    @property
    def build(self):
        return self._build
