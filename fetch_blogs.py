#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["beautifulsoup4", "feedparser", "opml"]
# ///

import os
import urllib.request
from datetime import datetime
from bs4 import BeautifulSoup
import feedparser
import opml

# Get current timestamp for "last updated"
last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Parse OPML and flatten nested structure
opml_doc = opml.parse("hn-popular-blogs-2025.opml")
blogs = []

# Handle nested outline structure
for outline in opml_doc:
    if hasattr(outline, "_outlines"):
        # This is a parent category with nested blogs
        for sub_outline in outline._outlines:
            if hasattr(sub_outline, "xmlUrl"):
                blogs.append(sub_outline)
    elif hasattr(outline, "xmlUrl"):
        # This is a blog directly
        blogs.append(outline)

html_template = """<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Blog Reader</title>
<style>
:root {
  --bg-color: #fafafa;
  --text-color: #1a1a1a;
  --header-bg: #ffffff;
  --sidebar-bg: #f5f5f5;
  --card-bg: #ffffff;
  --accent-color: #ff6600;
  --secondary-text: #666666;
  --border-color: #e0e0e0;
  --hover-bg: #e8e8e8;
}

[data-theme="dark"] {
  --bg-color: #1a1a1a;
  --text-color: #e4e4e4;
  --header-bg: #2d2d2d;
  --sidebar-bg: #252525;
  --card-bg: #2d2d2d;
  --accent-color: #ff6600;
  --secondary-text: #999999;
  --border-color: #404040;
  --hover-bg: #3d3d3d;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  background-color: var(--bg-color);
  color: var(--text-color);
  line-height: 1.6;
  transition: background-color 0.3s ease, color 0.3s ease;
}

header {
  background-color: var(--header-bg);
  border-bottom: 1px solid var(--border-color);
  padding: 1rem 2rem;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 60px;
}

h1 {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--accent-color);
}

.header-nav {
  display: flex;
  gap: 1.5rem;
  margin-left: auto;
  margin-right: 1rem;
}

.header-nav a {
  color: var(--text-color);
  text-decoration: none;
  font-size: 0.95rem;
  transition: color 0.2s ease;
}

.header-nav a:hover {
  color: var(--accent-color);
}

.last-updated {
  font-size: 0.85rem;
  color: var(--secondary-text);
  margin-left: auto;
  margin-right: 1rem;
}

.theme-toggle {
  background: none;
  border: 1px solid var(--border-color);
  color: var(--text-color);
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s ease;
}

.theme-toggle:hover {
  background-color: var(--hover-bg);
}

.container {
  display: flex;
  margin-top: 60px;
  min-height: calc(100vh - 60px);
}

.sidebar {
  width: 280px;
  background-color: var(--sidebar-bg);
  border-right: 1px solid var(--border-color);
  position: fixed;
  left: 0;
  top: 60px;
  bottom: 0;
  overflow-y: auto;
  padding: 1rem 0;
}

.sidebar-header {
  padding: 0 1rem 1rem;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--secondary-text);
  font-weight: 600;
}

.nav-links {
  list-style: none;
}

.nav-links li {
  margin: 0;
}

.nav-links a {
  display: block;
  padding: 0.5rem 1rem;
  text-decoration: none;
  color: var(--text-color);
  font-size: 0.9rem;
  transition: background-color 0.15s ease;
  border-left: 3px solid transparent;
}

.nav-links a:hover {
  background-color: var(--hover-bg);
  border-left-color: var(--accent-color);
}

main {
  margin-left: 280px;
  padding: 2rem;
  max-width: 900px;
  width: 100%;
}

.blog-section {
  margin-bottom: 3rem;
}

.blog-section h2 {
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--accent-color);
}

.blog-section h2 a {
  color: var(--text-color);
  text-decoration: none;
}

.blog-section h2 a:hover {
  color: var(--accent-color);
}

.post {
  background-color: var(--card-bg);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.post-header {
  margin-bottom: 1rem;
}

.post-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  line-height: 1.3;
}

.post-title a {
  color: var(--text-color);
  text-decoration: none;
}

.post-title a:hover {
  color: var(--accent-color);
}

.post-meta {
  font-size: 0.85rem;
  color: var(--secondary-text);
}

.post-content {
  font-size: 1rem;
  line-height: 1.7;
  color: var(--text-color);
}

.post-content p {
  margin-bottom: 1rem;
}

.post-content p:last-child {
  margin-bottom: 0;
}

.post-content a {
  color: var(--accent-color);
  text-decoration: underline;
}

.post-content img {
  max-width: 100%;
  height: auto;
  border-radius: 4px;
}

.post-content pre, .post-content code {
  background-color: var(--sidebar-bg);
  border-radius: 4px;
  font-family: "SF Mono", Monaco, "Cascadia Code", "Roboto Mono", Consolas, monospace;
  font-size: 0.9em;
}

.post-content code {
  padding: 0.2em 0.4em;
}

.post-content pre {
  padding: 1rem;
  overflow-x: auto;
  margin-bottom: 1rem;
}

.post-content pre code {
  padding: 0;
  background: none;
}

.post-content blockquote {
  border-left: 3px solid var(--accent-color);
  padding-left: 1rem;
  margin: 1rem 0;
  color: var(--secondary-text);
  font-style: italic;
}

.post-content h1, .post-content h2, .post-content h3, .post-content h4 {
  margin: 1.5rem 0 0.75rem;
  font-weight: 600;
}

.post-content ul, .post-content ol {
  margin: 1rem 0;
  padding-left: 1.5rem;
}

.post-content li {
  margin-bottom: 0.5rem;
}

.read-more {
  display: inline-block;
  margin-top: 1rem;
  color: var(--accent-color);
  text-decoration: none;
  font-weight: 500;
  font-size: 0.95rem;
}

.read-more:hover {
  text-decoration: underline;
}

@media (max-width: 1024px) {
  .sidebar {
    width: 240px;
  }
  
  main {
    margin-left: 240px;
  }
}

@media (max-width: 768px) {
  header {
    padding: 1rem;
  }
  
  .header-nav {
    gap: 1rem;
    font-size: 0.9rem;
  }
  
  .sidebar {
    width: 100%;
    position: relative;
    top: 0;
    border-right: none;
    border-bottom: 1px solid var(--border-color);
    max-height: 300px;
  }
  
  .container {
    flex-direction: column;
  }
  
  main {
    margin-left: 0;
    padding: 1rem;
  }
}
</style>
</head>
<body>
<header>
  <h1>Blog Reader</h1>
  <nav class="header-nav">
    <a href="index.html">Home</a>
    <a href="about.html">About</a>
  </nav>
  <button class="theme-toggle" onclick="toggleTheme()">Toggle Theme</button>
</header>
<div class="container">
  <aside class="sidebar">
    <div class="sidebar-header">Blogs</div>
    <ul class="nav-links"></ul>
  </aside>
  <main></main>
</div>
<script>
function toggleTheme() {
  const currentTheme = document.documentElement.getAttribute('data-theme');
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', newTheme);
  localStorage.setItem('theme', newTheme);
}

// Load saved theme
const savedTheme = localStorage.getItem('theme') || 'light';
document.documentElement.setAttribute('data-theme', savedTheme);
</script>
</body>
</html>"""

