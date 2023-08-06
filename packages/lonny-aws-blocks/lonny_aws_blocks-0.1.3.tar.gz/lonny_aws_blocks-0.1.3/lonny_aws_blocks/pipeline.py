from troposphere import iam, codebuild, codepipeline, s3, Template, Output
from lonny_aws_stack import Stack
from .base import Node, register, constructor
from .type import NodeType
import boto3
import botocore

ADMIN_POLICY_ARN = "arn:aws:iam::aws:policy/AdministratorAccess"
ARTIFACT_NAME = "ARTIFACT"
S3_BUCKET = "Bucket"
ENV_PROJECT = "BLOCKS_PROJECT"
ENV_STAGE = "BLOCKS_STAGE"

resource_s3 = boto3.resource("s3")

def _get_s3_bucket():
    return s3.Bucket("S3Bucket")

def _get_codebuild_role():
    return iam.Role("CodeBuildRole",
        AssumeRolePolicyDocument = dict(
            Statement = [dict(
                Action = [ "sts:AssumeRole" ],
                Effect = "Allow",
                Principal = dict(Service = "codebuild.amazonaws.com")
            )]
        ),
        ManagedPolicyArns = [ADMIN_POLICY_ARN]
    )

def _get_codepipeline_role():
    return iam.Role("CodePipelineRole",
        AssumeRolePolicyDocument = dict(
            Statement = [dict(
                Action = [ "sts:AssumeRole" ],
                Effect = "Allow",
                Principal = dict(Service = "codepipeline.amazonaws.com")
            )]
        ),
        ManagedPolicyArns = [ADMIN_POLICY_ARN]
    )

def _get_codebuild_project(*, role_arn, branch, environment):
    env_vars = [ dict(Name = k, Value = v) for k,v in environment.items() ]
    return codebuild.Project(f"CodeBuild",
        Artifacts = codebuild.Artifacts(Type = "CODEPIPELINE"),
        Environment = codebuild.Environment(
            EnvironmentVariables = env_vars,
            Type = "LINUX_CONTAINER",
            ComputeType = "BUILD_GENERAL1_SMALL",
            PrivilegedMode = True,
            Image = "aws/codebuild/standard:4.0"
        ),
        Source = codebuild.Source(
            Type = "CODEPIPELINE"
        ),
        SourceVersion = branch,
        ServiceRole = role_arn,
    )

def _get_codepipeline_pipeline(*, repo_name, branch, s3_bucket_name, role_arn, build_project_name):
    return codepipeline.Pipeline(f"CodePipeline",
        ArtifactStore = codepipeline.ArtifactStore(
            Location = s3_bucket_name,
            Type = "S3"
        ),
        RoleArn = role_arn,
        Stages = [
            codepipeline.Stages(
                Name = "Source",
                Actions = [
                    codepipeline.Actions(
                        Name = "SourceAction",
                        ActionTypeId = codepipeline.ActionTypeId(
                            Category = "Source",
                            Owner = "AWS",
                            Version = "1",
                            Provider = "CodeCommit"
                        ),
                        OutputArtifacts = [
                            codepipeline.OutputArtifacts(
                                Name = ARTIFACT_NAME
                            )
                        ],
                        Configuration = dict(
                            RepositoryName = repo_name,
                            BranchName = branch,
                            PollForSourceChanges = True
                        )
                    )
                ]
            ),
            codepipeline.Stages(
                Name = "Build",
                Actions = [
                    codepipeline.Actions(
                        Name = "BuildAction",
                        ActionTypeId = codepipeline.ActionTypeId(
                            Category = "Build",
                            Owner = "AWS",
                            Version = "1",
                            Provider = "CodeBuild"
                        ),
                        InputArtifacts  = [
                            codepipeline.InputArtifacts(
                                Name = ARTIFACT_NAME
                            )
                        ],
                        Configuration = dict(
                            ProjectName = build_project_name
                        )
                    )
                ]
            )
        ]
    )

def _get_template(*, branch, repo_url, repo_name, environment):
    template = Template()

    bucket = _get_s3_bucket()
    template.add_resource(bucket)

    codebuild_role = _get_codebuild_role()
    template.add_resource(codebuild_role)

    codepipeline_role = _get_codepipeline_role()
    template.add_resource(codepipeline_role)

    codebuild_project = _get_codebuild_project(
        role_arn = codebuild_role.get_att("Arn"),
        branch = branch,
        environment = environment
    )
    template.add_resource(codebuild_project)

    codepipeline_pipeline = _get_codepipeline_pipeline(
        repo_name = repo_name,
        branch = branch,
        build_project_name = codebuild_project.ref(),
        s3_bucket_name = bucket.ref(),
        role_arn = codepipeline_role.get_att("Arn")
    )
    template.add_resource(codepipeline_pipeline)

    template.add_output(Output(S3_BUCKET, Value = bucket.ref()))
    return template

@register
class Pipeline(Node):
    def __init__(self, project, stage, *, branch):
        self._project = project
        self._stage = stage
        self._branch = branch

    def get_parts(self):
        return [self._project, self._stage]

    def encode(self):
        return dict(
            project = self._project,
            stage = self._stage,
            branch = self._branch
        )

    def on_sync(self):
        Source = constructor(NodeType.source)
        super().on_sync()
        source = Source(self._project)
        templ = _get_template(
            branch = self._branch,
            repo_url = source.repo_https_url,
            repo_name = source.repo_name,
            environment = {
                ENV_PROJECT: self._project,
                ENV_STAGE: self._stage
            }
        ).to_json()
        Stack(self.name).up(templ)

    def on_destroy(self):
        DockerDeploy = constructor(NodeType.docker_deploy)
        for docker_deploy in DockerDeploy.search(project = self._project, stage = self._stage):
            docker_deploy.destroy()
        stack = Stack(self.name)
        data = stack.peek()
        if data is not None:
            try:
                bucket = resource_s3.Bucket(data[S3_BUCKET])
                for key in bucket.objects.all():
                    key.delete()
                bucket.delete()
            except botocore.exceptions.ClientError as err:
                if err.response["error_code"] != "404":
                    raise
        stack.down()
        super().on_destroy()

    def __str__(self):
        return f"Pipeline(project = '{self._project}', stage = '{self._stage}', branch = '{self._branch}')"

    @staticmethod
    def decode(data):
        return Pipeline(data["project"], data["stage"], branch = data["branch"])
    
    node_type = NodeType.pipeline
