"""Layout JSON App Config"""
# standard library
import json
import logging
import os
from collections import OrderedDict
from functools import lru_cache
from pathlib import Path
from typing import TYPE_CHECKING

from .models import LayoutJsonModel

if TYPE_CHECKING:  # pragma: no cover
    # first-party
    from tcex.app_config.models.install_json_model import OutputVariablesModel, ParamsModel


class LayoutJson:
    """Provide a model for the layout.json config file."""

    def __init__(self, filename=None, path=None, logger=None):
        """Initialize class properties."""
        filename = filename or 'layout.json'
        path = path or os.getcwd()
        self.log = logger or logging.getLogger('layout_json')

        # properties
        self.fqfn = Path(os.path.join(path, filename))

    @property
    @lru_cache()
    def contents(self) -> dict:
        """Return layout.json file contents."""
        contents = {}
        if self.fqfn.is_file():
            try:
                with self.fqfn.open() as fh:
                    contents = json.load(fh, object_pairs_hook=OrderedDict)
            except (OSError, ValueError):  # pragma: no cover
                self.log.error(
                    f'feature=layout-json, exception=failed-reading-file, filename={self.fqfn}'
                )
        else:  # pragma: no cover
            self.log.error(f'feature=layout-json, exception=file-not-found, filename={self.fqfn}')
        return contents

    def create(self, inputs: 'ParamsModel', outputs: 'OutputVariablesModel'):
        """Create new layout.json file based on inputs and outputs."""

        def input_data(sequence: int, title: str) -> dict:
            return {
                'parameters': [],
                'sequence': sequence,
                'title': title,
            }

        lj = LayoutJsonModel(
            **{
                'inputs': [
                    input_data(1, 'Action'),
                    input_data(2, 'Connection'),
                    input_data(3, 'Configure'),
                    input_data(4, 'Advanced'),
                ],
                'outputs': [{'display': '', 'name': o.name} for o in outputs],
            }
        )

        for input_ in inputs:
            if input_.name == 'tc_action':
                lj.inputs[0].parameters.append({'name': 'tc_action'})
            elif input_.hidden is True:
                lj.inputs[2].parameters.append(
                    {'display': "'hidden' != 'hidden'", 'hidden': 'true', 'name': input_.name}
                )
            else:
                lj.inputs[2].parameters.append({'display': '', 'name': input_.name})

        # write layout file to disk
        data = lj.json(
            by_alias=True, exclude_defaults=True, exclude_none=True, indent=2, sort_keys=True
        )
        self.write(data)

    @property
    # @lru_cache()
    def data(self) -> LayoutJsonModel:
        """Return the Install JSON model."""
        return LayoutJsonModel(**self.contents)

    @property
    def has_layout(self):
        """Return True if App has layout.json file."""
        return self.fqfn.is_file()

    @property
    def update(self):
        """Return InstallJsonUpdate instance."""
        return LayoutJsonUpdate(lj=self)

    def write(self, data: str) -> None:
        """Write updated file.

        Args:
            data: The JSON string to write data.
        """
        with self.fqfn.open(mode='w') as fh:
            fh.write(f'{data}\n')


class LayoutJsonUpdate:
    """Update layout.json file with current standards and schema."""

    def __init__(self, lj: LayoutJson) -> None:
        """Initialize class properties."""
        self.lj = lj

    def multiple(self) -> None:
        """Update the layouts.json file."""
        # APP-86 - sort output data by name
        self.update_sort_outputs()

        data = self.lj.data.json(
            by_alias=True, exclude_defaults=True, exclude_none=True, indent=2, sort_keys=True
        )
        self.lj.write(data)

    def update_sort_outputs(self) -> None:
        """Sort output field by name."""
        # APP-86 - sort output data by name
        self.lj.data.outputs = sorted(
            self.lj.data.dict().get('outputs', []), key=lambda i: i['name']
        )