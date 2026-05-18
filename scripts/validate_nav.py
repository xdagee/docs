import os
import yaml
import sys

def get_all_md_files(docs_dir):
    md_files = set()
    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith(".md"):
                # Get relative path from docs_dir, forcing forward slashes
                rel_path = os.path.relpath(os.path.join(root, file), docs_dir).replace("\\", "/")
                md_files.add(rel_path)
    return md_files

def get_nav_files(nav_config):
    nav_files = set()
    
    def extract_from_nav(nav_item):
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

def main():
    docs_dir = "docs"
    mkdocs_file = "mkdocs.yml"
    
    if not os.path.exists(mkdocs_file):
        print("Error: mkdocs.yml not found.")
        sys.exit(1)
        
    with open(mkdocs_file, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        
    if "nav" not in config:
        print("Error: 'nav' section not found in mkdocs.yml")
        sys.exit(1)
        
    physical_files = get_all_md_files(docs_dir)
    nav_files = get_nav_files(config["nav"])
    
    # Exclude known non-nav files if necessary (e.g. index.md is usually in nav, but maybe others aren't)
    # For now, we expect strict 1:1 mapping for perfection, except maybe CNAME or similar.
    # We can ignore CONTRIBUTING.md etc if they are properly in nav.
    
    missing_from_nav = physical_files - nav_files
    
    # Filter out known exceptions if any
    # missing_from_nav = {f for f in missing_from_nav if not f.startswith("assets/")}
    
    if missing_from_nav:
        print("Error: The following files are created but NOT listed in mkdocs.yml navigation:")
        for f in sorted(missing_from_nav):
            print(f"  - {f}")
        print("\nMaintainability Issue: Orphaned pages are hard for users to find.")
        sys.exit(1)
    
    print("Success: All documentation sections are properly linked in Navigation.")

if __name__ == "__main__":
    main()
