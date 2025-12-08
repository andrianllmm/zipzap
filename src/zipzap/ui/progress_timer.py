import time
from contextlib import contextmanager

from rich.progress import Progress, SpinnerColumn, TextColumn


class Timer:
    task: str = ""
    duration: float = 0.0

    def __init__(self, task: str):
        self.task = task


@contextmanager
def timed_progress(task_name: str, task_description: str = ""):
    """
    Context manager for a timed task with a Rich spinner.

    Usage:
        with timed_progress("Encoding text...") as timer:
            # your code here
            result = some_function()
        print(timer.duration)  # elapsed time in seconds
    """

    timer = Timer(task_name)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task(task_description, total=None)
        start = time.perf_counter()
        yield timer  # give back timer object to store duration
        timer.duration = time.perf_counter() - start
        progress.update(task, description=f"{task_description} complete!")
