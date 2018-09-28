# -*- coding: utf-8 -*-

"""Simple command-line tool to copy the default language file (strings.xml) to all the 
resource folders available (values-*)
"""

__author__ = 'severiano.jaramillo@gmail.com (Seven)'

from shutil import copyfile
from glob import glob
import argparse

def copy_files(base_path, ignored_language_list, verbose):
    """
    Copy the string.xml file in values folder to all the other resource folders
    :param base_path:
    :param string_dict:
    :return string_dict:
    """
    paths = glob(base_path + '/values-*/')
    base_file = base_path+'/values/strings.xml'
    count = 0

    # Each path is a different language file
    for path in paths:
        # print(path)
        # Get the language at folder name pattern
        language = path.strip('/').split('/')[-1].split('-', 1)[1]
        # Pass languages ignored and system folder
        if language in ignored_language_list:
            continue

        output_file = path+'strings.xml'
        
        if verbose:
            print("Copying to file: "+output_file)

        copyfile(base_file, output_file)

        count += 1
    
    if verbose:
        print("==============================================")
        print("Copied "+str(count)+" files.")


def main():
    parser = argparse.ArgumentParser(
        description="Copy the default strings.xml resource to all the other resource files, to prepare for the first complete translation.")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-i", "--ignored_languages_list", type=str,
                        help="String containing the languages which files should be ignored for the translation. Comma separated list. eg. ar,pt")
    parser.add_argument("path", type=str, help="The base values(-*) folders path")
    args = parser.parse_args()

    if args.verbose:
        print("Starting copy script")
    
    # System folders names that follows the pattern values-* and HAVE to be ignored
    ignored_language_list = ['w820dp', 'v21']
    if args.ignored_languages_list:
        ignored_language_list += args.ignored_languages_list.split(',')
        if args.verbose:
            print("Ignoring Languages: " + args.ignored_languages_list)

    copy_files(args.path, ignored_language_list, args.verbose)


if __name__ == '__main__':
    main()