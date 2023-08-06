# coding: utf-8

import json

import click

from fdfs_client import client
from fdfs_client import jsonencoder


def print_result(ret):
    click.echo(json.dumps(ret, indent=2, ensure_ascii=False, cls=jsonencoder.MyJsonEncoder))


@click.group()
def main():
    """
    Usage

    * Upload once:

        fdfs upload <filepath>

    * Upload by chunks:

        fdfs create <file_ext_no_dot>
        fdfs append <remote_file_id> <filepath>

    * Delete:

        fdfs delete <remote_file_id>
    """
    pass


@main.command()
@click.option('--conf', default='~/.local/etc/fdfs/client.conf', help='the client.conf path')
@click.argument('filepath', type=click.Path(exists=True))
def upload(filepath, conf):
    click.echo(f'Uploading: {filepath}, using: {conf}')
    cli = client.Fdfs_client(client.get_tracker_conf(conf))
    ret = cli.upload_by_filename(filepath)
    print_result(ret)


@main.command()
@click.option('--conf', default='~/.local/etc/fdfs/client.conf')
@click.argument('remote_file_id')
def delete(remote_file_id, conf):
    click.echo(f'Deleting: {remote_file_id}, using: {conf}')
    cli = client.Fdfs_client(client.get_tracker_conf(conf))
    ret = cli.delete_file(remote_file_id)
    print_result(ret)


@main.command()
@click.option('--conf', default='~/.local/etc/fdfs/client.conf', help='the client.conf path')
@click.argument('ext_name')
def create(conf, ext_name):
    """Using this cmd to create a upload task for big files"""
    click.echo(f'Creating appender for big files uploading... ({conf})')
    cli = client.Fdfs_client(client.get_tracker_conf(conf))
    ret = cli.upload_appender_by_buffer(b'', ext_name)
    print_result(ret)


@main.command()
@click.option('--conf', default='~/.local/etc/fdfs/client.conf', help='the client.conf path')
@click.argument('remote_file_id')
@click.argument('filepath', type=click.Path(exists=True))
def append(conf, remote_file_id, filepath):
    """Append content to the appender remote file id"""
    click.echo(f'Append data to remote file id: {remote_file_id}, file: {filepath}, conf: {conf}')
    cli = client.Fdfs_client(client.get_tracker_conf(conf))
    ret = cli.append_by_filename(filepath, remote_file_id)
    print_result(ret)


if __name__ == '__main__':
    main()
