from lonny_aws_stack import Stack
from .base import Resource, constructor, register
from .type import ResourceType
from .command import Command
from troposphere import codecommit, Template, Output

REPO_HTTPS_URL = "CloneUrlHttps"
REPO_SSH_URL = "CloneUrlSsh"
RESOURCE = "source"


def _get_git_repository(repo_name):
    return codecommit.Repository("Repository", 
        RepositoryName = repo_name
    )

def _get_template(*, repo_name):
    template = Template()
    repo = _get_git_repository(repo_name)
    template.add_resource(repo)
    template.add_output(Output(REPO_HTTPS_URL, Value = repo.get_att("CloneUrlHttp")))
    template.add_output(Output(REPO_SSH_URL, Value = repo.get_att("CloneUrlSsh")))
    return template

@register
class Source(Resource):
    def __init__(self, *, project):
        self._project = project

    def get_tags(self):
        return dict(project = self._project)

    def on_update(self):
        templ = _get_template(repo_name = self.get_name()).to_json()
        data = Stack(self.get_name()).up(templ)
        return dict(
            https_url = data[REPO_HTTPS_URL],
            name = self.get_name()
        )

    def on_destroy(self):
        Pipeline = constructor(ResourceType.pipeline)
        for pipeline in Pipeline.search(project = self._project):
            pipeline.destroy()
        Stack(self.get_name()).down()

    @staticmethod
    def from_tags(tags):
        return Source(project = tags["project"])

    resource_type = ResourceType.source

@Command
def list_sources(args):
    for source in Source.search():
        print(source)

@Command
def setup_source(args):
    Source(project = args.project).update()

@Command
def destroy_source(args):
    Source(project = args.project).destroy()