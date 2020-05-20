import re


def format_snippet_list(snippet_ids):
    out = 'Found snippets:\n\n'
    for obj in snippet_ids:
        _id = obj['_id']
        out += f'`id = {_id}`\n'
    out += '\nTo retrieve specific snippet, try `!snippet <id>`'
    return out


def format_snippet(snippet_obj):
    snippet = snippet_obj['code']
    snippet_id = str(snippet_obj['_id'])
    snippet = re.sub(r'```\w*', '', snippet)
    return f'Retrieved snippet with `id = {snippet_id}`\n\n```python\n{snippet}```'


def format_save(saved_id):
    out = f'Saved snippet with `id = {saved_id}`\n\n'
    out += 'To list saved snippets, try `!snippets`\n'
    out += 'To retrieve specific snippet, try `!snippet <id>`'
    return out
