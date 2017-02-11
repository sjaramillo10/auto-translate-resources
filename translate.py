# -*- coding: utf-8 -*-

"""Simple command-line example for Translate Android XML files.
Command-line application that translates some keys from base Android string.xml to others translations.
"""
from __future__ import print_function

__author__ = 'computationalcore@gmail.com (Vin)'

from xml.dom import minidom
from glob import glob
import argparse
import configparser
import html
from googleapiclient.discovery import build
from tempfile import mkstemp
from shutil import move
from os import remove, close
import time
import fileinput
start_time = time.time()


def translate(node):
    if len(node.childNodes) == 0:
        result = None
    else:
        result = node.firstChild.data
    return result


def get_string_dict(base_path, string_list):
    """
    Get the dictionary with the default key:value for each element of
    the string keys list passed.
    :param base_path:
    :param string_list:
    :return string_dict:
    """
    string_dict = {}
    baseDoc = minidom.parse(base_path + '/values/strings.xml')
    strings = baseDoc.getElementsByTagName("string")
    for string in strings:
        # Push into the dictionary the pair of key value for string key and key value
        if string.getAttribute("name") in string_list:
            string_dict[string.getAttribute("name")] = string.firstChild.nodeValue
    return string_dict


def translate_files(base_path, string_dict, ignored_language_list, verbose):
    """
    Translate all localization files available at base path, based on the values
    passed at string_dict dictionary.
    :param base_path:
    :param string_dict:
    :return string_dict:
    """
    paths = glob(base_path + '/values-*/')

    # Each path is a different language file
    for path in paths:
        # print(path)
        # Get the language at folder name pattern
        language = path.strip('/').split('/')[-1].split('-', 1)[1]
        # Pass languages ignored and system folder
        if language in ignored_language_list:
            continue
        # Android resources use a pattern with format xx-rCC where xx in the language
        # and CC is the country. But google translator API uses a format xx-cc
        language = encode_android_res_lang(language)
        print("Starting translation for " + language)
        translate_file(string_dict, path, language, verbose)
        print("--------------------------------------------")


def translate_file(string_dict, path, language, verbose):
    """
    Translate the file and save it with translated version
    :param string_dict:
    :param path:
    :param language:
    :param verbose:
    :return:
    """
    translated_dict = {}
    for key, value in string_dict.items():
        translated_value = translate(value, language)
        translated_dict[key] = translated_value
        if verbose:
            print(value + " => " + translated_value)
    if verbose:
        print("Translation Finished.")

    file_path = path + "strings.xml"
    update_file(file_path, translated_dict, verbose)


def translate(source, language):
    # Use Google Translator API to translate teh sentence <http://code.google.com/apis/console>
    config = configparser.ConfigParser()
    config.read('project.settings')
    api_key = config['translate']['api_key']
    service = (build('translate', 'v2', developerKey=api_key))
    request = service.translations().list(q=source, target=language)
    response = request.execute()
    # Escape some html entities that come with response AND Escape
    # Apostrophe (needed for Android Resource xml files)
    return html.unescape(response['translations'][0]['translatedText']).replace("'", "\\'")


def update_file(file_path, translated_dict, verbose):
    print("Updating file: " + file_path)
    baseDoc = minidom.parse(file_path)
    strings = baseDoc.getElementsByTagName("string")
    translated_list_key = list(translated_dict.keys())
    update_dict = {}
    for string in strings:
        # Push into the dictionary the pair of key value for string key and key value
        if string.getAttribute("name") in translated_list_key:
            update_key = string.getAttribute("name")
            # Remove items
            update_dict[update_key] = translated_dict[update_key]
            del translated_dict[update_key]

    # Select insert lines
    # List with the items to be inserted
    remaining_list = list(translated_dict.keys())
    insert_lines = ''
    for t_string in remaining_list:
        new_line = ' <string name="' + t_string + '">' + translated_dict[t_string] + '</string>\n'
        insert_lines += new_line

    # UPDATE AND INSERT LINES
    # List with items to be updated
    update_list = list(update_dict.keys())
    for line in fileinput.input([file_path], inplace=True):
        # Check if the tag  is commented
        if line.strip(' \t\n\r')[0:4] == '<!--':
            print(line)
            continue
        # Insert New Lines
        if insert_lines:
            # Insert as soon as the first resource tag appears
            if "<resources>" in line:
                start_tag_line = line.strip(' \t\n\r')
                new_lines = start_tag_line + "\n" + insert_lines
                print(line.replace(line, new_lines))
                #To stop running after first success
                insert_lines = None
                continue

        # Update Line
        updated = False
        for update in update_list:
            if update in line:
                new_line = ' <string name="' + update + '">' + update_dict[update] + '</string>\n'
                print(line.replace(line, new_line),'')
                # Remove updated list from the list since they are unique
                update_list.remove(update)
                updated = True
                break

        # Just copy the original line
        if not updated:
            print(line)

    print("File Updated.")


def replaceText(node, newText):
    if node.firstChild.nodeType != node.TEXT_NODE:
        raise Exception("node does not contain text")

    node.firstChild.replaceWholeText(newText)


def encode_android_res_lang(language):
    """
    Convert Android resource language identification pattern to Google API Pattern language identification pattern.

    Google Translator API
    https://cloud.google.com/translate/docs/languages
    The Translation API's recognition engine supports a wide variety of languages. These languages are specified within
    a recognition request using language code parameters as noted on this page. Most language code parameters conform to
     pure ISO-639-1 identifiers, except where noted.

    Android Resources
    https://developer.android.com/guide/topics/resources/providing-resources.html
    The android resouce language identification is defined by a two-letter ISO 639-1 language code, optionally followed
    by a two letter ISO 3166-1-alpha-2 region code (preceded by lowercase "r").
    The codes are not case-sensitive; the r prefix is used to distinguish the region portion. You cannot specify a region alone.
    :param dir:
    :return:
    """
    if '-r' in language:
        language = language.split('-r')
        return language[0] + "-" + language[1].lower()
    return language


def main():
    parser = argparse.ArgumentParser(
        description="Translate passed strings from files of a android project based on passed list of strings resouce names.")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-i", "--ignored_languages_list", type=str,
                        help="String containing the language which files should be ignored on at translation. Comma separated list. eg. ar,pt")
    parser.add_argument("path", type=str, help="The base path")
    parser.add_argument("string_list", type=str,
                        help="String of the base string.xml to be translated. Comma separated list eg, app_name,dialog_positive,loading_msg")
    args = parser.parse_args()

    list = args.string_list.split(',')

    if args.verbose:
        print("Starting translation script")
    # System folders names that follows the pattern values-* and HAVE to be ignored
    ignored_language_list = ['w820dp', 'v21']
    if args.ignored_languages_list:
        ignored_language_list += args.ignored_languages_list.split(',')
        if args.verbose:
            print("Ignoring Languages: " + args.ignored_languages_list)

    if args.verbose:
        print("Getting default values for " + ",".join(str(x) for x in list) + "...")
    # Get the values of the list to be translated
    string_dict = get_string_dict(args.path, list)
    if args.verbose:
        print("Done.")

    if args.verbose:
        print("Start Translation Files")
    # Start translating the strings on each file
    translate_files(args.path, string_dict, ignored_language_list, args.verbose)

    print("------------------------------------------------")
    print("--- Execution time %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
    main()
