from ..models import SemanticVersion
from git import Repo, GitCommandError


def get_current_version(deployment_target: str) -> SemanticVersion:
    """
    Retrieve the current semantic version for a given deployment target based on Git tags.

    Args:
        deployment_target (str): The deployment target (e.g., "api", "db").

    Returns:
        SemanticVersion: The current version of the deployment target.
    """
    try:
        repo = Repo(".")
        tags = repo.tags

        # Filter tags that match the deployment target
        target_tags = [
            tag.name for tag in tags if tag.name.startswith(f"{deployment_target}/v")
        ]

        if not target_tags:
            return SemanticVersion(0, 0, 0)  # No previous tag, return default version

        # Extract the versions from the tags
        versions = []
        for tag in target_tags:
            try:
                version_str = tag.split("/")[1]
                versions.append(SemanticVersion.from_string(version_str))
            except ValueError:
                continue

        # Find the latest version
        latest_version = max(
            versions, key=lambda v: (v.major, v.minor, v.patch), default=SemanticVersion(0, 0, 0)
        )

        return latest_version

    except GitCommandError as e:
        raise Exception(f"Git command error: {e}")
    except Exception as e:
        raise Exception(f"Error while retrieving the current version: {e}")
