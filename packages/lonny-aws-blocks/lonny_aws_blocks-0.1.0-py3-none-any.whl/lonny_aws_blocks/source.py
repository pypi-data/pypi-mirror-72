from lonny_aws_stack import Stack
from .base import Node, register, constructor
from .type import NodeType
from troposphere import codecommit, Template, Output

Pipeline = constructor(NodeType.pipeline)

REPO_HTTPS_URL = "CloneUrlHttps"
REPO_SSH_URL = "CloneUrlSsh"

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
class Source(Node):
    def __init__(self, project):
        self._project = project

    def encode(self):
        return dict(project = self._project)

    def get_parts(self):
        return [self._project]

    def on_sync(self):
        super().on_sync()
        templ = _get_template(repo_name = self.name).to_json()
        return Stack(self.name).up(templ)

    def on_destroy(self):
        for pipeline in Pipeline.search(project = self._project):
            pipeline.destroy()
        Stack(self.name).down()
        super().on_destroy()

    def __str__(self):
        return f"Source(project = '{self._project}')"

    @property
    def repo_name(self):
        return self.name

    @property
    def repo_https_url(self):
        return self.sync()[REPO_HTTPS_URL]

    @property
    def repo_ssh_url(self):
        return self.sync()[REPO_SSH_URL]

    @staticmethod
    def decode(data):
        return Source(data["project"])

    node_type = NodeType.source