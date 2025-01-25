from InquirerPy.prompts.list import ListPrompt
from ..models import DeploymentTarget

def prompt_user_select_deployment_target() -> DeploymentTarget:
    """Prompt the user to select a deployment target."""
    try:
        # Prepare choices for the prompt
        choices = [
            (target.value, target) for target in DeploymentTarget
        ]

        # Prompt user to select a deployment target
        selected_target_value = ListPrompt(
            message="Select a deployment target:",
            choices=[choice[0] for choice in choices],
            validate=lambda result: bool(result),
            invalid_message="You must select a deployment target.",
        ).execute()

        # Find the selected deployment target
        selected_target = next(
            target for value, target in choices if value == selected_target_value
        )

        return selected_target

    except Exception as e:
        print(f"Error: {e}")
        raise
