import os
import argparse
import shutil

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process command line arguments.')
    parser.add_argument('-p', dest='path', type=dir_path)

    return parser.parse_args()


def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"{path} is not a valid path")

def remove_migration(dir):
    for root, dirs, files in os.walk(dir):
        for dir in dirs:
            if dir.startswith('migrations'):
                path = os.path.join(root, dir)
                for filename in os.listdir(path):
                    f = os.path.join(path, filename)
                    # checking if it is a file
                    if filename[0].isdigit() and os.path.isfile(f):
                        print('migration: ',f)
                        os.remove(f)
                    if filename.startswith('__pycache') and os.path.isdir(f):
                        shutil.rmtree(f)

def main():
    args = parse_arguments()
    path = args.path
    remove_migration(path)

if __name__ == "__main__":
    main()