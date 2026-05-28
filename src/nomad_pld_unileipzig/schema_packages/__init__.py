from nomad.config.models.plugins import SchemaPackageEntryPoint


class UniLeipzigPLDSchema(SchemaPackageEntryPoint):
    def load(self):
        from nomad_pld_unileipzig.schema_packages.pld import m_package

        return m_package


uni_leipzig_pld_schema = UniLeipzigPLDSchema(
    name='UniLeipzigPhysicalLaserDepositionSchema',
    description='New schema package entry point configuration.',
)
