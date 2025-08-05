import asyncio
from collections import defaultdict

_email_locks = defaultdict(asyncio.Lock)

async def get_email_lock(email: str) -> asyncio.Lock:
    return _email_locks[email]
