import hashlib
import os
import requests
import shutil
import subprocess
import tarfile
import tempfile


GIT_LFS_FILE = "https://github.com/git-lfs/git-lfs/releases/download/v2.13.3/git-lfs-linux-amd64-v2.13.3.tar.gz"
GIT_LFS_CHECKSUM = "03197488f7be54cfc7b693f0ed6c75ac155f5aaa835508c64d68ec8f308b04c1"


def lfs_setup(_, config):
    # If we already have git-lfs, we do nothing
    if shutil.which("git-lfs"):
        return

    # Determine the git root directory
    gitroot = os.path.abspath(
        os.path.join(os.getcwd(), config.lfs_content_path_to_git_root)
    )

    # Download the latest git-lfs tarball and check its checksum
    git_lfs_content = requests.get(GIT_LFS_FILE).content
    checksum = hashlib.sha256(git_lfs_content).hexdigest()
    if checksum != GIT_LFS_CHECKSUM:
        raise ValueError("CheckSum of git-lfs tarball was incorrect!")

    # Create a temporary directory to install git-lfs into
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Write it to file (can this be short cut and merged with unpacking?)
        with open(os.path.join(tmp_dir, "git-lfs.tar.gz"), "wb") as tar:
            tar.write(git_lfs_content)

        # Unpack the tarball
        with tarfile.open(os.path.join(tmp_dir, "git-lfs.tar.gz"), "r:gz") as tar:
            tar.extractall(path=tmp_dir)

        # Setup a modified environment that has the temporary directory in PATH
        # This works around a bug in git-lfs where git-lfs is called recursively,
        # but the inner calls rely on git-lfs being in PATH.
        env = os.environ
        env["PATH"] = os.environ["PATH"] + os.path.pathsep + tmp_dir

        # Fetch the LFS content of the repository
        subprocess.check_call("git-lfs install".split(), env=env, cwd=gitroot)
        subprocess.check_call("git-lfs fetch".split(), env=env, cwd=gitroot)
        subprocess.check_call("git-lfs checkout".split(), env=env, cwd=gitroot)


def setup(app):
    app.add_config_value("lfs_content_path_to_git_root", ".", rebuild="")
    app.connect("config-inited", lfs_setup)

    return {"version": "0.1.0", "parallel_read_safe": True}
