from dataclasses import dataclass


@dataclass
class WorkerInfo:
    id: str
    name: str
    groups: list
    health: float
    health_verbose: str
    clock: dict
    job_details: dict
