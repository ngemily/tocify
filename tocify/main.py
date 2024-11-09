import csv
import pathlib
import shutil
import subprocess
import tempfile

import click
from jinja2 import Template


def parse_row(row, offset=0):
    """Parse row
    [+]*<title>, <page_no>

    Returns dict of args for use with jinja template.
    """
    title, page_no = row[0], row[1]
    depth = len(title) - len(title.lstrip("+")) + 1
    page_no = int(page_no) + offset
    title = title.lstrip("+ ")

    return {"title": title, "bookmark_level": depth, "page_number": page_no}


@click.command()
@click.option("--offset", default=0, help="Page number offset.")
@click.option(
    "-o", "--output-filename", type=click.Path(writable=True), help="Output filename."
)
@click.option(
    "--toc-filename",
    type=click.Path(exists=True, readable=True),
    required=True,
    help="""
    table of contents metadata

    \b
    toc file format:
        [+]*<heading>, <page_no>

    where the number of '+' symbol preceding a heading denotes its depth in the
    table of contents.

    \b
    e.g.
        <heading>, <page_no>
        +<sub-heading>, <page_no>
        ++<sub-sub-heading>, <page_no>
        ++<sub-sub-heading>, <page_no>
        <heading>, <page_no>
        +<sub-heading>, <page_no>
        """,
)
@click.argument("filename", type=click.Path(exists=True, readable=True))
def main(filename, output_filename, toc_filename, offset):
    """tocify

    Update FILENAME with table of contents metadata given in TOC_FILENAME
    """

    if not shutil.which("pdftk"):
        print("`pdftk` not found.")
        print("Please install pdftk https://www.pdflabs.com/tools/pdftk-server/")
        raise SystemExit(127)

    with open(pathlib.Path(__file__).parent / ("toc.j2")) as fh:
        template = Template(fh.read())

    with tempfile.NamedTemporaryFile(delete_on_close=False, mode="w") as ofh:
        with open(toc_filename, "r") as ifh:
            ofh.writelines(
                map(
                    lambda row: template.render(parse_row(row, offset)),
                    csv.reader(ifh),
                )
            )
        ofh.close()

        try:
            subprocess.run(
                ["pdftk", filename, "update_info", ofh.name, "output", output_filename],
                check=True,
                capture_output=True,
            )
        except subprocess.CalledProcessError as e:
            print(str(e.stderr, "utf-8"))


if __name__ == "__main__":
    main()
