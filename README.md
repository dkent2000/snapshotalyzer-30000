# snapshotalyzer-30000
A demo project to manage AWS EC2 instance snapshots

## About

This project is a demo, and uses boto3 to manage AWS EC2 instance snapshots.

## Configuring

shotty uses the configuration file created gby the AWS cli. e.g.

`'aws configure --profile shotty`

## Running

First, install pipenv.  Then:

`pipenv run "python shotty/shotty.py <command> <--project=PROJECT>"`

*command* is list, start, or stop
*Project* is optional