html = BeautifulSoup(html_template, "html.parser")

# Add last updated timestamp to header
header = html.find("header")
last_updated_div = html.new_tag("div", **{"class": "last-updated"})
last_updated_div.string = f"Last updated: {last_updated}"
# Insert after h1, before the theme toggle button
h1 = html.find("h1")
h1.insert_after(last_updated_div)

nav = html.find("ul", class_="nav-links")
main = html.find("main")

for blog in blogs:
    # Parse the blog RSS feed
    feed = feedparser.parse(blog.xmlUrl)

    # Create navigation link
    safe_id = blog.title.replace(" ", "-").replace("/", "-")
    li = html.new_tag("li")
    a = html.new_tag("a", href="#" + safe_id)
    a.string = blog.title
    li.append(a)
    nav.append(li)

    # Create blog section
    section = html.new_tag("section", id=safe_id, **{"class": "blog-section"})

    # Add blog title
    h2 = html.new_tag("h2")
    title_link = html.new_tag(
        "a", href=blog.htmlUrl if hasattr(blog, "htmlUrl") else "#"
    )
    title_link.string = blog.title
    h2.append(title_link)
    section.append(h2)

    # Add posts with content
    for entry in feed.entries[:3]:
        post_div = html.new_tag("article", **{"class": "post"})

        # Post header with title
        post_header = html.new_tag("div", **{"class": "post-header"})
        post_title = html.new_tag("h3", **{"class": "post-title"})

        # Get link and title
        link = getattr(entry, "link", None) or getattr(entry, "id", "#")
        title = getattr(entry, "title", None) or getattr(entry, "id", "Untitled")

        title_a = html.new_tag(
            "a", href=link, target="_blank", rel="noopener noreferrer"
        )
        title_a.string = title
        post_title.append(title_a)
        post_header.append(post_title)

        # Add date if available
        if hasattr(entry, "published") or hasattr(entry, "updated"):
            date_str = getattr(entry, "published", None) or getattr(
                entry, "updated", ""
            )
            if date_str:
                post_meta = html.new_tag("div", **{"class": "post-meta"})
                post_meta.string = date_str
                post_header.append(post_meta)

        post_div.append(post_header)

        # Add post content
        content_div = html.new_tag("div", **{"class": "post-content"})

        # Get content (prefer content, fallback to summary/description)
        content = getattr(entry, "content", None)
        if content and len(content) > 0:
            # content is a list of dicts with 'value' key
            content_html = content[0].get("value", "")
        else:
            content_html = getattr(entry, "summary", None) or getattr(
                entry, "description", ""
            )

        if content_html:
            # Parse the content and add it
            content_soup = BeautifulSoup(content_html, "html.parser")
            # Limit content length to avoid huge pages
            text_content = content_soup.get_text()
            if len(text_content) > 2000:
                # Find a good truncation point
                truncated = text_content[:2000]
                last_period = truncated.rfind(".")
                last_space = truncated.rfind(" ")
                if last_period > 1800:
                    truncated = truncated[: last_period + 1]
                elif last_space > 1800:
                    truncated = truncated[:last_space]
                truncated += "..."
                content_div.string = truncated
            else:
                content_div.append(content_soup)
        else:
            content_div.string = "No preview available."

        post_div.append(content_div)

        # Add read more link
        read_more = html.new_tag(
            "a",
            href=link,
            target="_blank",
            rel="noopener noreferrer",
            **{"class": "read-more"},
        )
        read_more.string = "Read more →"
        post_div.append(read_more)

        section.append(post_div)

    main.append(section)

# Write the html file
with open("index.html", "w") as file:
    file.write(str(html))
