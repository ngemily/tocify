import csv
import subprocess
import sys

import click
from jinja2 import Template

filename = ""
offset = 0
toc_file = "main.toc"
annotated_pdf = "out.pdf"
original_pdf = "in.pdf"

with open("toc.j2") as fh:
    template = Template(fh.read())


def parse_row(row):
    """Parse row 
    [+]*<title>, <page_no>

    Returns tuple of
        depth: int
        title: str
        page_no: int
    """
    title, page_no = row[0], row[1]
    depth = len(title) - len(title.lstrip("+")) + 1
    page_no = int(page_no) + offset
    title = title.lstrip("+ ")

    return (depth, title, page_no)


@click.command()
@click.option("-o", "--offset", default=0, help="Page number offset.")
@click.argument("filename", type=click.Path(exists=True, readable=True))
def main(filename, offset):
    """Foobar program

    \b
    toc file format:
        [+]*<heading>, <page_no>

        where the number of '+' symbol preceding a heading denotes its depth in
        the table of contents.

    \b
    e.g.
        <heading>, <page_no>
        +<sub-heading>, <page_no>
        ++<sub-sub-heading>, <page_no>
        ++<sub-sub-heading>, <page_no>
        <heading>, <page_no>
        +<sub-heading>, <page_no>
    """
    pass


def foo():
    with open(toc_file, "w") as ofh:
        with open(filename, "r") as ifh:
            for row in csv.reader(ifh):
                depth, title, page_no = parse_row(row)
                ofh.write(
                    template.render(
                        title=title, bookmark_level=depth, page_number=page_no
                    )
                )

    try:
        # NB: pdftk does not permit overwriting original file
        subprocess.run(
            ["pdftk", original_pdf, "update_info", toc_file, "output", annotated_pdf],
            check=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as e:
        print(str(e.stderr, "utf-8"))


if __name__ == "__main__":
    main()
