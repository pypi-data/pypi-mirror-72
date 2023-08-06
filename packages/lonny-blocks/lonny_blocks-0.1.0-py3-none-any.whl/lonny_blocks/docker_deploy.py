from lonny_aws_stack import Stack
import boto3
from base64 import b32encode
from troposphere import Template, iam, ecs, ecr, elasticloadbalancingv2 as elb, Join, Ref, Output, AWS_ACCOUNT_ID, AWS_REGION
from .base import Node, register, constructor
from .type import DomainName, ProcDef, NodeType
import json

CONTAINER_PORT = 8080
ADMIN_POLICY_ARN = "arn:aws:iam::aws:policy/AdministratorAccess"
WEB_PROC_NAME = "web"
SECRET_ENV = "BLOCKS_SECRET"
REGISTRY_URI = "ContainerRegistryURI"
REGISTRY_NAME = "RegistryName"

client_ecr = boto3.client("ecr")

def _get_cluster():
    return ecs.Cluster("Cluster")

def _get_task_def(*, machine, proc_name, entry_point, image_uri, role_arn, secret_arn):
    encoded = b32encode(proc_name.encode("utf-8")).decode("utf-8").strip("=")
    return ecs.TaskDefinition(f"TaskDefinition{encoded}",
        ExecutionRoleArn = role_arn,
        TaskRoleArn = role_arn,
        NetworkMode = "awsvpc",
        RequiresCompatibilities = ["FARGATE"],
        Cpu = str(machine.value[0]),
        Memory = str(machine.value[1]),
        ContainerDefinitions = [
            ecs.ContainerDefinition(
                Name = proc_name,
                EntryPoint = entry_point,
                Secrets = list() if secret_arn is None else [ecs.Secret(
                    Name = SECRET_ENV,
                    ValueFrom = secret_arn
                )],
                Image = image_uri,
                PortMappings = list() if proc_name != WEB_PROC_NAME else [ecs.PortMapping(
                    ContainerPort = CONTAINER_PORT,
                    HostPort = CONTAINER_PORT
                )]
            )
        ]
    )

def _get_service(*, proc_name, task_definition, cluster, instances, target_group, subnets, internal_security_group):
    encoded = b32encode(proc_name.encode("utf-8")).decode("utf-8").strip("=")
    return ecs.Service(f"Service{encoded}",
        Cluster = cluster,
        TaskDefinition = task_definition,
        LaunchType = "FARGATE",
        LoadBalancers = list() if proc_name != WEB_PROC_NAME else [ecs.LoadBalancer(
            ContainerName = proc_name,
            ContainerPort = CONTAINER_PORT,
            TargetGroupArn = target_group,
        )],
        DesiredCount = instances,
        NetworkConfiguration = ecs.NetworkConfiguration(
            AwsvpcConfiguration = ecs.AwsvpcConfiguration(
                AssignPublicIp = "ENABLED",
                SecurityGroups = [internal_security_group],
                Subnets = subnets
            ) 
        )
    )

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
            Values = [x.name for x in domains]
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

def _get_template(*, vpc, domains, image_uri, subnets, listener, procs, security_group, secret_arn):
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

    for proc_name, proc_def in procs.items():
        task_def = _get_task_def(
            machine = proc_def.machine,
            proc_name = proc_name,
            entry_point = proc_def.entry,
            secret_arn = secret_arn,
            image_uri = image_uri,
            role_arn = role.get_att("Arn")
        )
        template.add_resource(task_def)

        template.add_resource(_get_service(
            proc_name = proc_name,
            task_definition = task_def.ref(),
            cluster = cluster.ref(),
            instances = proc_def.instances,
            target_group = target_group.ref(),
            subnets = subnets,
            internal_security_group = security_group
        ))

    output_value = Join("", [Ref(AWS_ACCOUNT_ID), ".dkr.ecr.", Ref(AWS_REGION), ".amazonaws.com/", registry.ref()])
    template.add_output(Output(REGISTRY_URI, Value = output_value))
    template.add_output(Output(REGISTRY_NAME, Value = registry.get_att("RepositoryName")))

    return template

@register
class DockerDeploy(Node):
    def __init__(self, project, stage, *, domains, procs, image_uri, secret_arn = None):
        self._project = project
        self._stage = stage
        self._procs = procs
        self._secret_arn = secret_arn
        self._image_uri = image_uri
        self.domains = domains

    def get_parts(self):
        return [self._project, self._stage]

    def encode(self):
        return dict(
            project = self._project,
            stage = self._stage,
            domains = json.dumps([x.encode() for x in self.domains]),
            procs = json.dumps({ k : v.encode() for k,v in self.procs.items()}),
            secret_arn = self._secret_arn,
            image_uri = self._image_uri
        )

    def on_destroy(self):
        stack = Stack(self.name)
        data = stack.peek()
        if data is not None:
            try:
                client_ecr.delete_repository(
                    repositoryName = data[REGISTRY_NAME],
                    force = True
                )
            except client_ecr.exceptions.RepositoryNotFoundException:
                pass
        Stack(self.name).down()
        super().on_destroy()
        docker = constructor(NodeType.docker)()
        docker.sync(force = True)

    def on_sync(self):
        super().on_sync()
        docker = constructor(NodeType.docker)()
        docker.sync(force = True)
        templ = _get_template(
            domains = self.domains,
            secret_arn = self._secret_arn,
            procs = self._procs,
            image_uri = self._image_uri,
            vpc = docker.vpc,
            subnets = docker.subnets,
            listener = docker.listener,
            security_group = docker.security_group
        ).to_json()
        return Stack(self.name).up(templ)

    @property
    def registry_uri(self):
        return self.sync()[REGISTRY_URI]

    @staticmethod
    def decode(data):
        return DockerDeploy(
            data["project"], 
            data["stage"],
            image_uri = data["image_uri"],
            domains = [DomainName.decode(x) for x in json.loads(data["domains"])],
            procs = { k : ProcDef.decode(v) for k,v in json.loads(data["procs"]).items() },
            secret_arn = data["secret_arn"]
        )

    node_type = NodeType.docker_deploy