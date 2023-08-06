from enum import Enum

class ResourceType(Enum):
    source = "source"
    pipeline = "pipeline"
    dyno = "dyno"
    dyno_balancer = "dyno-balancer"
    dyno_config = "dyno-config"

class Machine(Enum):
        lean = (256, 512)
        lean_x2 = (256, 1024)
        standard = (512, 1024)
        standard_x2 = (512, 2048)
        heavy = (1024, 2048)
        heavy_x2 = (1024, 4096)