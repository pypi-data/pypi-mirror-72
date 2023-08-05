from argparse import ArgumentParser

parser = ArgumentParser(description="Browse trending repos on GitHub by stars")
parser.add_argument(
    "-l", "--lang", type=str, help="Language filter eg:python", required=False
)
parser.add_argument(
    "-d",
    "--date",
    type=str,
    help="Specify repo creation date in ISO8601 format YYYY-MM-DD",
    required=False,
)
parser.add_argument(
    "-L",
    "--layout",
    type=str,
    choices=("list", "table"),
    default="list",
    help="The output format (list or table), default is list",
)
parser.add_argument(
    "-s",
    "--stars",
    type=str,
    required=False,
    help="Range of stars required, default is '>=50'",
)
parser.add_argument("--debug", action="store_true", help="Turn on debugging mode")
args = parser.parse_args()
