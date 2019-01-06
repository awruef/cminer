#!/usr/bin/env python2.7 
from git import Repo
import subprocess
import argparse 
import sys 
import os

def get_repo(name, url, tree, basedir):
    """
    Clone from url at tree into basedir/name_tree, return that path
    """
    # Make a Repo for a local repo, one that either already exists or 
    # one we need to clone.
    ep = os.path.abspath("{bd}/{nm}_{tr}".format(bd=basedir, nm=name, tr=tree))
    if os.path.exists(ep):
        r = Repo(ep)
    else:
        r = Repo.clone_from(url, ep)
    
    # Set the Repo to the commit specified by tree.
    r.head.reference = r.commit(tree)
    assert r.head.is_detached

    return r.working_dir

CMAKE_CMD = "cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON {}"

def build_cmake(srcdir):
    """
    Invoke cmake and make, with arguments to emit compile_commands.json.
    Returns path to compile_commands.json.
    """
    buildir = "{}/build.obj".format(srcdir)
    if not os.path.exists(buildir):
        os.mkdir(buildir)
 
    try:
        subprocess.check_call(CMAKE_CMD.format(srcdir), shell=True, cwd=buildir)
        subprocess.check_call("make", shell=True, cwd=buildir)
    except Exception:
        return ""

    return "{}/compile_commands.json".format(buildir)

def generate_commands(name, repo, tree, workdir):
    src_dir = get_repo(args.name, args.repo, args.tree, args.workdir)
    # Is there a CMakeFile.txt? 
    if os.path.exists("{}/CMakeLists.txt".format(src_dir)):
        commands_json = build_cmake(src_dir)
        return commands_json
    return ""

def main(args):
    commands_file = generate_commands(args.name, args.repo, args.tree, args.workdir)
    print commands_file
    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser("builder")
    parser.add_argument("workdir")
    parser.add_argument("repo")
    parser.add_argument("tree")
    parser.add_argument("name")
    args = parser.parse_args()
    sys.exit(main(args))
