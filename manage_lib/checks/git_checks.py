from typing import Tuple, Optional
from git import Repo, InvalidGitRepositoryError, GitCommandError

# All checks should have the same signature:
#  - return a tuple with a boolean and an optional string
#  - the boolean indicates whether the check passed or not, true for passed
#  - the optional string is a message that explains the result of the check

def has_repo_access() -> Tuple[bool, Optional[str]]:
    """
    Checks if the current user has access to the repository for operations like creating a PR.

    Returns:
        Tuple[bool, Optional[str]]: True if access is available, False with an error message otherwise.
    """
    try:
        repo = Repo(".")
        
        if not repo.remotes:
            return False, "No remotes are configured for this repository."
        
        remote = repo.remotes.origin
        remote.fetch()
        return True, None

    except InvalidGitRepositoryError:
        return False, "The current directory is not a valid Git repository."
    except GitCommandError as e:
        # Handle specific Git permission errors
        if "permission denied" in str(e).lower():
            return False, "Permission denied: You do not have access to the repository."
        else:
            return False, f"Git command error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"


def is_current_branch_development() -> Tuple[bool, Optional[str]]:
    try:
        repo = Repo(".")
        
        if repo.head.is_detached:
            return False, "The HEAD is detached, not on any branch."
        
        current_branch = repo.active_branch.name
        if current_branch == "development":
            return True, None
        else:
            return False, f"The current branch is '{current_branch}', not 'development'."
    
    except InvalidGitRepositoryError:
        return False, "The current directory is not a valid Git repository."
    except GitCommandError as e:
        return False, f"Git command error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"

def is_working_tree_clean() -> Tuple[bool, Optional[str]]:
    """
    Checks if the current Git repository's working tree is clean.
    
    Returns:
        Tuple[bool, Optional[str]]: True if clean, False with an error message otherwise.
    """
    try:
        # Initialize the Repo object for the current directory
        repo = Repo(".")
        
        # Check if there are staged, unstaged, or untracked changes
        if repo.is_dirty(untracked_files=True):
            return False, "The working tree has changes (staged, unstaged, or untracked files)."
        
        return True, None

    except InvalidGitRepositoryError:
        return False, "The current directory is not a valid Git repository."
    except GitCommandError as e:
        return False, f"Git command error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"
