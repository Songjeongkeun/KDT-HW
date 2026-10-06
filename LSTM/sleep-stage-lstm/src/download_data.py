"""Download one Sleep-EDF Expanded hypnogram per subject.

Only the small expert-annotation files are downloaded. The multi-gigabyte PSG
signal files are intentionally excluded from this mini project.
"""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import Request, urlopen


BASE_URL = "https://physionet.org/files/sleep-edfx/1.0.0/sleep-cassette/"


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        href = dict(attrs).get("href")
        if href:
            self.links.append(href)


def list_hypnograms() -> list[str]:
    request = Request(BASE_URL, headers={"User-Agent": "sleep-stage-lstm-course-project/1.0"})
    with urlopen(request, timeout=30) as response:
        html = response.read().decode("utf-8")
    parser = LinkParser()
    parser.feed(html)
    return sorted(link for link in parser.links if link.endswith("-Hypnogram.edf"))


def first_night_per_subject(files: list[str], max_subjects: int) -> list[str]:
    selected: dict[str, str] = {}
    for filename in files:
        # SC4001 and SC4002 are two nights from subject SC400.
        subject_id = filename[:5]
        selected.setdefault(subject_id, filename)
    return list(selected.values())[:max_subjects]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("data/raw"))
    parser.add_argument("--max-subjects", type=int, default=40)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    files = first_night_per_subject(list_hypnograms(), args.max_subjects)

    for index, filename in enumerate(files, start=1):
        destination = args.output_dir / filename
        if destination.exists():
            print(f"[{index:02d}/{len(files):02d}] exists: {filename}")
            continue
        request = Request(
            urljoin(BASE_URL, filename),
            headers={"User-Agent": "sleep-stage-lstm-course-project/1.0"},
        )
        with urlopen(request, timeout=30) as response:
            destination.write_bytes(response.read())
        print(f"[{index:02d}/{len(files):02d}] downloaded: {filename}")

    print(f"Saved {len(files)} hypnograms to {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()

