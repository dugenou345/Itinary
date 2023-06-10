from tqdm import tqdm
import functools
import time

def progress_bar(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with tqdm(total=1, desc=f"Running {func.__name__}") as pbar:
            # Perform the decorated function
            result = func(*args, **kwargs)

            # Update the progress bar
            pbar.update(1)

        return result

    return wrapper
