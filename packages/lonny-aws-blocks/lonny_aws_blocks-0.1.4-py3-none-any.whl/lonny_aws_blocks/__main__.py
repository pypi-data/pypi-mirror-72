import argparse
from lonny_aws_blob import init as init_domain
from importlib import import_module
from .source import list_sources, setup_source, destroy_source
from .pipeline import setup_pipeline, list_pipelines, destroy_pipeline
from .dyno import setup_dyno, destroy_dyno
from lonny_aws_blob import Lock

from logging import StreamHandler
from lonny_aws_stack import logger as stack_logger

import_module("lonny_aws_blocks.dyno_balancer")
import_module("lonny_aws_blocks.dyno_config")

ROOT = "ROOT"
INIT = "INIT"

handler = StreamHandler()
stack_logger.addHandler(handler)
stack_logger.setLevel("DEBUG")

root = argparse.ArgumentParser()
root.set_defaults(which = ROOT)
subs = root.add_subparsers()

parser = subs.add_parser("init")
parser.set_defaults(which = "INIT")

# source commands
parser = subs.add_parser("setup_source")
parser.set_defaults(which = setup_source.which)
parser.add_argument("project")

parser = subs.add_parser("destroy_source")
parser.set_defaults(which = destroy_source.which)
parser.add_argument("project")

parser = subs.add_parser("list_sources")
parser.set_defaults(which = list_sources.which)

# pipeline commands
parser = subs.add_parser("setup_pipeline")
parser.set_defaults(which = setup_pipeline.which)
parser.add_argument("project")
parser.add_argument("stage")
parser.add_argument("--branch", default = "master")

parser = subs.add_parser("destroy_pipeline")
parser.set_defaults(which = destroy_pipeline.which)
parser.add_argument("project")
parser.add_argument("stage")

parser = subs.add_parser("list_pipelines")
parser.set_defaults(which = list_pipelines.which)
parser.add_argument("--project", default = None)

# dyno commands
parser = subs.add_parser("setup_dyno")
parser.set_defaults(which = setup_dyno.which)
parser.add_argument("project")
parser.add_argument("stage")
parser.add_argument("--config", default = "dyno.blocks.json")
parser.add_argument("--image_uri_f", default = "image_uri.txt")

def run():
    args = root.parse_args()

    if args.which == ROOT:
        root.print_help()
    elif args.which == INIT:
        init_domain()

    with Lock(__name__).lock():
        # source commands
        if args.which == setup_source.which:
            setup_source(args)
        elif args.which == destroy_source.which:
            destroy_source(args)
        elif args.which == list_sources.which:
            list_sources(args)

        # pipeline commands
        elif args.which == setup_pipeline.which:
            setup_pipeline(args)
        elif args.which == destroy_pipeline.which:
            destroy_pipeline(args)
        elif args.which == list_pipelines.which:
            list_pipelines(args)

        # dyno commands
        elif args.which == setup_dyno.which:
            setup_dyno(args)
        elif args.which == destroy_dyno.which:
            destroy_dyno(args)

run()