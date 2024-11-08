.. tocify documentation master file, created by
   sphinx-quickstart on Thu Nov  7 14:14:28 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

tocify
======

Add table of contents metadata to pdf files.

``tocify --toc-filename mytoc.toc -o annotated.pdf in.pdf``

.. image:: imgs/1.png
   :width: 48%

.. image:: imgs/2.png
   :width: 48%

toc files looks like::

    Chapter 1, 1
    +Subsection 1, 3
    ++Subsubsection 1, 5
    ...

You may specify a page number offset with ``--offset`` which will be added to
each page number given in the toc file.

.. toctree::
   :maxdepth: 2
   :caption: Contents:
