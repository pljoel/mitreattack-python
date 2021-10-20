import argparse
import json
from tabulate import tabulate
from dateutil.parser import isoparse


class IndexToMarkdown:
    @staticmethod
    def index_to_markdown(indexobj):
        """
        convert the index object [indexobj] (dict) to a markdown string and return the markdown string
        """
        lines = ["<!-- begin index generated by mitreattack-python.navlayers.collections.col_to_md.py -->",
                 f"## {indexobj['name']}", f"\n{indexobj['description']}\n", f"### {indexobj['name']} Collections\n"]

        for collection in indexobj['collections']:
            lines.append(f"#### {collection['name']}")
            lines.append(f"\n{collection['description']}\n")
            format_versions = list(map(lambda v: [
                f"[{collection['name']} v{v['version']}]({v['url']})",
                isoparse(v['modified']).strftime("%d %B %Y")
            ], collection["versions"]))

            lines.append(tabulate(format_versions, headers=['version', 'released'], tablefmt="github"))
            lines.append("")

        lines.append("<!-- end index generated by  mitreattack-python.navlayers.collections.col_to_md.py -->")

        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Print a markdown string to std-out representing a collection index"
    )
    parser.add_argument("-i",
                        "--index",
                        type=str,
                        default="index.json",
                        help="the collection index file to convert to markdown"
                        )
    parser.add_argument("-o",
                        "--output",
                        type=str,
                        default="index.md",
                        help="markdown output file"
                        )
    args = parser.parse_args()
    with open(args.index, "r") as f:
        index = json.load(f)
        with open(args.output, "w") as f2:
            f2.write(IndexToMarkdown.index_to_markdown(index))


if __name__ == "__main__":
    main()
