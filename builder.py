#!/usr/bin/env python2.7 
import argparse 
import sys 

def main(args):
    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser("builder")
    parser.add_argument("workdir")
    parser.add_argument("repo")
    parser.add_argument("tree")
    args = parser.parse_args()
    sys.exit(main(args))
