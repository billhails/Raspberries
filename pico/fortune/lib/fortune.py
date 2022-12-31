import os
import random


class fortune:
    def __init__(self, **kwargs):
        self.file = kwargs["file"]
        self.max_line_length = kwargs["max_line_length"]
        self.max_line_count = kwargs["max_line_count"]
        self.file_size = os.stat(self.file)[6]
        self.fo = open(self.file)

    def _get_random_fortune(self):
        position = random.randrange(self.file_size)
        self.fo.seek(position)
        foundStart = False
        result = []
        while not foundStart:
            line = self.fo.readline()
            if not line or line == "%\n" or line == "%%\n":
                foundStart = True
        if line:
            foundEnd = False
            while not foundEnd:
                line = self.fo.readline()
                if line:
                    line = line.strip().replace("\u2015", "-").replace("\u2014", "-")
                    if line.startswith("%"):
                        foundEnd = True
                    else:
                        result.append(line)
                else:
                    foundEnd = True
        return result

    def _fit_words(self, words):
        current_line = ""
        fitted_lines = []
        for word in words:
            if current_line:
                if len(current_line) + 1 + len(word) > self.max_line_length:
                    fitted_lines.append(current_line)
                    current_line = word
                else:
                    current_line = current_line + " " + word
            else:
                current_line = word
        if current_line:
            fitted_lines.append(current_line)
        return fitted_lines

    def _format_fortune(self, lines):
        if len(lines) == 0:
            return []
        author_words = []
        if lines[-1].startswith("-"):
            author_line = lines.pop()
            author_words = author_line[1:].split()
        body_words = []
        for line in lines:
            for body_word in line.split():
                body_words.append(body_word)
        return {
            "body": self._fit_words(body_words),
            "author": self._fit_words(author_words),
        }

    def get(self):
        while True:
            fortune = self._format_fortune(self._get_random_fortune())
            if (
                len(fortune)
                and len(fortune["body"]) + len(fortune["author"]) <= self.max_line_count
            ):
                return fortune
