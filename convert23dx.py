import sys
import os
import argparse
import subprocess


def find_files(folder_path,file_type):
    file_paths = []
    for file in os.listdir(folder_path):
        if file.endswith(file_type):
            print(os.path.join(folder_path,file))
            file_paths.append(os.path.join(folder_path,file))
    return file_paths

def open_file(file_path,program_path):
    subprocess.Popen([program_path,file_path])

def main():
    parser = argparse.ArgumentParser(description='This program help Bedo at daily job')
    parser.add_argument('-p', '--path', help='Path to the folder where the files are')
    parser.add_argument('-t', '--type', help='File type to look for in the folder')
    parser.add_argument('-pr','--program',help='Program .exe path')
    args = parser.parse_args()
    print(args)
    file_paths = find_files(args.path,args.type)
    open_file(str(file_paths[1]),args.program)


if __name__=="__main__":
    main()