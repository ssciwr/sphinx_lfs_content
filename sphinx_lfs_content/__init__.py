import os
import shutil
import subprocess


def lfs_setup(_, config):
    # If we already have git-lfs, we do nothing
    if shutil.which("git-lfs"):
        return
    
    # Determine the git root directory
    gitroot = os.path.abspath(os.path.join(os.getcwd(), config.lfs_content_path_to_git_root))

    # Setup a modified environment that has the gitroot in PATH
    env = os.environ
    env["PATH"] = os.environ["PATH"] + os.path.pathsep + gitroot

    # Define a convenience function for the following sys calls
    def syscall(cmd):
        subprocess.check_call(cmd.split(), env=env, cwd=gitroot)

    syscall("wget https://github.com/git-lfs/git-lfs/releases/download/v2.7.1/git-lfs-linux-amd64-v2.7.1.tar.gz")
    syscall("tar xvfz git-lfs-linux-amd64-v2.7.1.tar.gz")
    syscall("git-lfs install")
    syscall("git-lfs fetch")
    syscall("git-lfs checkout")


def setup(app):
    app.add_config_value("lfs_content_path_to_git_root", ".", rebuild='')
    app.connect('config-inited', lfs_setup)

    return {
        "version": "0.1",
        "parallel_read_safe": True
    }
