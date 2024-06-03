import sys
import time


def progressbar(it, prefix='', size=60, out=sys.stdout):
    count = len(it)
    start = time.time()
    for i, item in enumerate(it):
        x = int(size * (i + 1) / count)
        remaining = ((time.time() - start) / (i + 1)) * (count - (i + 1))
        mins, sec = divmod(remaining, 60)
        time_str = f"{int(mins):02}{sec:05.2f}"
        progress_bar_str = f"{prefix}[{'█' * x}{'.' * (size - x)}] {i + 1}/{count} Est Time {time_str}"
        print(progress_bar_str, end='\r', file=out)
        yield item

for i in progressbar(range(15), "Computing: ", 40):
    time.sleep(.1)  # any code you need
