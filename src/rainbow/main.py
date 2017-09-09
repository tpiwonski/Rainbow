import click


@click.command()
@click.option('--pattern', multiple=True, type=(str, str, str, str))
def run(pattern):
    import sys
    from rainbow import Rainbow, Pattern

    patterns = []
    for p in pattern:
        patterns.append(Pattern(pattern=p[0], fcolor=p[1], style=p[2], bgcolor=p[3]))

    r = Rainbow(patterns)
    for line in sys.stdin:
        line = r.process_line(line)
        print(line, end='')


if __name__ == '__main__':
    run()
