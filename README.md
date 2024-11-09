# Tocify

Annotate pdfs with table of contents metadata.

`tocify --toc-filename mytoc.toc -o annotated.pdf in.pdf`

<p float="left">
    <img src="docs/source/imgs/1.png" alt="before" width="40%">
    <img src="docs/source/imgs/2.png" alt="after" width="40%">
</p>

toc files looks like:

    Chapter 1, 1
    Chapter 2, 2
    +Subsection 1, 3
    ++Subsubsection 1, 5
    ...

You may specify a page number offset with `--offset` which will be added to
each page number given in the toc file.
