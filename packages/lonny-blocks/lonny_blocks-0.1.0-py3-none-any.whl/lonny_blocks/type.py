from enum import Enum, auto

class NodeType(Enum):
    source = auto()
    pipeline = auto()
    docker = auto()
    docker_deploy = auto()

class Machine(Enum):
        lean = (256, 512)
        lean_x2 = (256, 1024)
        standard = (512, 1024)
        standard_x2 = (512, 2048)
        heavy = (1024, 2048)
        heavy_x2 = (1024, 4096)

class ProcDef:
    def __init__(self, * entry, instances, machine):
        self.entry = list(entry)
        self.instances = instances
        self.machine = machine

    def encode(self):
        return dict(
            entry = self.entry,
            instances = self.instances,
            machine = self.machine.name
        )

    @staticmethod
    def decode(data):
        return ProcDef(
            data["entry"],
            instances = data["instances"],
            machhine = Machine[data["machine"]]
        )

class DomainName:
    def __init__(self, name, *, certificate_arn, hosted_zone_id):
        self.name = name
        self.certificate_arn = certificate_arn
        self.hosted_zone_id = hosted_zone_id

    def encode(self):
        return dict(
            name = self.name,
            certificate_arn = self.certificate_arn,
            hosted_zone_id = self.hosted_zone_id
        )
    
    @staticmethod
    def decode(data):
        return DomainName(
            data["name"],
            certificate_arn = data["certificate_arn"],
            hosted_zone_id = data["hosted_zone_id"]
        )