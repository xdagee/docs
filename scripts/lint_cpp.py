import os
import re
import sys

def lint_cpp_block(code, filename, line_num):
    errors = []
    
    # Basic Check 1: Arduino Structure
    # Most mission code should have setup() and loop()
    # We skip this for partial snippets (often labeled just 'cpp' without context)
    # But for full missions, it's usually expected. 
    # Let's enforce it loosely: if it looks like a full program (has void setup), it must have void loop.
    
    has_setup = "void setup" in code
    has_loop = "void loop" in code
    
    if has_setup and not has_loop:
        errors.append(f"Found 'void setup()' but missing 'void loop()'")
        
    # Basic Check 2: Balanced Braces (Simple counter)
    # This is naive but catches copy-paste errors
    open_braces = code.count('{')
    close_braces = code.count('}')
    
    if open_braces != close_braces:
        errors.append(f"Unbalanced braces: {{={open_braces}, }}={close_braces}")
        
    # Basic Check 3: Check for "placeholder" comments left by accident
    if "TODO" in code or "FIXME" in code:
        errors.append("Found TODO/FIXME in code block")

    return errors

def scan_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Regex to find cpp code blocks
    # ```cpp or ```c++
    # Capture content
    pattern = re.compile(r'```(?:cpp|c\+\+)(.*?)```', re.DOTALL)
    
    matches = pattern.finditer(content)
    file_errors = []
    
    for match in matches:
        code_block = match.group(1)
        # Line number approximation (not perfect due to dotall)
        start_index = match.start()
        line_num = content[:start_index].count('\n') + 1
        
        block_errors = lint_cpp_block(code_block, filepath, line_num)
        for err in block_errors:
            file_errors.append(f"Line {line_num}: {err}")
            
    return file_errors

def main():
    docs_dir = "docs"
    all_errors = {}
    has_failure = False
    
    print("Linting C++ code blocks...")
    
    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                errors = scan_file(path)
                if errors:
                    all_errors[path] = errors
                    has_failure = True
                    
    if has_failure:
        print("\nFAILED: C++ Issues Found")
        for path, errs in all_errors.items():
            print(f"\nFile: {path}")
            for e in errs:
                print(f"  - {e}")
        sys.exit(1)
        
    print("Success: C++ code blocks look structurally sound.")

if __name__ == "__main__":
    main()
