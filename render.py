import re

extend_search = re.compile(r"{{(extends) (.*)}}")
if_search = re.compile("{{if (?P<condition>\w+)}}(?P<content>.*?){{(else|endif)}}", re.DOTALL)
replace_search = re.compile("{{ (?P<replace>) }}")
else_search = re.compile("{{else}}(?P<content>.*?)(?={{endif}})", re.DOTALL)
elseless_search = re.compile("{{if.*?endif}}", re.DOTALL)

def render(template, app):  
    if not template:
        return None

    text = ""
    filename = "templates/" + template
    with open(filename) as f:
        text = f.read()
        # First compile template into extended base template.
        is_child = re.search(extend_search, text.splitlines()[0])
        if is_child:
            base_filename = "templates/" + is_child.group(2)
            with open(base_filename) as base:
                text = extend_template(base.read(), text)
        # Run conditional checks
        has_conditions = re.search(if_search, text)
        if has_conditions:
            text = render_conditionals(text, app)
        # Replace any variables passed to the render function.
        for replace in app.context.replaces.keys():
            arg_search = re.compile("{{ " + replace + " }}")
            text = re.sub(arg_search, app.context.replaces[replace], text)
    return text

def extend_template(base, text):
    block_search = re.compile("{{(block) (\w+)}}")
    has_blocks = re.search(block_search, base)
    if not has_blocks:
        return base
    else:
        find_content = re.compile("({{block "+has_blocks.group(2)+"}})(.*?)({{endblock}})", re.DOTALL)
        
        content = re.search(find_content, text).group(2)
        base = re.sub("{{block "+has_blocks.group(2)+"}}", content, base)
        return extend_template(base, text)

def render_conditionals(text, app):
    if_block_search = re.compile("{{if.*?endif}}", re.DOTALL)
    if_matches = if_block_search.finditer(text)
    else_content_search = re.compile("{{else}}(?P<content>.*?){{endif}}", re.DOTALL)
    # We now have the text of the if blocks in the template.
    for if_match in if_matches:
        # The full text of the if block.
        if_block = if_match.group(0)
        # A search match splitting the block into condition and content.
        if_parse = if_search.search(if_block)
        # The string after the 'if'
        con_check = if_parse.group('condition')
        # The string between the {{if}} and the {{endif}} or {{else}}
        content = if_parse.group('content')

        # import pdb
        # pdb.set_trace()

        if con_check in app.context.cons.keys() and app.context.cons[con_check]:
            text = re.sub(if_block, content, text)
        elif '{{else}}' in if_block:
            else_content = else_content_search.search(if_block).group('content')
            text = re.sub(if_block, else_content, text)
        else:
            text = re.sub(if_block, "", text)
    return text