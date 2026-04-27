import json
import requests
import markdown
from bs4 import BeautifulSoup, NavigableString

def html_to_telegraph_nodes(element):
    if isinstance(element, NavigableString):
        return str(element)

    if element.name is None:
        return None

    # Allowed tags in Telegraph
    allowed_tags = [
        'a', 'aside', 'b', 'blockquote', 'br', 'code', 'em',
        'figcaption', 'figure', 'h3', 'h4', 'hr', 'i', 'iframe',
        'img', 'li', 'ol', 'p', 'pre', 's', 'strong', 'u', 'ul', 'video'
    ]

    tag = element.name

    # Mapping unsupported tags
    if tag == 'h1' or tag == 'h2':
        tag = 'h3'
    elif tag == 'h5' or tag == 'h6':
        tag = 'h4'
    elif tag == 'del' or tag == 'strike':
        tag = 's'
    elif tag == 'ins':
        tag = 'u'
    elif tag == 'table':
        rows = []
        for tr in element.find_all('tr'):
            cells = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
            if cells:
                rows.append(cells)

        if not rows:
            return None

        # Determine column widths
        num_cols = max(len(row) for row in rows)
        col_widths = [0] * num_cols
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(cell))

        lines = []
        for i, row in enumerate(rows):
            # Pad row if it has fewer columns than others
            padded_row = row + [""] * (num_cols - len(row))
            line = " | ".join(padded_row[j].ljust(col_widths[j]) for j in range(num_cols))
            lines.append(line)

            # Add a separator after the first row if it's a header (thead or first tr)
            if i == 0 and (element.find('thead') or not element.find('thead')):
                sep = "-+-".join("-" * col_widths[j] for j in range(num_cols))
                lines.append(sep)

        table_text = "\n".join(lines)
        return {"tag": "pre", "children": [table_text]}
    elif tag == 'kbd' or tag == 'mark' or tag == 'samp':
        tag = 'code'
    elif tag == 'div' or tag == 'span' or tag == 'section' or tag == 'article' or tag == 'header' or tag == 'footer':
        # Container tags: just process children
        children = []
        for child in element.children:
            node = html_to_telegraph_nodes(child)
            if node:
                if isinstance(node, list):
                    children.extend(node)
                else:
                    children.append(node)
        return children
    elif tag not in allowed_tags:
        # Ignore unknown tags but keep children
        children = []
        for child in element.children:
            node = html_to_telegraph_nodes(child)
            if node:
                if isinstance(node, list):
                    children.extend(node)
                else:
                    children.append(node)
        return children

    node = {"tag": tag}

    attrs = {}
    if tag == 'a' and element.get('href'):
        attrs['href'] = element.get('href')
    if tag == 'img' and element.get('src'):
        attrs['src'] = element.get('src')
    if tag == 'iframe' and element.get('src'):
        attrs['src'] = element.get('src')
    if tag == 'video' and element.get('src'):
        attrs['src'] = element.get('src')

    if attrs:
        node['attrs'] = attrs

    children = []
    for child in element.children:
        child_node = html_to_telegraph_nodes(child)
        if child_node:
            if isinstance(child_node, list):
                children.extend(child_node)
            else:
                children.append(child_node)

    if children:
        node['children'] = children

    return node

def convert_md_to_telegraph(md_file):
    with open(md_file, 'r', encoding='utf-8') as f:
        text = f.read()

    # Extensions to handle tables, footnotes, etc.
    # Note: 'extra' includes tables, footnotes, attr_list, def_list, fenced_code, abbr.
    html = markdown.markdown(text, extensions=['extra', 'sane_lists', 'nl2br'])
    soup = BeautifulSoup(html, 'html.parser')

    nodes = []
    for child in soup.contents:
        node = html_to_telegraph_nodes(child)
        if node:
            if isinstance(node, list):
                nodes.extend(node)
            else:
                nodes.append(node)
    return nodes

def create_telegraph_page(title, content_nodes):
    # Create account
    res = requests.get('https://api.telegra.ph/createAccount', params={
        'short_name': 'Jules',
        'author_name': 'Jules AI'
    }).json()

    if not res.get('ok'):
        print("Error creating account:", res)
        return None

    access_token = res['result']['access_token']

    # Create page
    # The API might reject the request if content is too large or invalid.
    # We should clean up nodes that might be invalid (like empty strings or lists)

    clean_nodes = []
    for n in content_nodes:
        if n:
            clean_nodes.append(n)

    res = requests.post('https://api.telegra.ph/createPage', data={
        'access_token': access_token,
        'title': title,
        'content': json.dumps(clean_nodes),
        'return_content': 'true'
    }).json()

    if not res.get('ok'):
        print("Error creating page:", res)
        # Debugging: write nodes to a file to inspect
        with open('debug_nodes.json', 'w') as f:
            json.dump(clean_nodes, f, indent=2)
        return None

    return res['result']['url']

if __name__ == "__main__":
    nodes = convert_md_to_telegraph('markdown-showcase-2.md')
    url = create_telegraph_page('Showcase Completo de Markdown', nodes)
    if url:
        print(f"Telegraph URL: {url}")
