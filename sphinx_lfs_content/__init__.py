import hashlib
import os
import requests
import shutil
import sphinx
import subprocess
import tarfile
import tempfile


GIT_LFS_FILE = "https://github.com/git-lfs/git-lfs/releases/download/v3.1.2/git-lfs-linux-amd64-v3.1.2.tar.gz"
GIT_LFS_CHECKSUM = "a10bb562658a65ad0e22f331bc43f2cb292a57d21c5b26f52794257e48fcbe10"


def lfs_setup(_, config):
    # If we already have git-lfs, we do not need to set it up
    if shutil.which("git-lfs") is None:
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
            subprocess.check_call("git-lfs install".split(), env=env)
            subprocess.check_call("git-lfs fetch".split(), env=env)
            subprocess.check_call("git-lfs checkout".split(), env=env)

    # Execute all of the given post commands
    for cmd in config.lfs_content_post_commands:
        subprocess.check_call(cmd, shell=True)


def setup(app):
    app.add_config_value("lfs_content_post_commands", [], rebuild="")
    app.connect("config-inited", lfs_setup)

    return {"version": "1.1.0", "parallel_read_safe": True}
