import re

def render(template=None, **replaces):  
    if not template:
        return None

    text = ""
    filename = "templates/" + template
    extend_search = re.compile(r"{{%(extends) (.*)%}}")
    with open(filename) as f:
        text = f.read()
        
        is_child = re.search(extend_search, text.splitlines()[0])
        # import pdb
        # pdb.set_trace()
        if is_child:
            base_filename = "templates/" + is_child.groups()[1]
            with open(base_filename) as base:
                text = extend_template(base.read(), text)

        for replace in replaces.keys():
            arg_search = re.compile("{{" + replace + "}}")
            text = re.sub(arg_search, replaces[replace], text)
    return text

def extend_template(base, text):
    block_search = re.compile("{{(block) (\w+)}}")
    has_blocks = re.search(block_search, base)
    if not has_blocks:
        return base
    elif has_blocks:
        find_content = re.compile("{{block "+has_blocks.groups()[1]+"}}(.*){{endblock}}", re.DOTALL)
        
        content = find_content.search(text).groups()[0]
        base = re.sub("{{block "+has_blocks.groups()[1]+"}}", content, base)
        return extend_template(base, text)