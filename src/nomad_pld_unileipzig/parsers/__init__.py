from nomad_json_parser.parsers import ROCrateParserEntryPoint


ro_crate_parser_pld = ROCrateParserEntryPoint(
    name='JsonParser for ROCrate files.',
    description="""Parser for ROCrate files.""",
    level=1,
    mainfile_name_re=r'.*ro-crate-metadata.json$',
    mainfile_contents_re=r'.*#category-PLD Process.*',
    json_matching_key="pld_leipzig_jsonld",
)
