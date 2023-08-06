import httpx

from yatb.types import Update


async def poll_updates(
    token: str,
    client: httpx.AsyncClient,
    offset: int = None,
    limit: int = None,
    timeout: int = None,
    allowed_updates: str = None,
):
    offset = offset or 0

    while True:
        updates_data = await get_updates(
            token, client, offset, limit, timeout, allowed_updates
        )

        for update_data in updates_data["result"]:
            print(update_data)
            yield Update(**update_data)
            offset = update_data["update_id"] + 1


async def get_updates(
    token: str,
    client: httpx.AsyncClient,
    offset: int = None,
    limit: int = None,
    timeout: int = None,
    allowed_updates: str = None,
):
    """
    Use this method to receive incoming updates using long polling.
    An Array of Update objects is returned.

    https://core.telegram.org/bots/api#getupdates
    """
    response = await client.get(
        f"https://api.telegram.org/bot{token}/getUpdates",
        params={
            "offset": offset,
            "limit": limit,
            "timeout": timeout,
            "allowed_updates": allowed_updates,
        },
    )

    return response.json()
