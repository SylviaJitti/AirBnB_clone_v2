#!/usr/bin/python3
"""
A script to add compressed file to server.
The script will uncompress the files andserve the servers the index.html files.
"""
import os.path
from fabric.api import run, put, env

env.hosts = ["34.201.164.207", "54.84.88.116"]
env.key_filename = os.path.expanduser('~/.ssh/school')
env.user = "ubuntu"


def do_deploy(archive_path):
    """Function that will run the script."""
    if not os.path.exists(archive_path):
        return False
    put(archive_path, "/tmp/")
    compressed_filepath = "versions/web_static_20230406235730.tgz"
    compressed_filename = compressed_filepath.split("/")[1]
    compressed_file_without_ext = compressed_filename.split(".")[0]
    folder_uncompressed_file = "/data/web_static/releases/{}".format(
        compressed_file_without_ext)
    run("sudo mkdir -p {}".format(folder_uncompressed_file))
    run("sudo tar -xzf /tmp/{} -C {}".format(
        compressed_filename, folder_uncompressed_file))
    run("sudo rm /tmp/{} ".format(compressed_filename))
    run("sudo mv {}/web_static/* {}".format(
        folder_uncompressed_file, folder_uncompressed_file))
    run("sudo rm -rf {}/web_static".format(folder_uncompressed_file))
    run("sudo rm -rf /data/web_static/current")
    run("sudo ln -s {} /data/web_static/current".format(
        folder_uncompressed_file))
    return True
