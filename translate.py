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
import os

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
        #Push into the dictionary the pair of key value for string key and key value
        if string.getAttribute("name") in string_list:
            string_dict[string.getAttribute("name")] = string.firstChild.nodeValue
    return string_dict


def translate_files(base_path, string_dict, verbose):
    """
    Translate all localization files available at base path, based on the values
    passed at string_dict dictionary.
    :param base_path:
    :param string_dict:
    :return string_dict:
    """
    paths=glob(base_path + '/values-*/')

    for path in paths:
        #print(path)
        #Get the language at folder name pattern
        language = path.strip('/').split('/')[-1].split('-',1)[1]
        #Pass languages ignored and system folder
        if language in ignored_language_list:
            continue
        #Android resources use a pattern with format xx-rCC where xx in the language
        # and CC is the country. But google translator API uses a format xx-cc
        language = encode_android_res_lang(language)
        print( "Path => " + path + ", Language -> " + language )


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
    parser = argparse.ArgumentParser(description="Generate changes on the translated files of a android project based on passed key list from the nodes with to translate.")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-i", "--ignored_languages_list", type=str, help="String containing the language which files should be ignored on at translation")
    parser.add_argument("path", type=str, help="The base path")
    parser.add_argument("string_list", type=str, help="String containing the key string of the base string.xml needed to be translated. eg, app_name,dialog_positive,loading_msg,...")
    args = parser.parse_args()


    # Build a service object for interacting with the API. Visit
    # the Google APIs Console <http://code.google.com/apis/console>
    config = configparser.ConfigParser()
    config.read('project.settings')
    api_key= config['translate']['api_key']
    service = build('translate', 'v2', developerKey=api_key)



    list = args.string_list.split(',')

    #System folders names that follows the pattern values-* and HAVE to be ignored
    ignored_language_list = ['w820dp','v21']
    if args.ignored_languages_list:
        ignored_language_list += args.ignored_languages_list.split(',')

    string_dict = get_string_dict(args.path, args.string_list)



    translate_files(args.path, string_dict, ignored_language_list, args.verbose)







    for key, value in string_dict.items():
        print(key + " -> " + value)



if __name__ == '__main__':
    main()
