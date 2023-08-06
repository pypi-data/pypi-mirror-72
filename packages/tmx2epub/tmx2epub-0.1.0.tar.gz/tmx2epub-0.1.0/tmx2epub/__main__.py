r""" convert tmx to epub.
"""

from pathlib import Path

import logzero
from logzero import logger

# from pyquery import PyQuery as pq
from absl import app, flags

# from tmx2epub.xml_iter import xml_iter
from tmx2epub.browse_filename import browse_filename
from tmx2epub.gen_epub import gen_epub

FLAGS = flags.FLAGS
flags.DEFINE_string(
    "filename",
    "",  # browse to file if empty
    "tmx filename (can be gzip or bz2)",
    short_name="f",
)
flags.DEFINE_string(
    "dest",
    "",  # filename dir if empty
    "destintioin folder to save the epub file, if left empty, set to the same folder where tmx file is located",
    short_name="d",
)
flags.DEFINE_integer(
    "start",
    1,
    "starting pair (default to 1 (the first pari))",
    short_name="s",  # pairs per chapter
)
flags.DEFINE_integer(
    "pairs", 1000, "number of pairs per chapter", short_name="p"  # pairs per chapter
)
flags.DEFINE_integer("chapters", 10, "number of chapters", short_name="c")
flags.DEFINE_boolean("debug", False, "print debug messages.")
flags.DEFINE_boolean("version", False, "print version and exit", short_name="V")


def proc_argv(argv):  # pylint: disable=too-many-branches
    """ proc_argv in absl.
    __main__ main """
    del argv

    version = "0.1.0"
    if FLAGS.version:
        print("tmx2epub %s 20200630, brought to you by mu@qq41947782" % version)
        raise SystemExit(0)

    if FLAGS.debug:
        logzero.loglevel(10)  # logging.DEBUG
    else:
        logzero.loglevel(20)  # logging.INFO

    if FLAGS.start < 1:
        FLAGS.start = 1
    FLAGS.start = FLAGS.start - 1  # change to zero-based

    if FLAGS.pairs < 1:
        FLAGS.pairs = 1000
    if FLAGS.chapters < 1:
        FLAGS.pairs = 10

    # args = dict((elm, getattr(FLAGS, elm)) for elm in FLAGS)
    logger.debug(
        "\n\t available args: %s", dict((elm, getattr(FLAGS, elm)) for elm in FLAGS)
    )

    # browse to the filename's folder if the file does not exists
    filename = FLAGS.filename
    if not Path(filename).exists():
        try:
            filename = browse_filename(Path(filename))
        except Exception as exc:
            logger.error(exc)
            filename = ""
        logger.debug(" file selected: %s", filename)

    # filename = getattr(FLAGS, "filename")
    # filename not specified
    if not filename:
        # print("\t **filename not give**n, set to", Path(FLAGS.filename).absolute().parent))
        try:
            filename = browse_filename(Path(filename))
        except Exception as exc:
            logger.error(exc)
            filename = ""
        logger.debug(" file selected: %s", filename)

    FLAGS.filename = filename
    stem = Path(filename).stem
    if not FLAGS.dest:
        destfile = Path(FLAGS.filename).absolute().parent / f"{stem}.epub"
    else:
        destfile = Path(FLAGS.filename).absolute().parent / FLAGS.dest
        logger.debug(" FLAGS.filename: %s, destfle: %s", FLAGS.filename, destfile)
    FLAGS.dest = destfile
    if Path(FLAGS.dest).suffix not in ["epub"]:
        stem = Path(FLAGS.dest).stem
        FLAGS.dest = Path(FLAGS.dest).parent / f"{stem}.epub"
    FLAGS.dest = str(FLAGS.dest)

    args = ["filename", "dest", "start", "pairs", "chapters", "debug"]

    debug = FLAGS.debug
    if debug:
        logger.debug("\n\t args: %s", [[elm, getattr(FLAGS, elm)] for elm in args])

    try:
        outfile = gen_epub(
            FLAGS.filename,
            outfile=FLAGS.dest,
            start=FLAGS.start,
            pairs=FLAGS.pairs,
            chapters=FLAGS.chapters,
            debug=FLAGS.debug,
        )
    except Exception as exc:
        logger.error("gen_epub exc: %s", exc)
        raise SystemExit(1)

    logger.info(" epub generated **%s**", outfile)


def main():
    """ main. """
    app.run(proc_argv)


if __name__ == "__main__":
    main()
