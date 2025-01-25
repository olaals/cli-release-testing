from typer import Typer
from manage_lib.prompts.prompt_git_commit import prompt_user_select_git_commit
from manage_lib.prompts.prompt_deployment_target import prompt_user_select_deployment_target
from manage_lib.prompts.prompt_version_update_type import prompt_user_select_version_update
from manage_lib.run_checks import run_checks
from manage_lib.checks.git_checks import is_working_tree_clean, is_current_branch_development, has_repo_access

app = Typer()

@app.command()
def create_release():
    """
    Create a new release with the specified version and description.
    """
    checks_passed = run_checks([is_working_tree_clean, is_current_branch_development, has_repo_access])
    if not checks_passed:
        print("Checks failed. Aborting...")
        return
    print("Release created successfully!")
    prompt_user_select_deployment_target()
    prompt_user_select_version_update()
    prompt_user_select_git_commit()


@app.command()
def placeholder():
    pass

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1:
        sys.argv.append("--help")
    app()