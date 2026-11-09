"""
Production background task executor (clean control sample).
"""
import asyncio

class TaskExecutor:
    def __init__(self, concurrency: int = 5):
        self.semaphore = asyncio.Semaphore(concurrency)

    async def execute(self, task_id: str, coro):
        async with self.semaphore:
            return await coro()
