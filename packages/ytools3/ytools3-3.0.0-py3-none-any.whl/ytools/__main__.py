#!/usr/bin/env python3

# stdlib
import argparse
import optparse
import pathlib
import sys

# 3rd party
import jsonschema  # type: ignore
import yaml
from yaml import scanner

# this package
from ytools import __version__, dump, optiondefaults, validate


def main(argv):
	parser = argparse.ArgumentParser(
			prog=argv[0],
			description="""\
Dumps data from json (or yaml) documents in yaml format.
Command line wrapper for jsonpath-ng.
Find more information at https://github.com/yaccob/ytools
""",
			formatter_class=argparse.ArgumentDefaultsHelpFormatter,
			)
	# usage='Usage: %prog [OPTION] -p JSONPATH_EXPRESSION FILE...',
	# version='%s %s' % ("%prog", __version__),

	parser.add_argument("datafile", type=pathlib.Path, nargs=1, metavar="FILE")
	parser.add_argument(
			"-p",
			"--json-path",
			dest="path",
			default='$',
			help="Syntax for jsonpath expression: https://pypi.python.org/pypi/jsonpath-ng/1.4.2"
			)
	parser.add_argument(
			"-f",
			"--output-format",
			metavar="OUTPUTFORMAT",
			dest="format",
			choices={"yaml", "json", "python"},
			default="yaml",
			help='Output format. Can be "yaml", "json" or "python". '  # [default: %default]
			)
	parser.add_argument(
			"-y",
			"--yaml-options",
			dest="yaml_options",
			default=optiondefaults["yaml"],
			help="kwargs for yaml.dump (pyYaml) as yaml.mapping (for experts). "  # [default: '%default']
			)
	parser.add_argument(
			"-j",
			"--json-options",
			dest="json_options",
			default=optiondefaults["json"],
			help="kwargs for json.dumps as yaml.mapping (for experts). "  # [default: '%default']
			)
	parser.add_argument(
			"-v", "--validate", metavar="SCHEMA", dest="schema", help="Validate documents against json-schema"
			)
	parser.add_argument(
			"--encoding",
			dest="encoding",
			default="utf-8",
			help="Set encoding of input documents (if different from utf-8)"
			)

	args = parser.parse_args(argv[1:])

	try:
		if args.schema:
			validate(args.schema, args.datafile, encoding=args.encoding)
		del (args.__dict__["schema"])
		dump(args.datafile, **args.__dict__)

	except jsonschema.exceptions.ValidationError as e:
		sys.stderr.write(f"{e.path}: {e.message}\n")
		sys.stderr.write(f"  document-path: {list(e.absolute_path)}\n")
		sys.stderr.write(f"  schema-path:   {list(e.absolute_schema_path)}\n")
		sys.exit(1)

	except yaml.scanner.ScannerError as e:
		sys.stderr.write(f"{e}\n")


if __name__ == "__main__":
	main(sys.argv)
