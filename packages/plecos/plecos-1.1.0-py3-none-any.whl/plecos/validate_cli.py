"""Ocean Protocol wrapper around json schema"""

from pathlib import Path

import click


@click.command()
# @click.option('--source', default="source", help='The schema version filename, must exist in
# /schemas folder')
# @click.argument('schema', default="metadata_v190118.json")#, help='The schema version filename,
# must exist in /schemas folder')
@click.argument('schema_file', type=click.Path(exists=True))
# @click.argument('json_file', default="metadata_v190118.json")#, help='The schema version
# filename, must exist in /schemas folder')
@click.argument('json_file', type=click.Path(exists=True))
# @click.option('--file', default="metadata_v190118.json", help='The schema version filename,
# must exist in /schemas folder')

def validate(schema_file, json_file):
    """This script validates a json file according a schema file.
    Wraps the jsonschema project, see https://pypi.org/project/jsonschema/.

    Arguments:

        SCHEMA_FILE_NAME: the name of the schema file, found in ./schemas

        JSON_FILE: the relative (to current directory) path of the json file to validate against
    """

    click.echo("schema_file_name: {}".format(schema_file))
    click.echo("json_file {}".format(json_file))
    print(type(schema_file))
    json_file_path = Path.cwd() / json_file
    assert json_file_path.exists(), "Json file path {} does not exist".format(json_file_path)
    schema_file_path = Path.cwd() / schema_file
    assert schema_file_path.exists()

    # Load schema

    # Load file

    validator = Draft4Validator(valid_schema)


if __name__ == "__main__":
    validate()
