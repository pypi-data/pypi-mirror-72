from lonny_aws_stack import Stack
from troposphere import Template, iam, ecs, ecr, elasticloadbalancingv2 as elb, Join, Ref, Output, AWS_ACCOUNT_ID, AWS_REGION
from .command import Command
from .type import ResourceType, Machine
from .base import Resource, constructor, register
import boto3
import json

CONTAINER_PORT = 8080
ADMIN_POLICY_ARN = "arn:aws:iam::aws:policy/AdministratorAccess"
WEB_PROC_NAME = "web"
SECRET_ENV = "BLOCKS_SECRET"
IMAGE_URI = "ContainerRegistryURI"
REGISTRY_NAME = "RegistryName"
CLUSTER = "Cluster"
TARGET_GROUP = "TargetGroup"
ROLE_ARN = "RoleArn"

client_ecr = boto3.client("ecr")
client_ecs = boto3.client("ecs")

def _get_cluster():
    return ecs.Cluster("Cluster")

def _get_target_group(*, vpc):
    return elb.TargetGroup("TargetGroup",
        Port = CONTAINER_PORT,
        Protocol = "HTTP",
        VpcId = vpc,
        TargetType = "ip" 
    )

def _get_https_listener_rule(*, domains, listener, target_group):
    return elb.ListenerRule("ListenerRule",
        ListenerArn = listener,
        Priority = 1,
        Conditions = [elb.Condition(
            Field = "host-header",
            Values = [x["name"] for x in domains]
        )],
        Actions = [elb.Action(
            Type = "forward",
            TargetGroupArn = target_group
        )]
    )

def _get_container_registry():
    return ecr.Repository("ContainerRegistry")

def _get_ecs_role():
    return iam.Role("ECSRole",
        AssumeRolePolicyDocument = dict(
            Statement = [dict(
                Action = [ "sts:AssumeRole" ],
                Effect = "Allow",
                Principal = dict(Service = "ecs-tasks.amazonaws.com")
            )]
        ),
        ManagedPolicyArns = [ADMIN_POLICY_ARN]
    )

def _get_template(*, vpc, domains, subnets, listener, security_group):
    template = Template()

    cluster = _get_cluster()
    template.add_resource(cluster)

    target_group = _get_target_group(vpc = vpc)
    template.add_resource(target_group)

    role = _get_ecs_role()
    template.add_resource(role)

    template.add_resource(_get_https_listener_rule(
        domains = domains,
        listener = listener,
        target_group = target_group.ref()
    ))

    registry = _get_container_registry()
    template.add_resource(registry)

    image_uri = Join("", [
        Ref(AWS_ACCOUNT_ID), 
        ".dkr.ecr.", 
        Ref(AWS_REGION), 
        ".amazonaws.com/", 
        registry.ref(),
        ":latest",
    ])

    template.add_output(Output(IMAGE_URI, Value = image_uri))
    template.add_output(Output(REGISTRY_NAME, Value = registry.ref()))
    template.add_output(Output(CLUSTER, Value = cluster.ref()))
    template.add_output(Output(TARGET_GROUP, Value = target_group.ref()))
    template.add_output(Output(ROLE_ARN, Value = role.get_att("Arn")))
    return template

def _purge_container_registry(registry_name):
    while True:
        images = client_ecr.list_images(repositoryName = registry_name).get("imageIds", list())
        if len(images) == 0:
            break
        client_ecr.batch_delete_image(
            repositoryName = registry_name,
            imageIds = [dict(imageTag = x["imageTag"]) for x in images]
        )

def _register_task_definition(*, cluster, proc_name, proc_def, role, image, secrets_arn):
    machine = Machine[proc_def["machine"]]
    return client_ecs.register_task_definition(
        family = proc_name,
        taskRoleArn = role,
        executionRoleArn = role,
        networkMode = "awsvpc",
        requiresCompatibilities = ["FARGATE"],
        cpu = str(machine.value[0]),
        memory = str(machine.value[1]),
        containerDefinitions = [dict(
            name = proc_name,
            entryPoint = proc_def["entry"],
            secrets = list() if secrets_arn is None else [dict(
                name = SECRET_ENV,
                valueFrom = secrets_arn,
            )],
            image = image,
            portMappings = list() if proc_name != WEB_PROC_NAME else [dict(
                containerPort = CONTAINER_PORT,
                hostPort = CONTAINER_PORT
            )]
        )]
    )["taskDefinition"]["taskDefinitionArn"]

