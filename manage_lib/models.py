from dataclasses import dataclass
from typing import List
from enum import Enum

class VersionUpdateType(str, Enum):
    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"

class DeploymentTarget(str, Enum):
    DB = "db"
    API = "api"

@dataclass
class CommitData:
    short_hash: str
    long_hash: str
    message: str
    author: str
    tags: List[str]
