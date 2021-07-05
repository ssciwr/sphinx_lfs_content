import hashlib
import os
import requests
import shutil
import subprocess
import tarfile


GIT_LFS_FILE = "https://github.com/git-lfs/git-lfs/releases/download/v2.13.3/git-lfs-linux-amd64-v2.13.3.tar.gz"
GIT_LFS_CHECKSUM = "03197488f7be54cfc7b693f0ed6c75ac155f5aaa835508c64d68ec8f308b04c1"


def lfs_setup(_, config):
    # If we already have git-lfs, we do nothing
    if shutil.which("git-lfs"):
        return
    
    # Determine the git root directory
    gitroot = os.path.abspath(os.path.join(os.getcwd(), config.lfs_content_path_to_git_root))

    # Setup a modified environment that has the gitroot in PATH
    env = os.environ
    env["PATH"] = os.environ["PATH"] + os.path.pathsep + gitroot

    # Download the latest git-lfs tarball and check its checksum
    git_lfs_content = requests.get(GIT_LFS_FILE).content
    checksum = hashlib.sha256(git_lfs_content).hexdigest()
    if checksum != GIT_LFS_CHECKSUM:
        raise ValueError("CheckSum of git-lfs tarball was incorrect!")

    # Write it to file (can this be short cut and merged with unpacking?)
    with open("git-lfs.tar.gz", "wb") as tar:
        tar.write(git_lfs_content)

    # Unpack the tarball
    with tarfile.open("git-lfs.tar.gz", "r:gz") as tar:
        tar.extractall(path=gitroot)

    # Define a convenience function for the following sys calls
    def syscall(cmd):
        subprocess.check_call(cmd.split(), env=env, cwd=gitroot)

    syscall("git-lfs install")
    syscall("git-lfs fetch")
    syscall("git-lfs checkout")


def setup(app):
    app.add_config_value("lfs_content_path_to_git_root", ".", rebuild='')
    app.connect('config-inited', lfs_setup)

    return {
        "version": "0.1.0",
        "parallel_read_safe": True
    }
