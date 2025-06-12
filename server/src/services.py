import asyncio
import json


class BusinessLogic:

    progress_store = {}
    result_store = {}

    @classmethod
    async def long_running_task(cls, task_id: str):
        """
        Длительная задача на расчет
        """
        total_steps = 100
        for i in range(1, total_steps + 1):
            await asyncio.sleep(0.2)
            cls.progress_store[task_id] = i
        result = {"message": "Task completed", "task_id": task_id}
        cls.result_store[task_id] = result

    @classmethod
    async def cache_checker(cls, request, task_id):
        """
        Стриминг кэша для SSE
        """
        last_sent = 0
        while True:
            if await request.is_disconnected():
                break
            current = cls.progress_store.get(task_id, 0)
            if current != last_sent:
                data = {"progress": current}
                if current >= 100 and task_id in cls.result_store:
                    data["result"] = cls.result_store[task_id]
                    yield f"data: {json.dumps(data)}\n\n"
                    break
                yield f"data: {json.dumps(data)}\n\n"
                last_sent = current
            await asyncio.sleep(0.2)