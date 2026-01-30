#!/usr/bin/python3
"""Markdown to HTML converter script"""
import sys
import os

def parse_heading(line):
    """Parse a Markdown heading line and convert it to HTML"""
    if line.startswith('#'):
        level = 0
        for char in line:
            if char == '#':
                level += 1
            else:
                break

        if 1 <= level <= 6:
            heading_text = line[level:].strip()
            return f"<h{level}>{heading_text}</h{level}>\n"

    return None



if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html",
              file=sys.stderr)
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.exists(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

    with open(input_file, 'r', encoding='utf-8') as md_file:
        with open(output_file, 'w', encoding='utf-8') as html_file:
            for line in md_file:
                line = line.rstrip('\n')
                html_line = parse_heading(line)
                if html_line:
                    html_file.write(html_line)
    
    sys.exit(0)