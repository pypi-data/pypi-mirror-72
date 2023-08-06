""" generate epub.
"""

from typing import Optional

from pathlib import Path
import math
import logzero
from logzero import logger
from tqdm import tqdm, trange

from pyquery import PyQuery as pq
from ebooklib import epub

from tmx2epub.xml_iter import xml_iter


# fmt: off
def gen_epub(  # pylint: disable=too-many-arguments, too-many-locals, too-many-statements, too-many-branches
        infile: str,
        outfile: Optional[str] = None,
        title: Optional[str] = None,
        start: int = 1,
        pairs: int = 1000,
        chapters: int = 10,
        debug: bool = False,
) -> Optional[str]:
    # fmt: on
    """ gen epub.
        infile: str = r"tests\2.tmx"
        outfile: Optional[str] = None
        title: Optional[str] = None
        start: int = 1
        pairs: int = 1000
        chapters: int = 10
        debug: bool = True
    """

    if debug:
        logzero.loglevel(10)
    else:
        logzero.loglevel(20)

    if not Path(infile).is_file():
        logger.error(" [%s] is not a file or does not exist, exiting...", infile)
        raise SystemExit(1)

    if outfile is None:
        _ = Path(infile).absolute().parent
        stem = Path(infile).absolute().stem
        outfile = str(_ / f"{stem}.epub")

    if title is None:
        title = Path(infile).name

    if start < 1:
        start = 1
    start = start - 1
    if pairs < 0:
        pairs = 1000
    if chapters < 0:
        chapters = 1000

    # xml
    try:
        next(xml_iter(infile))
    except Exception as exc:
        logger.error(" file [%s] maybe not a valid tmx file: %s", infile, exc)
        raise SystemExit(1)

    # ---
    xml_g = xml_iter(infile)

    # skip
    if start > 5000:
        for elm in tqdm(start):
            next(xml_g)
    else:
        for elm in range(start):
            next(xml_g)

    chp_cont = []
    ch_ = 0
    try:
        conn = "<br/>"
        conn = " "
        # for ch_ in trange(chapters):
        for ch_ in range(chapters):
            ct_ = []
            if pairs > 10000:
                for _ in trange(pairs):
                    el_ = next(xml_g)
                    # ct_.append('<br/>&nbsp;&nbsp;'.join([pq(elm).html() for elm in pq(el_)("tuv")]))
                    tuv = [pq(elm).html() for elm in pq(el_)("tuv")]
                    # indent the secon tuv by 10px
                    _ = tuv[0] + f"""<div style="margin-left: 20px">{tuv[1]}</div>"""
                    ct_.append(_)
            else:
                for _ in range(pairs):
                    el_ = next(xml_g)
                    # ct_.append('<br/>&nbsp;&nbsp;'.join([pq(elm).html() for elm in pq(el_)("tuv")]))
                    tuv = [pq(elm).html() for elm in pq(el_)("tuv")]
                    # indent the secon tuv by 10px
                    _ = tuv[0] + f"""<div style="margin-left: 20px">{tuv[1]}</div>"""
                    ct_.append(_)

            chp_cont.append(conn.join(ct_))
    except StopIteration:
        # normal, just collect chapter content
        chp_cont.append(conn.join(ct_))
    except Exception as exc:
        logger.error("collecting sent pairs exc: %s", exc)
    finally:
        final_ch = ch_ + 1

    if final_ch < chapters:
        logger.info(" Only able to collect **%s** chapters", final_ch)

    digits = math.ceil(math.log(chapters) / math.log(10)) + 1

    # refer to https://pypi.org/project/EbookLib/
    _ = """
    # create chapter
    c1 = epub.EpubHtml(title='Intro', file_name='chap_01.xhtml', lang='hr')
    c1.content=u'<h1>Intro heading</h1><p>Zaba je skocila u baru.</p>'

    # add chapter
    book.add_item(c1)

    # define Table Of Contents
    book.toc = (epub.Link('chap_01.xhtml', 'Introduction', 'intro'),
                 (epub.Section('Simple book'),
                 (c1, ))
                )
    # """

    # create chapters
    ch_epub = []
    for elm in range(1, final_ch + 1):
        _ = epub.EpubHtml(title=f"{elm}", file_name=f"chap_{elm:0{digits}d}.xhtml", lang="en")
        # celm = _,
        # globals()[f"c{elm}"] = _

        logger.debug("elm: %s", elm)

        _.content = chp_cont[elm - 1]
        ch_epub.append(_)

    book = epub.EpubBook()
    # set metadata
    book.set_identifier(f"{title}-20200630")
    book.set_title(title)
    book.set_language('en')
    book.add_author('tmx2epub by mu@qq41947782')

    # add chapters nad prepare toc
    # toc = []
    for elm in ch_epub:
        book.add_item(elm)
        # toc.append(elm)

    # define CSS style
    style = 'body { font-family: Times, Times New Roman, serif; }'

    nav_css = epub.EpubItem(
        uid="style_nav",
        file_name="style/nav.css",
        media_type="text/css",
        content=style,
    )

    # add CSS file
    book.add_item(nav_css)

    _ = """
    for elm in range(1, final_ch + 1):
        _ = epub.Link(f"chap_{elm:0{digits}d}.xhtml", f"{elm}", f"{elm}")
        toc.append(_)
        # sect = (epub.Section(f"sect-{elm}"), (chp_cont[elm - 1],))
        # toc.append(sect)
    book.toc = toc
    # """

    book.toc = ((epub.Section(title), ch_epub),)

    # basic spine
    # book.spine = [cover, nav]

    book.spine = ["nav"]
    # book.spine.extend(toc)
    book.spine.extend(ch_epub)

    # add default NCX and Nav file
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    epub.write_epub(outfile, book)

    return outfile
