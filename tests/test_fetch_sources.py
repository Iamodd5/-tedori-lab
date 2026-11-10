"""scripts/fetch_sources.py: the publisher's file is used when it still matches its fingerprint; otherwise the archived copy;
otherwise the build stops. Uses file:// URLs, so no network."""
import hashlib

import pytest

from scripts import fetch_sources as fs


def setup(tmp_path, publisher, archive):
    src = tmp_path / "sources"
    src.mkdir()
    good = b"the page as saved"
    (src / "SHA256SUMS").write_text(f"{hashlib.sha256(good).hexdigest()}  ward/page.html\n")
    (tmp_path / "pub.html").write_bytes(publisher)
    (tmp_path / "arc.html").write_bytes(archive)
    (src / "EXTERNAL.tsv").write_text(f"# path\tURL\tarchive\nward/page.html\t{(tmp_path / 'pub.html').as_uri()}\t{(tmp_path / 'arc.html').as_uri()}\n")
    return good


def test_publisher_file_used_while_it_matches(tmp_path):
    good = setup(tmp_path, b"the page as saved", b"something else")
    fs.fetch(tmp_path)
    assert (tmp_path / "sources" / "ward" / "page.html").read_bytes() == good


def test_archive_copy_used_when_the_publisher_changed_the_page(tmp_path):
    good = setup(tmp_path, b"next year's page", b"the page as saved")
    fs.fetch(tmp_path)
    assert (tmp_path / "sources" / "ward" / "page.html").read_bytes() == good


def test_page_without_a_fingerprint_is_taken_from_the_publisher(tmp_path):
    # Pages that embed a per-request token are not in SHA256SUMS (see SHA256SUMS.volatile).
    setup(tmp_path, b"page with this request's token", b"archived copy")
    (tmp_path / "sources" / "SHA256SUMS").write_text("")
    fs.fetch(tmp_path)
    assert (tmp_path / "sources" / "ward" / "page.html").read_bytes() == b"page with this request's token"


def test_build_stops_when_no_copy_matches(tmp_path):
    setup(tmp_path, b"next year's page", b"also different")
    with pytest.raises(SystemExit):
        fs.fetch(tmp_path)
    assert not (tmp_path / "sources" / "ward" / "page.html").exists()


def test_page_without_an_archive_copy_stops_the_build_naming_it(tmp_path):
    # Some city pages could not be saved at the Internet Archive, so their row has no third column.
    setup(tmp_path, b"next year's page", b"unused")
    tsv = tmp_path / "sources" / "EXTERNAL.tsv"
    tsv.write_text(f"ward/page.html\t{(tmp_path / 'pub.html').as_uri()}\n")
    with pytest.raises(SystemExit) as stop:
        fs.fetch(tmp_path)
    assert "ward/page.html" in str(stop.value.code) and "different from the saved fingerprint" in str(stop.value.code)
    assert not (tmp_path / "sources" / "ward" / "page.html").exists()
