import httpx

API_BASE_URL = "http://backend:8000"


async def create_task(data: dict):
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{API_BASE_URL}/tasks/", json=data)
        resp.raise_for_status()
        return resp.json()


async def list_tasks(telegram_user_id: int):
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{API_BASE_URL}/tasks/", params={"telegram_user_id": telegram_user_id}
        )
        resp.raise_for_status()
        return resp.json()


async def mark_done(task_id: int):
    async with httpx.AsyncClient() as client:
        resp = await client.patch(f"{API_BASE_URL}/tasks/{task_id}/", json={"status": "done"})
        resp.raise_for_status()
        return resp.json()


async def mark_undone(task_id: int):
    async with httpx.AsyncClient() as client:
        resp = await client.patch(f"{API_BASE_URL}/tasks/{task_id}/", json={"status": "undone"})
        resp.raise_for_status()
        return resp.json()


async def get_task_detail(task_id: int):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{API_BASE_URL}/tasks/{task_id}/")
        resp.raise_for_status()
        return resp.json()
