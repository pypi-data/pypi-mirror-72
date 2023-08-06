import asyncio
import json

class Storage:
    def __init__(self, filename):
        self.filename = filename
        self._task = None
        self.load()

    def load(self):
        self.data = {}
        try:
            self.data.update(json.load(open(self.filename, 'r', encoding='utf-8')))
        except:
            pass

    def dump(self):
        json.dump(self.data, open(self.filename, 'w', encoding='utf-8'))

    async def _dump_later(self):
        await asyncio.sleep(3)
        self.dump()
        self._task = None

    def dump_later(self):
        if self._task is not None:
            self._task.cancel()
        self._task = asyncio.create_task(self._dump_later())

    def get(self, key, default=None):
        return self.data.get(key)

    def set(self, key, value):
        self.data[key] = value
        self.dump_later()

    def remove(self, key):
        self.data.pop(key, None)
        self.dump_later()
