"""

renamed from xml_iter_rev in es-stuff
Based on xmllarge.py

from pyquery import PyQuery as pq
res = xml_iter(filename)

[pq(elm).text() for elm in (pq(next(res)))('tuv')]

"""
from pathlib import Path
import io
import bz2
import gzip


def search_opentag(line, pos=0, tag="tu"):
    """search opening tag"""
    tag1 = f"<{tag} ".encode()
    tag2 = f"<{tag}>".encode()

    try:
        pos1 = line.index(tag1, pos)
    except ValueError:
        pos1 = -1

    try:
        pos2 = line.index(tag2, pos)
    except ValueError:
        pos2 = -1

    if pos1 > -1 and pos2 > -1:
        return min(pos1, pos2)

    return max(pos1, pos2)


def search_closetag(line, pos=0, tag="tu"):
    """search closing tag"""
    tag3 = f"</{tag}>".encode()

    try:
        pos3 = line.index(tag3, pos)
    except ValueError:
        pos3 = -1

    return pos3


def xml_iter(file, tag="tu"):
    """
    Process huge xml files
    <tag> </tag> need to be in separate lines
    # TODO: in the middle of lines

    :file: file path
    :tag: element to retrieve
    """
    if not Path(file).exists():
        raise SystemExit(f"File [{file}] does not exist.")

    open = io.open  # pylint: disable=redefined-builtin
    if Path(file).suffix == ".gz":
        open = gzip.open
    if Path(file).suffix == ".bz2":
        open = bz2.open

    inputbuffer = b""
    # search_opentag else search_closetag
    flag = True

    with open(file, "rb") as inputfile:
        for line in inputfile:
            # line = next(inputfile)
            pos = 0
            pos_o = 0
            pos_c = 0
            while not (pos_c == -1 or pos_o == -1):
                if flag:
                    pos_o = search_opentag(line, pos)
                    if pos_o > -1:
                        flag = False
                        pos = pos_o
                    else:
                        pos = 0
                else:
                    pos_c = search_closetag(line, pos)
                    if pos_c > -1:
                        flag = True
                        inputbuffer += line[pos: pos_c + len(tag) + 3]

                        yield inputbuffer
                        # print(inputbuffer)

                        inputbuffer = b""
                        pos = pos_c
                        flag = True
                    else:
                        inputbuffer += line[pos_o:]  # save foe the next line

                        # reset pos
                        pos = 0
