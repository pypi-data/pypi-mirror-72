from .base import Resource, register
from .type import ResourceType

@register
class DynoConfig(Resource):
    def __init__(self, *, project, stage):
        self._project = project
        self._stage = stage

    def get_tags(self):
        return dict(
            project = self._project,
            stage = self._stage
        )

    def on_update(self, *, domains):
        return dict(domains = domains)

    @staticmethod
    def from_tags(tags):
        return DynoConfig(
            project = tags["project"],
            stage = tags["stage"]
        )

    resource_type = ResourceType.dyno_config