def _create_service(*, cluster, proc_name, proc_def, task_definition_arn, target_group, subnets, security_group):
    client_ecs.create_service(
        cluster = cluster,
        serviceName = proc_name,
        launchType = "FARGATE",
        taskDefinition = task_definition_arn,
        loadBalancers = list() if proc_name != WEB_PROC_NAME else [dict(
            targetGroupArn = target_group,
            containerName = proc_name,
            containerPort = CONTAINER_PORT
        )],
        desiredCount = proc_def["instances"],
        networkConfiguration = dict(
            awsvpcConfiguration = dict(
                subnets = subnets,
                securityGroups = [security_group],
                assignPublicIp = "ENABLED"
            )
        )
    )

def _update_service(*, cluster, task_definition_arn, proc_name, proc_def):
    client_ecs.update_service(
        cluster = cluster,
        service = proc_name,
        desiredCount = proc_def["instances"],
        taskDefinition = task_definition_arn,
        forceNewDeployment = True
    )

def _delete_service(*, cluster, proc_name):
    client_ecs.update_service(cluster = cluster, service = proc_name, desiredCount = 0)
    client_ecs.delete_service(cluster = cluster, service = proc_name)

def _get_service_arns(*, cluster, next_token = None):
    data = client_ecs.list_services(
        cluster = cluster,
        ** dict() if next_token is None else dict(nextToken = next_token)
    )
    for arn in data["serviceArns"]:
        yield arn
    next_token = data.get("nextToken")
    if next_token is None:
        return
    for arn in _get_service_arns(cluster = cluster, next_token = next_token):
        yield arn

def _get_services(*, cluster):
    for arn in _get_service_arns(cluster = cluster):
        yield client_ecs.describe_services(
            cluster = cluster, 
            services = [arn]
        )["services"][0]

@register
class Dyno(Resource):
    def __init__(self, *, project, stage):
        self._project = project
        self._stage = stage

    def get_tags(self):
        return dict(
            project = self._project,
            stage = self._stage
        )

    def get_domains(self, domains):
        return json.loads(self.get_domains_blob().get()["domains"])

    def on_update(self, *, procs, domains, secrets_arn = None):
        Pipeline = constructor(ResourceType.pipeline)
        DynoConfig = constructor(ResourceType.dyno_config)
        DynoBalancer = constructor(ResourceType.dyno_balancer)
        Pipeline(project = self._project, stage = self._stage).get_data()
        DynoConfig(project = self._project, stage = self._stage).update(domains = domains)
        balancer = DynoBalancer().update()
        templ = _get_template(
            domains = domains,
            vpc = balancer["vpc"],
            subnets = balancer["subnets"],
            listener = balancer["listener"],
            security_group = balancer["security_group"]
        ).to_json()
        output = Stack(self.get_name()).up(templ)

        service_map = { x["serviceName"] : x for x in _get_services(cluster = output[CLUSTER]) }
        for name, service in service_map.items():
            if name not in procs:
                _delete_service(cluster = output[CLUSTER], name = name)
        for proc_name, proc_def in procs.items():
            task_def_arn = _register_task_definition(
                cluster = output[CLUSTER],
                proc_name = proc_name,
                proc_def = proc_def,
                role = output[ROLE_ARN],
                image = output[IMAGE_URI],
                secrets_arn = secrets_arn
            )
            if proc_name in service_map:
                _update_service(
                    cluster = output[CLUSTER],
                    task_definition_arn = task_def_arn,
                    proc_name = proc_name,
                    proc_def = proc_def
                )
            else:
                _create_service(
                    cluster = output[CLUSTER],
                    task_definition_arn = task_def_arn,
                    proc_name = proc_name,
                    proc_def = proc_def,
                    target_group = output[TARGET_GROUP],
                    subnets = balancer["subnets"],
                    security_group = balancer["security_group"]
                )
        return dict(
            image_uri = output[IMAGE_URI]
        )

    def on_destroy(self):
        DynoConfig = constructor(ResourceType.dyno_config)
        DynoBalancer = constructor(ResourceType.dyno_balancer)
        stack = Stack(self.get_name())
        data = stack.peek()
        if data is not None:
            _purge_container_registry(data[REGISTRY_NAME])
            for service in _get_services(cluster = data[CLUSTER]):
                _delete_service(cluster = data[CLUSTER], name = service["serviceName"])
        stack.down()
        for domain_set in DynoConfig.search(project = self._project, stage = self._stage):
            domain_set.destroy()
        DynoBalancer().update()

    @staticmethod
    def from_tags(tags):
        return Dyno(
            project = tags["project"],
            stage = tags["stage"]
        )

    resource_type = ResourceType.dyno

@Command
def setup_dyno(args):
    with open(args.config) as f:
        config = json.loads(f.read())
    dyno = Dyno(project = args.project, stage = args.stage)
    image_uri = dyno.update(
        domains = config["domains"],
        procs = config["procs"]
    )["image_uri"]
    with open(args.image_uri_f, "w") as f:
        f.write(image_uri)

@Command
def destroy_dyno(args):
    dyno = Dyno(project = args.project, stage = args.stage)
    dyno.destroy()