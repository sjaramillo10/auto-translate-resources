# Resources Translator

Script to translate Android project localizable resources files using google translate API.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Python 2.7+
Python 3.2+ (Recommended)


####Dependencies Installation (MacOS) 
Python 2.7 comes shipped with the OS. 

To install Python3 I recommend use Homebrew package manager

The script will explain what changes it will make and prompt you before the installation begins. 
```
$ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Edit your ~/.profile to include (if it is not already there)

```
export PATH=/usr/local/bin:/usr/local/sbin:$PATH
```

To install Python 3:
```
$ brew install python3
```

#####Working with Python 3
At this point, you have the system Python 2.7 available, potentially the Homebrew version of Python 2 installed, and the Homebrew version of Python 3 as well.

```
$ python
```
will launch the Python 2 interpreter.

```
$ python3
```
will launch the Python 3 interpreter

### Installing

To download, install and run the project follow the instructions:

```
git clone https://github.com/computationalcore/auto-translate-resources
cd auto-translate-resources
python3 setup.py install
```

Python the setup install will install all python dependences.
And repeat

```
$ python3 translate.py -h

positional arguments:
  path                  The base path
  string_list           String of the base string.xml to be translated. Comma
                        separated list eg,
                        app_name,dialog_positive,loading_msg

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose
  -i IGNORED_LANGUAGES_LIST, --ignored_languages_list IGNORED_LANGUAGES_LIST
                        String containing the language which files should be
                        ignored on at translation. Comma separated list. eg.
```

path - The absolute or relative dir of the resource folder of your android project
string_list - List of the string of comma separated resource names you want to automatically translate to other languages 
-i - a comma separated list of languages locales to be ignored. The locale use the same notation explainded here https://developer.android.com/guide/topics/resources/providing-resources.html


If is necessary to necessary to register at https://cloud.google.com/translate/ to get your API key.

To include your API key into the project just copy or rename the file project.settings.example to project.settings

```
$ cp project.settings.example project.settings
```

The open the project.settings with your favorite text editor and replace YOUR_GOOGLE_TRANSLATE_API_KEY_HERE with your Google Translate API 
```
#CREDENTIALS (Currently only Google Translate API is supported)

#Text-to-speech service credentials
[translate]
api_key = YOUR_GOOGLE_TRANSLATE_API_KEY_HERE
```

After it you can run 
```
$ python3 translate.py PATH_TO_RESOURCE STRING_LIST 
```
## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* This works only with Android string resource schemes
* Currently it doesn't support translate all the strings (it needs the list 
* Maybe I will extend functionality and support iOS localizable strings and other frameworks.
