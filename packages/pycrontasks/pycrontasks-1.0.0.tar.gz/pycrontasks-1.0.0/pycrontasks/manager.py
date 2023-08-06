from __future__ import annotations

from asyncio import sleep, get_event_loop
from importlib.util import find_spec, module_from_spec
from os import listdir
from os.path import sep
from typing import Tuple

from .errors import NoEntryPointFoundError
from .task import Task


class TaskManager():
    # TODO: task reloading/unloading

    def __enter__(self): return self
    def __exit__(self, *args): ...
    def __init__(self, ctx: object):
        self.tasks = []
        self.ctx = ctx

    def add_tasks(self, *tasks, reload: bool=True):
        for task in tasks:
            if not isinstance(task, Task):
                raise TypeError("tasks need to derive from Task")
            if task in self:
                if not reload:
                    continue
                else:
                    self.pop_task(str(task))
                    
            task._ctx = self.ctx
            self.tasks.append(task)

    def load_tasks_from_file(self, fname: str):
        spec = find_spec(fname, package=".")
        if spec is None:
            raise FileNotFoundError
        tasklib = module_from_spec(spec)
        spec.loader.exec_module(tasklib)

        if hasattr(tasklib, "enter"):
            tasklib.enter(self)
        else:
            raise NoEntryPointFoundError("Task files need to provide a `enter` method")

    def load_tasks_from_folder(self, fpath: str):
        # TODO: clean this up, this is ugly
        for f in listdir(fpath.replace(".", sep)):
            fp = f"{fpath.replace(sep, '.').replace('/', '.')}.{f}"
            if fp.endswith(".py") and not "__" in fp:
                self.load_tasks_from_file(fp[:-3])
        return self
                
    async def check_on_tasks(self):
        for task in self.tasks:
            await task._run_if_time(self.ctx)

    async def run_startup_tasks(self):
        for task in self.tasks:
            await task._run_on_reboot(self.ctx)

    def __getitem__(self, key):
        for task in self.tasks:
            if key == str(task):
                return task
        raise KeyError()
    
    def __contains__(self, key):
        try:
            _ = self[str(key)]
            return True
        except KeyError:
            return False

    def __iter__(self):
        for task in self.tasks:
            yield task
    
    def pop_task(self, task: str):
        _task = self[task]
        self.tasks.remove(_task)
        del _task    

    def pop_tasks(self, tasks: Tuple[str]):
        for task in tasks:
            self.pop_task(task)

    async def arun(self, delay: int=1):
        await self.run_startup_tasks()

        while True:
            await self.check_on_tasks()
            sleep(1)

    def run(self, delay: int=1):
        loop = get_event_loop()
        loop.run_until_complete(self.arun(delay))
