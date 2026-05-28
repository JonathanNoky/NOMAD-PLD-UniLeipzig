from nomad.config.models.plugins import ParserEntryPoint


class UniLeipzigPLDEntryPoint(ParserEntryPoint):
    def load(self):
        from nomad_pld_unileipzig.parsers.parser import UniLeipzigPLDParser

        return UniLeipzigPLDParser(**self.dict())


unileipzig_pld_parser = UniLeipzigPLDEntryPoint(
    name='JsonParser for Uni Leipzig ELN PLD files',
    description="""Parser for Uni Leipzig ELN PLD files.""",
    mainfile_name_re=r'.*ro-crate-metadata.json$',
)
