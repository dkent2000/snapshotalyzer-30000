# snapshotalyzer-30000
A demo project to manage AWS EC2 instance snapshots

## About

This project is a demo, and uses boto3 to manage AWS EC2 instance snapshots.

## Configuring

shotty uses the configuration file created gby the AWS cli. e.g.

`'aws configure --profile shotty`

## Running

First, install pipenv.  Then:

`pipenv run "python shotty/shotty.py <command> <subcommand> <--project=PROJECT>"`

*command* is instances, volumes, or snapshots
*subcokmmand* - depends on command
*Project* is optional
