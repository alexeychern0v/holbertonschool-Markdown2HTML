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
            heading_text = parse_inline_formatting(heading_text)
            return f"<h{level}>{heading_text}</h{level}>\n"

    return None

def is_unordered_list_item(line):
    """Check if a line is an unordered list item"""
    return line.startswith('- ')

def is_ordered_list_item(line):
    """Check if a line is an ordered list item"""
    return line.startswith('* ')

def parse_list_item(line):
    """
    Parse a Markdown list item and return the text without the dash"""
    return line[2:].strip()

def parse_inline_formatting(text):
    """Parse inline Markdown formatting (bold and emphasis) to HTML"""
    while '**' in text:
        start = text.find('**')
        if start != -1:
            end = text.find('**', start + 2)
            if end != -1:
                bold_text = text[start + 2:end]
                text = text[:start] + f'<b>{bold_text}</b>' + text[end + 2:]
            else:
                break
        else:
            break

    while '__' in text:
        start = text.find('__')
        if start != -1:
            end = text.find('__', start + 2)
            if end != -1:
                em_text = text[start + 2:end]
                text = text[:start] + f'<em>{em_text}</em>' + text[end + 2:]
            else:
                break
        else:
            break

    return text

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
        lines = md_file.readlines()
    
    with open(output_file, 'w', encoding='utf-8') as html_file:
        in_list = False
        list_type = None
        in_paragraph = False
        paragraph_lines = []
        i = 0
        while i < len(lines):
            line = lines[i].rstrip('\n')

            html_line = parse_heading(line)
            if html_line:
                if in_paragraph:
                    html_file.write("<p>\n")
                    html_file.write("<br/>\n".join(paragraph_lines))
                    html_file.write("\n</p>\n")
                    in_paragraph = False
                    paragraph_lines = []
                if in_list:
                    html_file.write("</ul>\n")
                    in_list = False
                    list_type = None
                html_file.write(html_line)
                i += 1
                continue

            if is_unordered_list_item(line):
                if in_paragraph:
                    html_file.write("<p>\n")
                    html_file.write("<br/>\n".join(paragraph_lines))
                    html_file.write("\n</p>\n")
                    in_paragraph = False
                    paragraph_lines = []
                
                if not in_list:
                    html_file.write("<ul>\n")
                    in_list = True
                    list_type = 'ul'
                
                elif list_type != 'ul':
                    html_file.write(f"</{list_type}>\n")
                    html_file.write("<ul>\n")
                    list_type = 'ul'

                item_text = parse_list_item(line)
                item_text = parse_inline_formatting(item_text)
                html_file.write(f"<li>{item_text}</li>\n")
                i += 1
                continue

            if is_ordered_list_item(line):
                if in_paragraph:
                    html_file.write("<p>\n")
                    html_file.write("<br/>\n".join(paragraph_lines))
                    html_file.write("\n</p>\n")
                    in_paragraph = False
                    paragraph_lines = []

                if not in_list:
                    html_file.write("<ol>\n")
                    in_list = True
                    list_type = 'ol'

                elif list_type != 'ol':
                    html_file.write(f"</{list_type}>\n")
                    html_file.write("<ol>\n")
                    list_type = 'ol'

                item_text = parse_list_item(line)
                item_text = parse_inline_formatting(item_text)
                html_file.write(f"<li>{item_text}</li>\n")
                i += 1
                continue

            if line.strip() == '':
                if in_paragraph:
                    html_file.write("<p>\n")
                    html_file.write("<br/>\n".join(paragraph_lines))
                    html_file.write("\n</p>\n")
                    in_paragraph = False
                    paragraph_lines = []
                if in_list:
                    html_file.write(f"</{list_type}>\n")
                    in_list = False
                    list_type = None
                i += 1
                continue

            if in_list:
                html_file.write(f"</{list_type}>\n")
                in_list = False
                list_type = None

            formatted_line = parse_inline_formatting(line)
            paragraph_lines.append(line)
            in_paragraph = True
            i += 1

        if in_paragraph:
            html_file.write("<p>\n")
            html_file.write("<br/>\n".join(paragraph_lines))
            html_file.write("\n</p>\n")

        if in_list:
            html_file.write(f"</{list_type}>\n")
    
    sys.exit(0)