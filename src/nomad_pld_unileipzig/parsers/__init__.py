from nomad_json_parser.parsers import ROCrateParserEntryPoint


ro_crate_parser_pld = ROCrateParserEntryPoint(
    name='JsonParser for ROCrate files.',
    description="""Parser for ROCrate files.""",
    mainfile_name_re=r'.*ro-crate-metadata.json$',##default
    json_matching_re=r'.*#category-PLD Process.*',
    json_matching_key="pld_leipzig_jsonld",
)
