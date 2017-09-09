import re


class Pattern(object):

    fcolors = dict(
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

    def __init__(self, pattern, fcolor, style, bgcolor):
        self.pattern = "({pattern})".format(pattern=pattern)
        self.fcolor = fcolor
        self.style = style
        self.bgcolor = bgcolor

    def match(self, text):
        return [Match(self, m.group(0), m.start(0), m.end(0)) for m in re.finditer(self.pattern, text, re.MULTILINE)]

    def color(self, value):
        color = "\033[{style};{fgcolor};{bgcolor}m".format(style=self.styles[self.style],
                                                           fgcolor=self.fcolors[self.fcolor],
                                                           bgcolor=self.bgcolors[self.bgcolor])
        return "{color}{value}\033[00m".format(color=color, value=value)


class Match(object):

    def __init__(self, pattern, value, start, end):
        self.pattern = pattern
        self.value = value
        self.start = start
        self.end = end

    def overlap(self, match):
        return (match.start < self.start < match.end) or (match.start < self.end < match.end)

    def length(self):
        return self.end - self.start

    def find(self, text, start):
        return text.index(self.value, start)

    def colored(self):
        return self.pattern.color(self.value)


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
            match1 = matches.pop()
            ok = True
            for match2 in matches:
                if match1.overlap(match2):
                    if match1.length() < match2.length():
                        ok = False
                        break

            if ok or not matches:
                result.append(match1)

        return sorted(result, key=lambda r: r.start)

    def replace_matches(self, matches, line):
        start = 0
        for match in matches:
            index = match.find(line, start)
            if index == -1:
                return line

            result = line[0:index] + match.colored()
            start = len(result)
            line = result + line[index + len(match.value):]

        return line
