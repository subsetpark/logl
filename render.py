import re

def render(template, app):  
    if not template:
        return None

    text = ""
    filename = "templates/" + template
    extend_search = re.compile(r"{{%(extends) (.*)%}}")
    if_search = re.compile("{{if (?P<condition>\w+)}}(?P<content>.*){{endif}}", re.DOTALL)
    replace_search = re.compile("{{ (?P<replace>) }}")
    with open(filename) as f:
        text = f.read()
        
        # First compile template into extended base template.
        is_child = re.search(extend_search, text.splitlines()[0])
        if is_child:
            base_filename = "templates/" + is_child.groups()[1]
            with open(base_filename) as base:
                text = extend_template(base.read(), text)

        has_conditions = re.search(if_search, text)
        if has_conditions:
            text = render_conditionals(if_search, text, app)

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
        find_content = re.compile("({{block "+has_blocks.groups()[1]+"}})(.*?)({{endblock}})", re.DOTALL)
        
        content = re.search(find_content, text).groups()[1]
        base = re.sub("{{block "+has_blocks.groups()[1]+"}}", content, base)
        return extend_template(base, text)

def render_conditionals(if_search, text, app):
    has_conditions = re.search(if_search, text)

    if not has_conditions:
        return text
    else:
        condition = has_conditions.group('condition')
        if condition in app.context.cons.keys() and app.context.cons[condition]:
            text = re.sub(if_search, '(P=content)', text)
            return render_conditionals(if_search, text, app)
        else:
            text = re.sub(if_search, "", text)
            return render_conditionals(if_search, text, app)