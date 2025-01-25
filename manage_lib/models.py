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

@dataclass
class SemanticVersion:
    major: int
    minor: int
    patch: int

    def as_string(self) -> str:
        return f"v{self.major}.{self.minor}.{self.patch}"

    @staticmethod
    def from_string(version: str) -> "SemanticVersion":
        try:
            version = version.lstrip("v")
            major, minor, patch = map(int, version.split("."))
            return SemanticVersion(major, minor, patch)
        except Exception as e:
            raise ValueError(f"Invalid version format: {version}") from e
