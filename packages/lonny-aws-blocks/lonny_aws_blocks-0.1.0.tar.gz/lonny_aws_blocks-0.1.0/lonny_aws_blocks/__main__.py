from .type import DomainName, ProcDef, NodeType
from .base import constructor
from os.path import join
import argparse, os, json

from logging import StreamHandler
from lonny_aws_blob import logger as blob_logger
from lonny_aws_stack import logger as stack_logger

handler = StreamHandler()
stack_logger.addHandler(handler)
stack_logger.setLevel("DEBUG")
blob_logger.addHandler(handler)
blob_logger.setLevel("DEBUG")

ROOT = "ROOT"

LIST_SOURCES = "LIST_SOURCES"
CREATE_SOURCE = "CREATE_SOURCE"
DESTROY_SOURCE = "DESTROY_SOURCE"

LIST_PIPELINES = "LIST_PIPELINES"
CREATE_PIPELINE = "CREATE_PIPELINE"
DESTROY_PIPELINE = "DESTROY_PIPELINE"

DEPLOY_PIPELINE = "DEPLOY_PIPELINE"

Source = constructor(NodeType.source)
Pipeline = constructor(NodeType.pipeline)
DockerDeploy = constructor(NodeType.docker_deploy)

root = argparse.ArgumentParser()
root.set_defaults(which = ROOT)
subs = root.add_subparsers()

list_sources = subs.add_parser("list_sources")
list_sources.set_defaults(which = LIST_SOURCES)

create_source = subs.add_parser("create_source")
create_source.set_defaults(which = CREATE_SOURCE)
create_source.add_argument("project")

destroy_source = subs.add_parser("destroy_source")
destroy_source.set_defaults(which = DESTROY_SOURCE)
destroy_source.add_argument("project")

list_pipelines = subs.add_parser("list_pipelines")
list_pipelines.set_defaults(which = LIST_PIPELINES)
list_pipelines.add_argument("--project", default = None)

create_pipeline = subs.add_parser("create_pipeline")
create_pipeline.set_defaults(which = CREATE_PIPELINE)
create_pipeline.add_argument("project")
create_pipeline.add_argument("stage")
create_pipeline.add_argument("--branch")

deploy_pipeline = subs.add_parser("deploy_pipeline")
deploy_pipeline.set_defaults(which = DEPLOY_PIPELINE)
deploy_pipeline.add_argument("project")
deploy_pipeline.add_argument("stage")
deploy_pipeline.add_argument("--config", default = "blocks.json")
deploy_pipeline.add_argument("--image_uri")

destroy_pipeline = subs.add_parser("destroy_pipeline")
destroy_pipeline.set_defaults(which = DESTROY_PIPELINE)
destroy_pipeline.add_argument("project")
destroy_pipeline.add_argument("stage")

def run():
    args = root.parse_args()
    if args.which == ROOT:
        root.print_help()

    elif args.which == LIST_SOURCES:
        for source in Source.search():
            print(source)
    elif args.which == CREATE_SOURCE:
        Source(args.project).sync()
    elif args.which == DESTROY_SOURCE:
        for source in Source.search(project = args.project):
            source.destroy()

    elif args.which == LIST_PIPELINES:
        for pipeline in Pipeline.search(project = args.project):
            print(pipeline)
    elif args.which == CREATE_PIPELINE:
        Pipeline(args.project, args.stage, branch = args.branch).sync()
    elif args.which == DEPLOY_PIPELINE:
        with open(join(os.getcwd(), args.config)) as f:
            config = json.loads(f.read())
        docker = config.get("docker")
        if docker is not None:
            domains = [DomainName.decode(x) for x in docker["domains"]]
            secret_arn = docker.get("secret_arn")
            procs = { k : ProcDef.decode(v) for k,v in docker.get("procs", dict()).items() }
            DockerDeploy(
                args.project, 
                args.stage, 
                domains = domains, 
                procs = procs, 
                secret_arn = secret_arn, 
                image_uri = args.image_uri
            ).sync()
    elif args.which == DESTROY_PIPELINE:
        for pipeline in Pipeline.search(project = args.project, stage = args.stage):
            pipeline.destroy()

run()