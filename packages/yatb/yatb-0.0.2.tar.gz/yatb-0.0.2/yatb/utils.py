from . import types


def extract_command(update: types.Update) -> str:
    """
    Extract invoked bot command from a given Update (without a leading slash)
    Returns empty string if a given Update is not related to a bot command
    """
    command = ""

    if (
        update.message is None
        or update.message.text is None
        or update.message.entities is None
    ):
        return command

    for mentity in update.message.entities:
        value = mentity.type.value
        if value == types.MessageEntityType.bot_command.value:  # noqa: E721
            command = update.message.text[mentity.offset : mentity.length]
            break

    return command.lstrip("/")
