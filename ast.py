#!/usr/bin/env python3
# The MIT License (MIT)
#
# Copyright (c) 2021-2023 Yegor Bugayenko
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import javalang


def nofa(tlist) -> int:
    """Number of final attributes.
    :rtype: int
    """
    declaration = tlist[0][1].filter(javalang.tree.FieldDeclaration)
    fields = list(field for field in declaration)
    found = 0
    for path, node in fields:
        del path
        if 'final' in node.modifiers:
            found += 1
    return found

def nosfa(tlist) -> int:
    """Number of static final attributes.
    :rtype: int
    """
    declaration = tlist[0][1].filter(javalang.tree.FieldDeclaration)
    fields = list(field for field in declaration)
    found = 0
    for path, node in fields:
        del path
        if 'static' in node.modifiers and 'final' in node.modifiers:
            found += 1
    return found


class NotClassError(Exception):
    """If it's not a class"""


if __name__ == '__main__':
    JAVA = sys.argv[1]
    METRICS = sys.argv[2]
    with open(JAVA, encoding='utf-8', errors='ignore') as file:
        try:
            raw = javalang.parse.parse(file.read())
            tree = raw.filter(javalang.tree.ClassDeclaration)
            if not (tree_class := list((value for value in tree))):
                raise NotClassError('This is not a class')
            with open(METRICS, 'a', encoding='utf-8') as metric:
                metric.write(f'nofa {nofa(tree_class)} '
                             f'Number of Final Attributes\n')
                metric.write(f'nosfa {nosfa(tree_class)} '
                             f'Number of Static Final Attributes\n')
        except FileNotFoundError as exception:
            message = f"{type(exception).__name__} {str(exception)}: {JAVA}"
            sys.exit(message)
