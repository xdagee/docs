import os
import sys

import yaml


# Files intentionally excluded from navigation.
# These are internal reference documents, non-content files,
# or files only reachable via inline links within other pages.
ALLOWLIST = {
    "LICENSE",
    "photoshoot_plan.md",
}


class _IgnoreUnknownTagsLoader(yaml.SafeLoader):
    """YAML loader that silently handles !!python/name tags.

    MkDocs uses !!python/name for pymdownx emoji configuration
    and superfences custom fences. SafeLoader rejects these tags,
    but we only need the nav structure — so we treat unknown tags
    as plain strings.
    """


_IgnoreUnknownTagsLoader.add_multi_constructor(
    "tag:yaml.org,2002:python/",
    lambda loader, suffix, node: str(node.value),
)


def get_all_md_files(docs_dir: str) -> set[str]:
    """Walk the docs directory and collect all .md file paths (relative)."""
    md_files = set()
    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith(".md"):
                rel_path = os.path.relpath(
                    os.path.join(root, file), docs_dir
                ).replace("\\", "/")
                md_files.add(rel_path)
    return md_files


def get_nav_files(nav_config: list) -> set[str]:
    """Recursively extract all file paths referenced in the nav config."""
    nav_files: set[str] = set()

    def extract_from_nav(nav_item: object) -> None:
        if isinstance(nav_item, str):
            nav_files.add(nav_item)
        elif isinstance(nav_item, dict):
            for key, value in nav_item.items():
                if isinstance(value, list):
                    for item in value:
                        extract_from_nav(item)
                elif isinstance(value, str):
                    nav_files.add(value)

    for item in nav_config:
        extract_from_nav(item)

    return nav_files


def main() -> None:
    docs_dir = "docs"
    mkdocs_file = "mkdocs.yml"

    if not os.path.exists(mkdocs_file):
        print("Error: mkdocs.yml not found.")
        sys.exit(1)

    with open(mkdocs_file, "r", encoding="utf-8") as f:
        config = yaml.load(f, Loader=_IgnoreUnknownTagsLoader)

    if "nav" not in config:
        print("Error: 'nav' section not found in mkdocs.yml")
        sys.exit(1)

    physical_files = get_all_md_files(docs_dir)
    nav_files = get_nav_files(config["nav"])

    missing_from_nav = physical_files - nav_files - ALLOWLIST

    if missing_from_nav:
        print(
            "Error: The following files are created but NOT listed "
            "in mkdocs.yml navigation:"
        )
        for f in sorted(missing_from_nav):
            print(f"  - {f}")
        print(
            "\nMaintainability Issue: Orphaned pages are hard for "
            "users to find."
        )
        sys.exit(1)

    print(
        f"Success: All documentation sections are properly linked "
        f"in Navigation. ({len(nav_files)} nav entries, "
        f"{len(ALLOWLIST)} allowlisted)"
    )


if __name__ == "__main__":
    main()
