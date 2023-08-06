#!/usr/bin/env python3
#
#  __init__.py
"""
Library for validating `yaml` files against schema and selectively dumping nodes from `yaml` (or `json`) documents in `yaml` or `json` format.
"""
#
#  Copyright (c) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#  Copyright (c) Jakob Stemberger <yaccob@gmx.net>
#  Apache 2.0 Licensed
#  See LICENSE for more information
#

__author__ = "Dominic Davis-Foster"
__copyright__ = "2020 Dominic Davis-Foster"

__license__ = "Apache2.0"
__version__ = "3.0.0"
__email__ = "dominic@davis-foster.co.uk"

# stdlib
import collections
import json
import pathlib
from typing import Callable, Dict, Iterable, Union

# 3rd party
import jsonschema  # type: ignore
import yaml
from jsonpath_ng import ext as jsonpath  # type: ignore
from typing_extensions import TypedDict
from yaml import constructor, resolver

__all__ = ["validate", "dump", "optiondefaults", "__version__"]

optiondefaults = {
		"yaml": "{explicit_start: True, explicit_end: True, allow_unicode: True}",
		"json": "{indent: 2, encoding: utf-8}",
		"python": "{}"
		}


def dict_constructor(loader, node) -> Dict:
	return dict(loader.construct_pairs(node))


def orderedDict_constructor(loader, node, deep=False):
	data = collections.OrderedDict()
	yield data

	if isinstance(node, yaml.MappingNode):
		loader.flatten_mapping(node)

	data.update(collections.OrderedDict(loader.construct_pairs(node, deep)))


class Encoder(TypedDict):
	dumper: Callable
	kwargs: str
	yaml_constructor: Callable


def validate(
		schemafile: Union[str, pathlib.Path],
		datafiles: Iterable[Union[str, pathlib.Path]],
		encoding: str = "utf-8",
		) -> None:
	"""
	Validate the given datafiles using a schema

	:param schemafile: The ``json`` or ``yaml`` formatted schema to validate with
	:param datafiles: An iterable of ``json`` or ``yaml`` files to validate
	:param encoding: Encoding to open the files with.
	:type encoding: str
	"""

	schemafile = pathlib.Path(schemafile)

	schema = yaml.load(schemafile.read_text(encoding=encoding), Loader=yaml.FullLoader)

	for filename in datafiles:
		for document in yaml.load_all(
				pathlib.Path(filename).read_text(encoding=encoding),
				Loader=yaml.FullLoader,
				):
			try:
				jsonschema.validate(document, schema, format_checker=jsonschema.FormatChecker())
			except jsonschema.exceptions.ValidationError as e:
				e.filename = str(filename)
				raise e


def dump(
		datafile: Union[str, pathlib.Path],
		path: str = '$',
		format: str = "yaml",
		yaml_options: str = optiondefaults["yaml"],
		json_options: str = optiondefaults["json"],
		encoding: str = "utf-8",
		) -> None:
	"""

	:param datafile:
	:type datafile:
	:param path:
	:type path:
	:param format:
	:type format:
	:param yaml_options:
	:type yaml_options:
	:param json_options:
	:type json_options:
	:param encoding: Encoding to open the files with.
	:type encoding: str
	"""

	encoders: Dict[str, Encoder] = {
			"yaml": {
					"dumper": yaml.dump,
					"kwargs": yaml_options,
					"yaml_constructor": orderedDict_constructor,
					},
			"json": {
					"dumper": json.dumps,
					"kwargs": json_options,
					"yaml_constructor": orderedDict_constructor,
					},
			"python": {
					"dumper": (lambda x, **kwargs: x),
					"kwargs": "{}",
					"yaml_constructor": dict_constructor,
					},
			}

	yaml.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, encoders[format]["yaml_constructor"])

	if format == "json":
		yaml.add_constructor("tag:yaml.org,2002:timestamp", yaml.constructor.SafeConstructor.construct_yaml_str)

	yaml.add_representer(collections.OrderedDict, lambda dumper, data: dumper.represent_dict(data.items()))

	documents = yaml.load_all(
			pathlib.Path(datafile).read_text(encoding=encoding),
			Loader=yaml.FullLoader,
			)

	formatoptions = dict(
			yaml.load(optiondefaults[format], Loader=yaml.FullLoader),
			**yaml.load(encoders[format]["kwargs"], Loader=yaml.FullLoader)
			)

	for document in documents:
		for match in jsonpath.parse(path).find(document):
			print(encoders[format]["dumper"](match.value, **formatoptions))
