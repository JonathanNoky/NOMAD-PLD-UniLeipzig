# Introduction

This is an example of a mapping for a PVD experiment. It contains the mapper file and a ro-crate file as exported from eLabFTW. Please note, that for the example to work, the .eln file was extracted (renamed to .zip and unzipped) into a folder. This is only because the example logic of NOMAD would not work otherwise, for real uploads the full .eln file can be used.

# Viewing uploaded data

Below, you find an overview of your uploaded data.
Click on the `> /` button to get a list of your data or select **FILES** from the top menu of this upload.

The `mapper_pvd.json` contains the mapping of the data in the .eln file to the NOMAD schema. It defines the classes used in the NOMAD schema and contains the rules how to map between the data JSON and the schema. The mapping rules follow the ones of the [NOMAD Transformer](https://nomad-lab.eu/prod/v1/docs/howto/programmatic/json_transformer.html).

The other files are created via the mapper as NOMAD schemas filled with the data from the .eln file.

You can create your own mapper and data files and try them out here or in separate uploads.

# Where to go from here?

If you're interested in using this plugin and NOMAD in general you'll find support for the mapper at the [documentation](https://fairmat-nfdi.github.io/nomad-json-parser/) and general support at [FAIRmat](https://www.fairmat-nfdi.eu/fairmat).

If you have any questions about this example you may contact [Jonathan Noky](https://www.fairmat-nfdi.eu/fairmat/about-fairmat/team-fairmat) from the FAIRmat consortium.