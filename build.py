#!/usr/bin/env python3
"""
Static site generator for resurrexi.io
Clean academic research lab site with publications, technical work, and compute access
"""

from pathlib import Path
import shutil
import yaml
import markdown
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

# Paths
BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"
CONTENT_DIR = BASE_DIR / "content"
STATIC_DIR = BASE_DIR / "static"
PUBLIC_DIR = BASE_DIR / "public"

# Setup Jinja2
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

def parse_frontmatter(content):
    """Parse YAML frontmatter from markdown content"""
    if content.startswith('---'):
        try:
            _, frontmatter, body = content.split('---', 2)
            metadata = yaml.safe_load(frontmatter)
            return metadata, body.strip()
        except ValueError:
            return {}, content
    return {}, content

def build_publications():
    """Build publications page from markdown files"""
    pub_files = sorted((CONTENT_DIR / "publications").glob("*.md"), reverse=True)
    publications = []

    for pub_file in pub_files:
        content = pub_file.read_text()
        metadata, body = parse_frontmatter(content)
        html_content = markdown.markdown(body, extensions=['extra', 'codehilite'])

        publications.append({
            'title': metadata.get('title', pub_file.stem),
            'authors': metadata.get('authors', 'Murad Farzulla'),
            'date': metadata.get('date', ''),
            'venue': metadata.get('venue', ''),
            'doi': metadata.get('doi', ''),
            'ssrn': metadata.get('ssrn', ''),
            'pdf': metadata.get('pdf', ''),
            'github': metadata.get('github', ''),
            'abstract': metadata.get('abstract', ''),
            'body': html_content,
            'slug': pub_file.stem
        })

    template = env.get_template('publications.html')
    output = template.render(publications=publications, year=datetime.now().year)
    (PUBLIC_DIR / "publications.html").write_text(output)
    print(f"Built publications page with {len(publications)} papers")

def build_technical_work():
    """Build technical work page from markdown files"""
    work_files = sorted((CONTENT_DIR / "technical-work").glob("*.md"), reverse=True)
    projects = []

    for work_file in work_files:
        content = work_file.read_text()
        metadata, body = parse_frontmatter(content)
        html_content = markdown.markdown(body, extensions=['extra', 'codehilite', 'fenced_code'])

        projects.append({
            'title': metadata.get('title', work_file.stem),
            'category': metadata.get('category', 'Infrastructure'),
            'date': metadata.get('date', ''),
            'github': metadata.get('github', ''),
            'description': metadata.get('description', ''),
            'body': html_content,
            'slug': work_file.stem,
            'tags': metadata.get('tags', [])
        })

    template = env.get_template('technical-work.html')
    output = template.render(projects=projects, year=datetime.now().year)
    (PUBLIC_DIR / "work.html").write_text(output)
    print(f"Built technical work page with {len(projects)} projects")

def build_pages():
    """Build static pages (index, about, compute)"""
    pages = ['index.html', 'about.html', 'compute.html']

    for page in pages:
        template = env.get_template(page)
        output = template.render(year=datetime.now().year)
        (PUBLIC_DIR / page).write_text(output)
        print(f"Built {page}")

def copy_static():
    """Copy static assets"""
    if STATIC_DIR.exists():
        shutil.copytree(STATIC_DIR, PUBLIC_DIR / "static", dirs_exist_ok=True)
        print("Copied static assets")

def main():
    """Build the entire site"""
    print("Building resurrexi.io...")

    # Clean and recreate public directory
    if PUBLIC_DIR.exists():
        shutil.rmtree(PUBLIC_DIR)
    PUBLIC_DIR.mkdir()

    # Build all pages
    build_pages()
    build_publications()
    build_technical_work()
    copy_static()

    print("\n✓ Build complete!")
    print(f"Output: {PUBLIC_DIR}")

if __name__ == "__main__":
    main()
