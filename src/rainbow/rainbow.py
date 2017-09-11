import re


class Pattern(object):

    fgcolors = dict(
        default=39,
        black=30,
        red=31,
        green=32,
        yellow=33,
        blue=34,
        purple=35,
        cyan=36,
        white=37
    )

    styles = dict(
        default=0,
        bold=1,
        opaque=2,
        italic=3,
        underline=4,
        crossout=9
    )

    bgcolors = dict(
        default=49,
        grey=40,
        red=41,
        green=42,
        yellow=43,
        blue=44,
        purple=45,
        cyan=46,
        white=47
    )

    prefix = '\x1b['
    suffix = 'm'
    reset = "{prefix}00{suffix}".format(prefix=prefix, suffix=suffix)

    def __init__(self, pattern, fgcolor, style, bgcolor, rank):
        self.pattern = "({pattern})".format(pattern=pattern)
        self.fgcolor = fgcolor
        self.style = style
        self.bgcolor = bgcolor
        self.rank = rank

    def match(self, text):
        return [Match(self, m.group(0), m.start(0), m.end(0))
                for m in re.finditer(self.pattern, text, re.MULTILINE)]

    def get_coloured(self, text):
        color = "{prefix}{style};{fgcolor};{bgcolor}{suffix}".format(
            prefix=self.prefix,
            style=self.styles[self.style],
            fgcolor=self.fgcolors[self.fgcolor],
            bgcolor=self.bgcolors[self.bgcolor],
            suffix=self.suffix
        )

        return "{color}{text}{reset}".format(color=color, text=text, reset=self.reset)


class Match(object):

    def __init__(self, pattern, value, start, end):
        self.pattern = pattern
        self.value = value
        self.start = start
        self.end = end

    def overlap(self, match):
        return (match.start <= self.start < match.end) or (match.start < self.end <= match.end) or\
               (self.start <= match.start < self.end) or (self.start < match.end <= self.end)

    def length(self):
        return self.end - self.start

    def find_value(self, text, start):
        return text.find(self.value, start)

    def get_coloured_value(self):
        return self.pattern.get_coloured(self.value)

    def get_rank(self):
        return self.pattern.rank


class Rainbow(object):

    def __init__(self, patterns):
        self.patterns = patterns

    def process_line(self, line):
        matches = self.find_matches(line, self.patterns)
        matches = self.filter_matches(matches)
        line = self.replace_matches(matches, line)
        return line

    def find_matches(self, line, patterns):
        matches = []
        for pattern in patterns:
            matches.extend(pattern.match(line))

        return matches

    def filter_matches(self, matches):
        result = []

        while matches:
            m = matches.pop()
            ok = True
            for o in matches:
                if o != m and o.overlap(m):
                    matches.remove(o)
                    foos = self.foo(m, o)
                    matches.extend(foos)
                    ok = False
                    break

            if ok:
                result.append(m)

        return sorted(result, key=lambda r: r.start)

    def replace_matches(self, matches, line):
        start = 0
        for match in matches:
            index = match.find_value(line, start)
            if index == -1:
                return line

            result = line[0:index] + match.get_coloured_value()
            start = len(result)
            line = result + line[index + len(match.value):]

        return line

    def foo(self, match1, match2):
        """
        Waiting for a better name and to be refactored:)
        """
        result = []

        if match1.start <= match2.start:
            current = match1
            next = match2
        else:
            current = match2
            next = match1

        if next.get_rank() > current.get_rank():
            l = next.start - current.start
            v = current.value[:l]
            m = Match(current.pattern, v, current.start, next.start)
            result.append(m)

            current, next = next, Match(current.pattern, current.value[l:], next.start, current.end)

        if current.end >= next.end:
            result.append(current)
            return result

        result.append(current)

        l = next.end - current.end
        v = next.value[-l:]
        current = Match(next.pattern, v, current.end, next.end)
        result.append(current)

        return result
