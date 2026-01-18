#!/usr/bin/env python3
"""
Convert DOC and DOCX files to Markdown while preserving original content.

Usage:
    python convert_to_markdown.py <input_file>
    python convert_to_markdown.py <input_file> <output_file>
    python convert_to_markdown.py --batch <directory>
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path
import argparse
from docx import Document
import html2text


def convert_doc_to_html(doc_path):
    """Convert DOC file to HTML using macOS textutil command."""
    html_path = tempfile.mktemp(suffix='.html')
    cmd = ['textutil', '-convert', 'html', doc_path, '-output', html_path]
    subprocess.run(cmd, check=True)
    return html_path


def convert_html_to_markdown(html_path):
    """Convert HTML file to Markdown."""
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Configure html2text to preserve as much formatting as possible
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.ignore_tables = False
    h.body_width = 0  # Don't wrap lines
    h.mark_code = True
    h.emphasis_mark = '*'
    h.strong_mark = '**'
    
    return h.handle(html_content)


def convert_docx_to_markdown(docx_path):
    """Convert DOCX file to Markdown."""
    doc = Document(docx_path)
    markdown_content = []
    
    for para in doc.paragraphs:
        text = para.text
        if not text.strip():
            markdown_content.append('')
            continue
        
        # Check if it's a heading
        is_heading = False
        for heading_level in range(1, 7):
            heading_style = f'Heading {heading_level}'
            if para.style.name == heading_style:
                markdown_content.append(f'{'#' * heading_level} {text}')
                is_heading = True
                break
        
        if not is_heading:
            # Check for bold and italic
            para_text = ''
            for run in para.runs:
                run_text = run.text
                if run.bold and run.italic:
                    run_text = f'***{run_text}***'
                elif run.bold:
                    run_text = f'**{run_text}**'
                elif run.italic:
                    run_text = f'*{run_text}*'
                para_text += run_text
            
            markdown_content.append(para_text)
    
    return '\n'.join(markdown_content)


def convert_file(input_path, output_path=None):
    """Convert a single DOC/DOCX file to Markdown."""
    input_path = Path(input_path)
    
    if not output_path:
        output_path = input_path.with_suffix('.md')
    else:
        output_path = Path(output_path)
    
    print(f"Converting {input_path.name} to {output_path.name}...")
    
    try:
        if input_path.suffix.lower() == '.doc':
            # Convert DOC to HTML first, then to Markdown
            html_path = convert_doc_to_html(str(input_path))
            markdown_content = convert_html_to_markdown(html_path)
            os.unlink(html_path)  # Clean up temp file
        elif input_path.suffix.lower() == '.docx':
            # Convert DOCX directly to Markdown
            markdown_content = convert_docx_to_markdown(str(input_path))
        else:
            raise ValueError(f"Unsupported file format: {input_path.suffix}")
        
        # Write the markdown content
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"✅ Conversion complete: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error converting {input_path.name}: {e}")
        return False


def batch_convert(directory):
    """Convert all DOC and DOCX files in a directory to Markdown."""
    dir_path = Path(directory)
    
    if not dir_path.exists() or not dir_path.is_dir():
        print(f"❌ Directory not found: {directory}")
        return
    
    # Get all DOC and DOCX files
    doc_files = list(dir_path.glob('*.doc')) + list(dir_path.glob('*.docx'))
    
    if not doc_files:
        print(f"❌ No DOC/DOCX files found in {directory}")
        return
    
    print(f"Found {len(doc_files)} files to convert...")
    
    success_count = 0
    for doc_file in doc_files:
        if convert_file(doc_file):
            success_count += 1
    
    print(f"\n📊 Batch conversion complete: {success_count}/{len(doc_files)} files converted successfully")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert DOC/DOCX files to Markdown")
    parser.add_argument("input", help="Input file or directory")
    parser.add_argument("output", nargs="?", help="Output file (optional)")
    parser.add_argument("--batch", action="store_true", help="Batch convert all files in directory")
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    
    if args.batch or (input_path.is_dir() and not args.output):
        # Batch conversion
        batch_convert(args.input)
    elif input_path.is_file():
        # Single file conversion
        convert_file(args.input, args.output)
    else:
        print(f"❌ Error: {args.input} is not a valid file or directory")
        sys.exit(1)
