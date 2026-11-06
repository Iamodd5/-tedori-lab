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


def test_build_stops_when_no_copy_matches(tmp_path):
    setup(tmp_path, b"next year's page", b"also different")
    with pytest.raises(SystemExit):
        fs.fetch(tmp_path)
    assert not (tmp_path / "sources" / "ward" / "page.html").exists()
