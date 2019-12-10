# The Colonist translation validator

## Description
This is a small validator i made to check that the translation has all the tags and parameters as the original english phrase.
I tested it and should work as expected, if you find a bug please [report it](https://github.com/ScrappyCocco/TheColonistsItalian/issues).

## How to use
You need Python 3.6/3.7 to use this validator.
Download the two .py files and launch the main with the command:
```
python main.py filename.csv
```
**Remember:** you need to use it on **your** csv file, **not the main one** with **all* the languages.
Simply go to **your** sheet and export it using File -> Download as -> Comma-separated values.

## Available variables to change:
* CSVValidator.py:
    * `lines_to_ignore` list of lines number to skip.
    For example writing `[500, 1025]` will make the check skip line 500 and line 1025 of the translation file.
    
* ValidatorFileManager.py:
    * `file_output_name` the string name of the output file to create. Remember this **must** have the extension (default is .txt);
    * `every_output_file_different` boolean (default = False). If true will generate a new filename with date and hour on every execution.

## Validator steps
Here's what the validator check:
1. The Validator will open the file, checking it has the .csv extension, and check that the number of the columns is 6 (or 7);
1. If the line is in the `lines_to_ignore[]` array the check will skip it;
1. Check that the **row parameters** are valid. For example, if in english there is a `{0}` that must be present also in the translated string; 
This check will count how many parameters in format `{n}` are present and will validate the translated string;
1. Check that the **row symbol-grammar** is correct. For example, if the english phrase ends with '!' or with '.', the translation string must contain the same symbols;
1. Check that the **row tags** are valid. For example, if the english string has `<cat>String</cat>` the translated string must have `<cat>` and `</cat>` too.

If none of these checks find an error, the file is valid.
Every execution generate an output file you can read.