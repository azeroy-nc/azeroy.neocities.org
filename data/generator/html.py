# coding: utf-8
from . import load_data_from_file
import markdown

# Boxes

def generate_box(item):
    """Generates a box for the item (song/video)."""
    html = f'\n<div class="itembox {item.item_type}">'

    html += '\n\t<a class="itembox-thumbnail"></a>'

    html += f'\n\t<h2 class="itembox-title"><a class="itembox-title-link" href="/{item.item_type}/{item.id}/">{item.title}</a></h2>'
    html += f'\n\t<p><span class="itembox-channel">{item.account_readable}</span> · <span class="itembox-length">{item.length}</span></p>'
    html += f'\n\t<p><span class="itembox-date">{item.release_date}</span></p>'

    html += '\n</div>'
    return html

def generate_boxlist(items):
    """Generates a boxlist for the given items."""
    html = ''

    for item in items:
        html += generate_box(item)

    return html

def boxlist_from_file(type, source):
    return generate_boxlist(load_data_from_file(type, source))

# Info page

def generate_infopage_content(item):
    """Generates the main content of the infopage."""
    html = f'<div class="infopage-content {item.item_type}">'
    html += f'\n\t<div class="infopage-thumbnail"></div>'
    html += f'\n\t<h1>{item.title}</h1>'

    values = ['title', 'type', 'account', 'series', 'status', 'length', 'release_date']

    html += f'\n\t<table class="infopage-table {item.item_type}">\n\t\t<thead>'
    for value in values:
        html += '\n\t\t\t<tr>'
        html += '\n\t\t\t\t<th>'
        html += f'\n\t\t\t\t\t{value.replace("_", " ").capitalize()}'
        html += '\n\t\t\t\t</th>'
        html += '\n\t\t\t\t<td>'
        html += f'\n\t\t\t\t\t{item.format(value)}'
        html += '\n\t\t\t\t</td>'
        html += '\n\t\t\t</tr>'
    html += '\n\t</table>'

    headered_values = ['links', 'notes', 'content_warnings', 'sources', 'original_description']
    for value in headered_values:
        html += f'\n\t<h2>{value.replace("_", " ").capitalize()}</h2>'
        html += f'\n\t<p>{transform(value, item.format(value))}</p>'

    html += '\n</div>'

    return html

def infopage_from_file(type, source, _id):
    data = load_data_from_file(type, source, str(_id))
    item = None
    for i in data:
        if str(i.id) == str(_id):
            item = i
            break
    if not item:
        print("NO ITEM!!!", data)
        return ''
    return generate_infopage_content(item)

# Transforms

def transform_html(value):
    return str(markdown.markdown(str(value)))

def transform_table(value):
    html = ''
    html += f'\n\t<table class="inline-table">\n\t\t<thead>'
    for key, val in value.items():
        if isinstance(val, dict):
            val_tf = transform_table(val)
        elif isinstance(val, list):
            val_tf = transform_list(val)
        else:
            val_tf = transform_html(val)
        html += '\n\t\t\t<tr>'
        html += '\n\t\t\t\t<th>'
        html += f'\n\t\t\t\t\t{key.replace("_", " ").capitalize()}'
        html += '\n\t\t\t\t</th>'
        html += '\n\t\t\t\t<td>'
        html += f'\n\t\t\t\t\t{val_tf}'
        html += '\n\t\t\t\t</td>'
        html += '\n\t\t\t</tr>'
    html += '\n\t</table>'

    return html

def transform_list(value):
    md = ''
    for item in value:
        md += f' * {item}\n'
    return transform_html(md)

def transform_links(links):
    html = '<ul>'
    for label, link in links.items():
        html += f'<li><a href="{link}" class="link">{label}</a></li>'
    html += '</ul>'

    return html

def transform(_type, value):
    if not value:
        return '<span class="dim">N/A</span>'
    if _type == 'links':
        return transform_links(value)
    if isinstance(value, dict):
        return transform_table(value)
    elif isinstance(value, list):
        return transform_list(value)
    return transform_html(value)
