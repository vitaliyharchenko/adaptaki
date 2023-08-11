from bs4 import BeautifulSoup
import markdown


def beautify(question_text_new):   
    soup = BeautifulSoup(question_text_new, 'html.parser')

    for node in soup.find_all('span'):
        tex_string = node.string
        tex_string = tex_string.removeprefix("\(").removesuffix("\)")

        inline = True
        if not node.next_sibling and not node.previous_sibling:
            inline = False

        if inline:
            tex_string = f"${tex_string}$"
        else:
            tex_string = f"$${tex_string}$$"

        node.clear()

        extension_configs = {
            'mdx_math_svg': {
                'inline_class': 'math',
                'display_class': 'math'
            }
        }
        md = markdown.Markdown(extensions=['mdx_math_svg'], extension_configs=extension_configs)

        svg_text = md.convert(tex_string)

        if inline:
            svg_text = svg_text.removeprefix("<p>").removesuffix("</p>")

        node.append(BeautifulSoup(svg_text, 'html.parser'))

    new_html_text = str(soup)
    return new_html_text