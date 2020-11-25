import mistune, re
from mistune.directives import DirectiveToc
from mistune.plugins import plugin_strikethrough, plugin_footnotes, plugin_table, plugin_url

def markdown(text, with_toc=False):
    renderer = mistune.HTMLRenderer(escape=False)
    inline = mistune.InlineParser(renderer, hard_wrap=True)
    md = mistune.Markdown(
        renderer=renderer,
        inline=inline
    )
    md.use(plugin_strikethrough)
    md.use(plugin_footnotes)
    md.use(plugin_table)
    md.use(plugin_url)

    if with_toc:
        md.use(DirectiveToc())
        text = f".. toc::\n<section id=\"text\">\n\n{text}\n\n</section>"
    return md(text)