from lonny_aws_stack import Stack
from troposphere import elasticloadbalancingv2 as elb, ec2, route53, Template, Output, Join, Ref, AWS_REGION
from .base import Resource, constructor, register
from .type import ResourceType
from base64 import b32encode

SUBNET_A = "SubnetA"
SUBNET_B = "SubnetB"
SECURITY_GROUP = "SecurityGroup"
INGRESS_PORTS = [80, 443]
VPC = "VPC"
LISTENER = "Listener"

def _get_balancer(*, subnet_a, subnet_b, security_group):
    return elb.LoadBalancer("ApplicationLoadBalancer",
        SecurityGroups = [security_group],
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
    certs = set(x["certificate_arn"] for x in domains)
    return elb.Listener("HTTPSListener",
        LoadBalancerArn = balancer,
        Port = 443,
        Protocol = "HTTPS",
        Certificates = [
            elb.Certificate(CertificateArn = x) for x in certs
        ],
        DefaultActions = [elb.Action(
            Type = "fixed-response",
            FixedResponseConfig = elb.FixedResponseConfig(StatusCode = "502")
        )]
    )

def _get_domain_alias(*, balancer_dns, balancer_hosted_zone_id, domain):
    encoded_suffix = b32encode(domain["name"].encode("utf-8")).decode("utf-8").strip("=")
    return route53.RecordSetType(f"RecordSet{encoded_suffix}",
        Name = domain["name"],
        Type = "A",
        HostedZoneId = domain["hosted_zone_id"],
        AliasTarget = route53.AliasTarget(
            DNSName = balancer_dns,
            HostedZoneId = balancer_hosted_zone_id
        )
    )

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

def _get_external_security_group_rule(*, port, security_group):
    return ec2.SecurityGroupIngress(f"ExternalSecurityGroupRule{port}",
        GroupId = security_group,
        IpProtocol = "tcp",
        FromPort = port,
        ToPort = port,
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

    template.add_resource(_get_internal_security_group_rule_b(
        internal_security_group = internal_security_group.ref(),
        external_security_group = external_security_group.ref(),
    ))

    for port in INGRESS_PORTS:
        template.add_resource(_get_external_security_group_rule(
            port = port,
            security_group = external_security_group.ref(),
        ))

    balancer = _get_balancer(
        subnet_a = subnet_a.ref(),
        subnet_b = subnet_b.ref(),
        security_group = external_security_group.ref()
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

    for domain in domains:
        template.add_resource(_get_domain_alias(
            balancer_dns = balancer.get_att("DNSName"),
            balancer_hosted_zone_id = balancer.get_att("CanonicalHostedZoneID"),
            domain = domain
        ))

    template.add_output(Output(LISTENER, Value = https_listener.ref()))
    template.add_output(Output(SUBNET_A, Value = subnet_a.ref()))
    template.add_output(Output(SUBNET_B, Value = subnet_b.ref()))
    template.add_output(Output(VPC, Value = vpc.ref()))
    template.add_output(Output(SECURITY_GROUP, Value = internal_security_group.ref()))
    return template

@register
class DynoBalancer(Resource):
    def on_update(self):
        DynoConfig = constructor(ResourceType.dyno_config)
        domains = list()
        for config in DynoConfig.search():
            domains.extend(config.get_data()["domains"])
        if len(domains) == 0:
            self.destroy()
            return
        templ = _get_template(domains = domains).to_json()
        data = Stack(self.get_name()).up(templ)
        return dict(
            listener = data[LISTENER],
            subnets = [data[SUBNET_A], data[SUBNET_B]],
            security_group = data[SECURITY_GROUP],
            vpc = data[VPC]
        )

    def on_destroy(self):
        Stack(self.get_name()).down()

    def get_listener(self):
        return self.get_data()[LISTENER]

    @staticmethod
    def from_tags(tags):
        return DynoBalancer()

    resource_type = ResourceType.dyno_balancer