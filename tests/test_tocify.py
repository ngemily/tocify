from tocify.main import parse_row

def test_parse_row():
    r = parse_row(["+Subheading", 2])
    assert r == {"title": "Subheading", "bookmark_level": 2, "page_number": 2}
    r = parse_row(["+Subheading", 2], 1)
    assert r == {"title": "Subheading", "bookmark_level": 2, "page_number": 3}
