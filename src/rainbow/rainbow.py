import re


class Pattern(object):

    fgcolors = dict(
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
        noeffect=0,
        bold=1,
        underline=2,
        negative1=3,
        negative2=5
    )

    bgcolors = dict(
        black=40,
        red=41,
        green=42,
        yellow=43,
        blue=44,
        purple=45,
        cyan=46,
        white=47
    )

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
        color = "\033[{style};{fgcolor};{bgcolor}m".format(style=self.styles[self.style],
                                                           fgcolor=self.fgcolors[self.fgcolor],
                                                           bgcolor=self.bgcolors[self.bgcolor])
        return "{color}{text}\033[00m".format(color=color, text=text)


class Match(object):

    def __init__(self, pattern, value, start, end):
        self.pattern = pattern
        self.value = value
        self.start = start
        self.end = end

    def overlap(self, match):
        return (match.start <= self.start <= match.end) or (match.start <= self.end <= match.end) or\
               (self.start <= match.start <= self.end) or (self.start <= match.end <= self.end)

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
        for current in matches:
            overlapping = [m for m in matches
                           if m != current and m.overlap(current) and m.get_rank() > current.get_rank()]
            if not overlapping:
                result.append(current)

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
