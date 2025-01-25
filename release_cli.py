from git import Repo, GitCommandError
from contextlib import ExitStack
from dataclasses import dataclass
from typing import List, Optional
from InquirerPy.prompts.fuzzy import FuzzyPrompt

@dataclass
class CommitData:
    short_hash: str
    long_hash: str
    message: str
    author: str
    tags: List[str]

def get_git_commits() -> List[CommitData]:
    """Retrieve a list of commits with detailed data from the git repository."""
    try:
        with ExitStack():
            print("Getting commits...")
            repo = Repo(".")
            if repo.bare:
                print("Not a valid git repository.")
                raise Exception("Not a valid git repository.")

            # Get the commits (newest first)
            commits = []
            for commit in repo.iter_commits():
                # Find tags associated with the commit
                tags = [tag.name for tag in repo.tags if tag.commit == commit]
                commits.append(
                    CommitData(
                        short_hash=commit.hexsha[:7],
                        long_hash=commit.hexsha,
                        message=str(commit.message.strip()),
                        author=str(commit.author.name),
                        tags=tags,
                    )
                )

            if not commits:
                raise Exception("No commits found in the repository.")
            return commits

    except GitCommandError as e:
        raise Exception(f"Git error while retrieving commits: {e}")
    except Exception as e:
        raise Exception(f"Error while retrieving commits: {e}")

def main():
    try:
        # Retrieve commits
        commits = get_git_commits()

        # Prepare choices for the prompt
        choices = [
            f"{commit.short_hash} - {commit.message} ({commit.author}) [Tags: {', '.join(commit.tags) or 'None'}]"
            for commit in commits
        ]

        # Prompt user to select a commit
        selected_commit_str = FuzzyPrompt(
            message="Select a commit:",
            choices=choices,
            validate=lambda result: bool(result),
            invalid_message="You must select a commit.",
            max_height="70%",  # Adjust height if needed
        ).execute()

        # Find the selected commit data
        selected_commit = next(
            (commit for commit, choice in zip(commits, choices) if choice == selected_commit_str),
            None,
        )

        if not selected_commit:
            raise Exception("Selected commit not found.")

        # Print the selected commit
        print("Selected Commit:")
        print(f"  Short Hash: {selected_commit.short_hash}")
        print(f"  Long Hash: {selected_commit.long_hash}")
        print(f"  Message: {selected_commit.message}")
        print(f"  Author: {selected_commit.author}")
        print(f"  Tags: {', '.join(selected_commit.tags) or 'None'}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
