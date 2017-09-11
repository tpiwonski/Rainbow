import click
import sys

from rainbow import Rainbow, Pattern


@click.command()
@click.option('--pattern', multiple=True, type=(str, str, str, str))
def run(pattern):
    patterns = []
    for r, p in enumerate(pattern):
        patterns.append(Pattern(pattern=p[0], fgcolor=p[1], style=p[3], bgcolor=p[2], rank=r))

    r = Rainbow(patterns)
    for line in sys.stdin:
        line = r.process_line(line)
        print(line, end='')


if __name__ == '__main__':
    run()
