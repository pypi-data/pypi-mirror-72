from time import time
from typing import Callable

from croniter import croniter


class Task():
    _ctx: object = None
    _reboot: bool = False
    _always: bool = False
    time_str: str = None
    _only_startup: bool = False
    _next_scheduled_run: float = 0
    def __init__(self, time_str: str, func: Callable):
        self.callback = func
        self._parse_time(time_str)
        if not self._only_startup:
            self._get_next_scheduled_run()
 
    def _parse_time(self, time_str: str):
        """Parses non-standard aliases and then passes the time string to croniter.  
        """
        self.time_str = time_str
        if time_str.startswith("@reboot"):
            self._reboot = True
            time_str = time_str[7:].strip()
        
            if not time_str:
                self._only_startup = True
                return
        elif time_str.startswith("@always"):
            self._always = True
            return
        elif time_str.startswith("@hourly"):
            time_str = "*/60 * * * *"
        elif time_str.startswith("@daily"):
            time_str = "0 */24 * * *"
        self._cron = croniter(time_str)

    async def __call__(self, ctx=None, *args, **kwargs):
        if ctx is None:
            ctx = self._ctx
        await self.callback(ctx, *args, **kwargs)

    def _get_next_scheduled_run(self):
        if not self._always:
            self._next_scheduled_run = self._cron.get_next()

    async def _run_if_time(self, ctx=None):
        if ctx is None:
            ctx = self._ctx
        _time = time()
        if  self._always \
            or (
                not self._only_startup
                and _time >= self._next_scheduled_run
            ):
            await self.callback(ctx)

            self._get_next_scheduled_run()

    async def _run_on_reboot(self, ctx=None):
        if ctx is None:
            ctx = self._ctx
        if self._reboot or self._always:
            await self.callback(ctx)
    
    def __str__(self):
        return self.callback.__name__

    def __repr__(self):
        return "{0} {1}".format(f"[{self.time_str}]:", self)
    
    @property
    def __name__(self):
        return str(self)
