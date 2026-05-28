from typing import (
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )

import json

from nomad.config import config
from nomad.datamodel import EntryArchive
from nomad.parsing.parser import MatchingParser
from nomad_json_parser.parsers.parser import MappedJsonParser

configuration = config.get_plugin_entry_point(
    'nomad_pld_unileipzig.parsers:unileipzig_pld_parser'
)


class UniLeipzigPLDParser(MatchingParser):
    def parse(self, mainfile: str, archive: EntryArchive, logger) -> None:  # noqa: PLR0912, PLR0915
        data_file_with_path = mainfile.rsplit('raw/', maxsplit=1)[-1]
        logger.info(data_file_with_path)

        with archive.m_context.raw_file(data_file_with_path, 'r') as file:
            data = json.load(file)

        newgraph = []
        for j in range(len(data['@graph'])):
            if 'value' in data['@graph'][j]:
                try:
                    data['@graph'][j]['value'] = json.loads(data['@graph'][j]['value'])
                except (json.JSONDecodeError, KeyError, TypeError):
                    pass
            if data['@graph'][j]['@type'] == 'File':
                data = json.loads(
                    json.dumps(data).replace(
                        data['@graph'][j]['@id'],
                        data['@graph'][j]['@id'].replace(
                            './',
                            './' + data_file_with_path.strip('ro-crate-metadata.json'),
                        ),
                    )
                )
        for j in range(len(data['@graph'])):
            d = data['@graph'][j]
            if 'hasPart' in d.keys():
                for f in range(len(d['hasPart'])):
                    for i in range(len(data['@graph'])):
                        if (
                            data['@graph'][len(data['@graph']) - 1 - i]['@id']
                            == d['hasPart'][f]['@id']
                        ):
                            data['@graph'][j]['hasPart'][f] = data['@graph'][
                                len(data['@graph']) - 1 - i
                            ]
            if 'variableMeasured' in d.keys():
                for f in range(len(d['variableMeasured'])):
                    for i in range(len(data['@graph'])):
                        if (
                            data['@graph'][len(data['@graph']) - 1 - i]['@id']
                            == d['variableMeasured'][f]['@id']
                        ):
                            data['@graph'][j]['variableMeasured'][f] = data['@graph'][
                                len(data['@graph']) - 1 - i
                            ]
            if 'mentions' in d.keys():
                for f in range(len(d['mentions'])):
                    for i in range(len(data['@graph'])):
                        if (
                            data['@graph'][len(data['@graph']) - 1 - i]['@id']
                            == d['mentions'][f]['@id']
                        ):
                            data['@graph'][j]['mentions'][f] = data['@graph'][
                                len(data['@graph']) - 1 - i
                            ]
            if d['@id'] == './':
                newgraph.append(data['@graph'][j])

        newdata = dict()
        newdata['graph'] = newgraph
        newdata['$mapped_json_class_key'] = 'pld_leipzig'

        filename = data_file_with_path.replace('ro-crate-metadata.json', 'data.json')

        with archive.m_context.raw_file(filename, 'w') as outfile:
            json.dump(newdata, outfile)

        toparse = MappedJsonParser(json_file=filename)
        toparse.parse(filename, archive, logger)
        # json_archive=create_archive(toparse, archive, filename.replace('.json', '.archive.json'))
