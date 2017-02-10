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
import json
from googleapiclient.discovery import build


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

    #Each path is a different language file
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
        translated_value = translate(value,language)
        translated_dict[key] = translated_value
        if verbose:
            print( value + " => " + translated_value)
    if verbose:
        print( "Translation Finished.")

    file_path = path + "strings.xml"
    update_file(file_path, translated_dict)



def translate(source,language):
    # Use Google Translator API to translate teh sentence <http://code.google.com/apis/console>
    config = configparser.ConfigParser()
    config.read('project.settings')
    api_key = config['translate']['api_key']
    service = (build('translate', 'v2', developerKey=api_key))
    request = service.translations().list(q=source, target=language)
    response = request.execute()
    return response['translations'][0]['translatedText']


def update_file(file_path, translated_dict):
    print("Updating file: " + file_path )
    baseDoc = minidom.parse(file_path)
    strings = baseDoc.getElementsByTagName("string")
    translated_list_key = list(translated_dict.keys())
    for string in strings:
        # Push into the dictionary the pair of key value for string key and key value
        if string.getAttribute("name") in translated_list_key:
            string_dict[string.getAttribute("name")] = string.firstChild.nodeValue


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


if __name__ == '__main__':
    main()
