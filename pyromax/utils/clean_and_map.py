from pyromax.utils import DeepestTagScanner


def clean_and_map(raw_html, target_tags):
    scanner = DeepestTagScanner(target_tags)
    scanner.feed(raw_html)

    found_tags = sorted(scanner.results, key=lambda x: x['from'])

    clean_text = ""
    elements = []
    last_idx = 0

    for tag in found_tags:
        tag_open_start = raw_html.rfind('<', 0, tag['from'])

        clean_text += raw_html[last_idx:tag_open_start]

        new_from = len(clean_text)
        clean_text += tag['content']

        elements.append({
            'type': tag['tag'],
            'from': new_from,
            'length': tag['length'],
            'attributes': tag['attrs']
        })

        last_idx = raw_html.find('>', tag['from'] + tag['length']) + 1

    clean_text += raw_html[last_idx:]
    return clean_text, elements


if __name__ == '__main__':
    text_input = "Hello <STRONG>test of strong</STRONG> and <STRONG>second</STRONG>!"
    text, elements = clean_and_map(text_input, ['STRONG'])

    from pprint import pprint

    print('text:')
    pprint(text)
    print('elements:')
    pprint(elements)

