import argparse
from unfurl import unfurl


def main():
    parser = argparse.ArgumentParser(
        description='unfurl takes a URL and expands ("unfurls") it into a directed graph, extracting every '
                    'bit of information from the URL and exposing the obscured.')
    parser.add_argument(
        'what_to_unfurl',
        help='what to unfurl. typically this is a URL, but it also supports integers (timestamps), '
             'encoded protobufs, and more.')
    parser.add_argument(
        '-d', '--detailed', help='show more detailed explanations.', action='store_true')
    parser.add_argument(
        '-f', '--filter',
        help='only output lines that match this filter.')
    parser.add_argument(
        '-v', '-V', '--version', action='version', version='unfurl v20200613')
    args = parser.parse_args()

    unfurl_instance = unfurl.Unfurl()
    unfurl_instance.add_to_queue(
        data_type='url', key=None,
        value=args.what_to_unfurl)
    unfurl_instance.parse_queue()

    print(unfurl_instance.generate_text_tree(
        detailed=args.detailed, output_filter=args.filter))


if __name__ == "__main__":
    main()
