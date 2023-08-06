from lonny_aws_stack import Stack
from troposphere import elasticloadbalancingv2 as elb, ec2, route53, Template, Output, Ref, Join, AWS_REGION
from .base import Node, register, constructor
from .type import NodeType
from base64 import b32encode

VPC = "VPC"
BALANCER = "Balancer"
LISTENER = "Listener"
SUBNET_A = "SubnetA"
SUBNET_B = "SubnetB"
SECURITY_GROUP = "SecurityGroup"

def _get_vpc():
    return ec2.VPC("VPC", CidrBlock = "10.0.0.0/16")

def _get_internet_gateway():
    return ec2.InternetGateway("InternetGateway")

def _get_gateway_attachment(*, vpc, internet_gateway):
    return ec2.VPCGatewayAttachment("GatewayAttachment",
        VpcId = vpc,
        InternetGatewayId = internet_gateway
    )

def _get_route_table(vpc):
    return ec2.RouteTable("RouteTable",
        VpcId = vpc
    )

def _get_subnet_a(*, vpc):
    return ec2.Subnet("SubnetA",
        VpcId = vpc,
        MapPublicIpOnLaunch = True,
        CidrBlock = "10.0.0.0/19",
        AvailabilityZone = Join("", [Ref(AWS_REGION), "a"])
    )

def _get_subnet_b(*, vpc):
    return ec2.Subnet("SubnetB",
        VpcId = vpc,
        MapPublicIpOnLaunch = True,
        CidrBlock = "10.0.32.0/19",
        AvailabilityZone = Join("", [Ref(AWS_REGION), "b"])
    )

def _get_subnet_a_route_table_association(*, route_table, subnet_a):
    return ec2.SubnetRouteTableAssociation("SubnetARouteTableAssociation",
        RouteTableId = route_table,
        SubnetId=subnet_a
    )

def _get_subnet_b_route_table_association(*, route_table, subnet_b):
    return ec2.SubnetRouteTableAssociation("SubnetBRouteTableAssociation",
        RouteTableId = route_table,
        SubnetId=subnet_b
    )

def _get_public_route(*, route_table, internet_gateway):
    return ec2.Route("PublicRoute",
        RouteTableId = route_table,
        DestinationCidrBlock = "0.0.0.0/0",
        GatewayId = internet_gateway
    )

def _get_external_security_group(*, vpc):
    return ec2.SecurityGroup("ExternalSecurityGroup",
        VpcId = vpc,
        GroupDescription = "Security Group for public load balancer",
    )

def _get_external_security_group_rule_a(*, security_group):
    return ec2.SecurityGroupIngress("ExternalSecurityGroupRuleA",
        GroupId = security_group,
        IpProtocol = "tcp",
        FromPort = 443,
        ToPort = 443,
        CidrIp = "0.0.0.0/0"
    )

def _get_external_security_group_rule_b(*, security_group):
    return ec2.SecurityGroupIngress("ExternalSecurityGroupRuleB",
        GroupId = security_group,
        IpProtocol = "tcp",
        FromPort = 80,
        ToPort = 80,
        CidrIp = "0.0.0.0/0"
    )

def _get_internal_security_group(*, vpc):
    return ec2.SecurityGroup("InternalSecurityGroup",
        GroupDescription = "Security Group for internal services",
        VpcId = vpc,
    )

def _get_internal_security_group_rule_b(*, external_security_group, internal_security_group):
    return ec2.SecurityGroupIngress("InternalSecurityGroupRuleB",
        IpProtocol = "-1",
        SourceSecurityGroupId = external_security_group,
        GroupId = internal_security_group,
    )

def _get_internal_security_group_rule_a(*, security_group):
    return ec2.SecurityGroupIngress("InternalSecurityGroupRuleA",
        IpProtocol = "-1",
        SourceSecurityGroupId = security_group,
        GroupId = security_group,
    )

def _get_balancer(*, subnet_a, subnet_b, external_security_group):
    return elb.LoadBalancer("ApplicationLoadBalancer",
        SecurityGroups = [external_security_group],
        Subnets = [subnet_a, subnet_b]
    )

def _get_http_listener(*, balancer):
    return elb.Listener("HTTPListener",
        LoadBalancerArn = balancer,
        Port = 80,
        Protocol = "HTTP",
        DefaultActions = [elb.Action(
            Type = "redirect",
            RedirectConfig = elb.RedirectConfig(
                Host = "#{host}",
                Path = "/#{path}",
                Port = "443",
                Protocol = "HTTPS",
                Query = "#{query}",
                StatusCode = "HTTP_301"
            )
        )]
    )   

def _get_https_listener(*, balancer, domains):
    certificate_arns = list(set( x.certificate_arn for x in domains))
    certificate_arns.sort()
    return elb.Listener("HTTPSListener",
        LoadBalancerArn = balancer,
        Port = 443,
        Protocol = "HTTPS",
        Certificates = [elb.Certificate(CertificateArn = x) for x in certificate_arns],
        DefaultActions = [elb.Action(
            Type = "fixed-response",
            FixedResponseConfig = elb.FixedResponseConfig(StatusCode = "502")
        )]
    )

