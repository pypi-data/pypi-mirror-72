from typing import Callable

from .task import Task



def task(time: str):
    """Decorator to create a :Task: from a :Callable:.  
    Takes in a time :str: in cron-syntax.  
    """
    def f(func: Callable):
        return Task(time, func)
    return f
