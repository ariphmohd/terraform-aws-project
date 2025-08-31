
# create a program to find files name with their data size under a given directory and asking folder name as user input
import os
import sys
import time
import datetime
import shutil
import glob
import re
import math
def find_files_with_size(directory):
    try:
        files = os.listdir(directory)
        file_info = {}
        for file in files:
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                size = os.path.getsize(file_path)
                file_info[file] = size
        return file_info
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}
    
if __name__ == "__main__":
    directory = input("Enter the directory path: ")
    if os.path.isdir(directory):
        file_sizes = find_files_with_size(directory)
        if file_sizes:
            print("Files and their sizes in bytes:")
            for file, size in file_sizes.items():
                print(f"{file}: {size} bytes")
        else:
            print("No files found in the specified directory.")
    else:
        print("The specified path is not a valid directory.")