def _get_domain_alias(*, balancer_dns, balancer_hosted_zone_id, domain):
    encoded_suffix = b32encode(domain.name.encode("utf-8")).decode("utf-8").strip("=")
    return route53.RecordSetType(f"RecordSet{encoded_suffix}",
        Name = domain.name,
        Type = "A",
        HostedZoneId = domain.hosted_zone_id,
        AliasTarget = route53.AliasTarget(
            DNSName = balancer_dns,
            HostedZoneId = balancer_hosted_zone_id
        )
    )

def _get_template(*, domains):
    template = Template()

    vpc = _get_vpc()
    template.add_resource(vpc)

    gateway = _get_internet_gateway()
    template.add_resource(gateway)

    gateway_attachment = _get_gateway_attachment(
        vpc = vpc.ref(),
        internet_gateway = gateway.ref()
    )
    template.add_resource(gateway_attachment)

    route_table = _get_route_table(
        vpc = vpc.ref()
    )
    template.add_resource(route_table)

    subnet_a = _get_subnet_a(
        vpc = vpc.ref()
    )
    template.add_resource(subnet_a)

    subnet_b = _get_subnet_b(
        vpc = vpc.ref()
    )
    template.add_resource(subnet_b)

    template.add_resource(_get_subnet_a_route_table_association(
        route_table = route_table.ref(),
        subnet_a = subnet_a.ref()
    ))

    template.add_resource(_get_subnet_b_route_table_association(
        route_table = route_table.ref(),
        subnet_b = subnet_b.ref()
    ))

    template.add_resource(_get_public_route(
        route_table = route_table.ref(),
        internet_gateway = gateway.ref()
    ))

    external_security_group = _get_external_security_group(vpc = vpc.ref())
    template.add_resource(external_security_group)

    internal_security_group = _get_internal_security_group(vpc = vpc.ref())
    template.add_resource(internal_security_group)

    template.add_resource(_get_internal_security_group_rule_a(
        security_group = internal_security_group.ref(),
    ))

    template.add_resource(_get_external_security_group_rule_a(
        security_group = external_security_group.ref(),
    ))

    template.add_resource(_get_external_security_group_rule_b(
        security_group = external_security_group.ref(),
    ))

    template.add_resource(_get_internal_security_group_rule_b(
        internal_security_group = internal_security_group.ref(),
        external_security_group = external_security_group.ref(),
    ))

    balancer = _get_balancer(
        subnet_a = subnet_a.ref(),
        subnet_b = subnet_b.ref(),
        external_security_group = external_security_group.ref()
    )
    template.add_resource(balancer)

    http_listener = _get_http_listener(
        balancer = balancer.ref()
    )
    template.add_resource(http_listener)

    https_listener = _get_https_listener(
        balancer = balancer.ref(),
        domains = domains
    )
    template.add_resource(https_listener)

    domain_dict = { x.name : x for x in domains }
    for key in sorted(domain_dict.keys()):
        domain = domain_dict[key]
        template.add_resource(_get_domain_alias(
            balancer_dns = balancer.get_att("DNSName"),
            balancer_hosted_zone_id = balancer.get_att("CanonicalHostedZoneID"),
            domain = domain
        ))

    template.add_output(Output(BALANCER, Value = balancer.ref()))
    template.add_output(Output(LISTENER, Value = https_listener.ref()))
    template.add_output(Output(SUBNET_A, Value = subnet_a.ref()))
    template.add_output(Output(SUBNET_B, Value = subnet_b.ref()))
    template.add_output(Output(VPC, Value = vpc.ref()))
    template.add_output(Output(SECURITY_GROUP, Value = internal_security_group.ref()))

    return template

@register
class Docker(Node):
    @property
    def balancer(self):
        return self.sync()[BALANCER]

    @property
    def listener(self):
        return self.sync()[LISTENER]

    @property
    def subnets(self):
        output = self.sync()
        return [
            output[SUBNET_A],
            output[SUBNET_B]
        ]

    @property
    def vpc(self):
        return self.sync()[VPC]

    @property
    def security_group(self):
        return self.sync()[SECURITY_GROUP]

    def on_sync(self):
        super().on_sync()
        domains = list()
        DockerDeploy = constructor(NodeType.docker_deploy)
        for deploy in DockerDeploy.search():
            domains.extend(deploy.domains)
        if len(domains) == 0:
            Stack(self.name).down()
            return
        templ = _get_template(domains = domains).to_json()
        return Stack(self.name).up(templ)

    def on_destroy(self):
        Stack(self.name).down()
        super().on_destroy()

    @classmethod
    def decode(data):
        return Docker()

    node_type = NodeType.docker