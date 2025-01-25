# manage_lib/prompts/prompt_version_update.py
from InquirerPy.prompts.list import ListPrompt
from ..models import VersionUpdateType

def prompt_user_select_version_update() -> VersionUpdateType:
    """Prompt the user to select a version update type."""
    try:
        # Prepare choices for the prompt
        choices = [
            (update_type.value, update_type) for update_type in VersionUpdateType
        ]

        # Prompt user to select a version update type
        selected_update_value = ListPrompt(
            message="Select a version update type:",
            choices=[choice[0] for choice in choices],
            validate=lambda result: bool(result),
            invalid_message="You must select a version update type.",
        ).execute()

        # Find the selected version update type
        selected_update = next(
            update_type for value, update_type in choices if value == selected_update_value
        )

        return selected_update

    except Exception as e:
        print(f"Error: {e}")
        raise
