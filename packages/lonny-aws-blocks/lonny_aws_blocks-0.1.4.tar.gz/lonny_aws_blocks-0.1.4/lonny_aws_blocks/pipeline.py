from troposphere import iam, codebuild, codepipeline, s3, Template, Output
from lonny_aws_stack import Stack
from .command import Command
from .base import Resource, constructor, register
from .type import ResourceType

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

def _purge_s3_bucket(name):
    try:
        bucket = resource_s3.Bucket(name)
        for key in bucket.objects.all():
            key.delete()
        bucket.delete()
    except botocore.exceptions.ClientError as err:
        if err.response["error_code"] != "404":
            raise

@register
class Pipeline(Resource):
    def __init__(self, *, project, stage):
        self._project = project
        self._stage = stage

    def get_tags(self):
        return dict(
            project = self._project,
            stage = self._stage
        )

    def on_update(self, *, branch):
        Source = constructor(ResourceType.source)
        source = Source(project = self._project).update()
        templ = _get_template(
            branch = branch,
            repo_url = source["https_url"],
            repo_name = source["name"],
            environment = {
                ENV_PROJECT: self._project,
                ENV_STAGE: self._stage
            }
        ).to_json()
        Stack(self.get_name()).up(templ)

    def on_destroy(self):
        Dyno = constructor(ResourceType.dyno)
        dyno = Dyno(project = self._project, stage = self._stage)
        dyno.destroy()
        stack = Stack(self.get_name())
        data = stack.peek()
        if data is not None:
            _purge_s3_bucket(data[S3_BUCKET])
        stack.down()

    @staticmethod
    def from_tags(tags):
        return Pipeline(
            project = tags["project"], 
            stage = tags["stage"]
        )

    resource_type = ResourceType.pipeline

@Command
def list_pipelines(args):
    for pipeline in Pipeline.search(project = args.project):
        print(pipeline)

@Command
def destroy_pipeline(args):
    Pipeline(
        project = args.project,
        stage = args.stage
    ).destroy()

@Command
def setup_pipeline(args):
    Pipeline(
        project = args.project,
        stage = args.stage
    ).update(branch = args.branch)