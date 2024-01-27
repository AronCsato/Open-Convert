import sys
import os
import argparse


def find_files(folder_path,file_type):
    for file in os.listdir(folder_path):
        if file.endswith(file_type):
            print(os.path.join(file))

def main():
    parser = argparse.ArgumentParser(description='This program help Bedo at daily job')
    parser.add_argument('-p', '--path', help='Path to the folder where the files are')
    parser.add_argument('-t', '--type', help='File type to look for in the folder')
    args = parser.parse_args()
    print(args)
    find_files(args.path,args.type)


if __name__=="__main__":
    main()