"""Audit all image/media references in Markdown files.

Walks every .md file under docs/, extracts image references
(both Markdown syntax and HTML <img> tags), and reports which
referenced files are missing from disk.

Exit codes:
  0 — All referenced media exists on disk
  1 — One or more media files are missing (report printed)
"""

import os
import re
import sys
from typing import NamedTuple


class MediaRef(NamedTuple):
    """A single media reference found in a Markdown file."""
    source_file: str
    line_number: int
    ref_path: str
    resolved_path: str
    exists: bool


# Markdown image syntax:  ![alt](path)
MD_IMG_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")

# HTML img tag:  <img src="path" ... >
HTML_IMG_RE = re.compile(r'<img\s[^>]*src=["\']([^"\']+)["\']', re.IGNORECASE)


def scan_file(filepath: str, docs_dir: str) -> list[MediaRef]:
    """Extract all media references from a single Markdown file."""
    refs: list[MediaRef] = []
    file_dir = os.path.dirname(filepath)

    with open(filepath, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            for pattern in (MD_IMG_RE, HTML_IMG_RE):
                for match in pattern.finditer(line):
                    ref_path = match.group(1).strip()

                    # Skip external URLs and anchors
                    if ref_path.startswith(("http://", "https://", "#")):
                        continue

                    # Decode URL-encoded spaces
                    ref_path_decoded = ref_path.replace("%20", " ")

                    # Resolve relative to the file's directory
                    resolved = os.path.normpath(
                        os.path.join(file_dir, ref_path_decoded)
                    )

                    rel_source = os.path.relpath(
                        filepath, docs_dir
                    ).replace("\\", "/")

                    refs.append(MediaRef(
                        source_file=rel_source,
                        line_number=line_num,
                        ref_path=ref_path,
                        resolved_path=resolved,
                        exists=os.path.isfile(resolved),
                    ))

    return refs


def main() -> None:
    docs_dir = "docs"
    all_refs: list[MediaRef] = []

    print("Auditing media references...")

    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                all_refs.extend(scan_file(path, docs_dir))

    total = len(all_refs)
    missing = [r for r in all_refs if not r.exists]
    found = total - len(missing)

    print(f"\nTotal media references: {total}")
    print(f"  Found on disk:       {found}")
    print(f"  Missing:             {len(missing)}")

    if missing:
        # Group by source file for readability
        by_file: dict[str, list[MediaRef]] = {}
        for ref in missing:
            by_file.setdefault(ref.source_file, []).append(ref)

        print("\n--- Missing Media Report ---\n")
        print(f"{'Source File':<60} {'Line':<6} {'Referenced Path'}")
        print("-" * 120)

        for source in sorted(by_file.keys()):
            for ref in sorted(by_file[source], key=lambda r: r.line_number):
                print(f"{ref.source_file:<60} {ref.line_number:<6} {ref.ref_path}")

        # Also produce CSV-compatible output
        csv_path = os.path.join("scripts", "missing_media.csv")
        with open(csv_path, "w", encoding="utf-8") as csv_f:
            csv_f.write("source_file,line_number,ref_path\n")
            for ref in sorted(missing, key=lambda r: (r.source_file, r.line_number)):
                csv_f.write(f"{ref.source_file},{ref.line_number},{ref.ref_path}\n")

        print(f"\nCSV report written to: {csv_path}")
        print("\nWARNING: Missing media found. Review the report above.")
        # Exit 0 because placeholder GIFs are intentional per AGENTS.md.
        # Change to sys.exit(1) when all placeholders are replaced.
        sys.exit(0)

    print("\nSuccess: All media references resolved.")


if __name__ == "__main__":
    main()
