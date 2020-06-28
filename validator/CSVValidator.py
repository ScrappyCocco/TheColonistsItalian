# ---------------------------------------------------------------------
# IMPORTS

import csv
import sys

from bs4 import BeautifulSoup
from ValidatorFileManager import ValidatorFileManager


# ---------------------------------------------------------------------


class CSVValidator:
    # ---------------------------------------------------------------------

    # List of lines to ignore
    # For example [500, 1025] will make the check skip line 500 and line 1025
    # Remember that line 1 is the file header
    lines_to_ignore = []

    # Grammar elements to check in the row
    elements_to_check = [",", ".", ":", "!", " - ", "%", "[", "]"]
    # Elements which number can differ between the english version and the translated version
    # This is to allow translated phrases to have more grammar that might be necessary
    # Remember that this only apply when the english version has 0, otherwise the number must be the same
    allowed_elements_difference = [",", ":"]

    # ---------------------------------------------------------------------

    @staticmethod
    def __csv_columns_validation(first_row: list) -> bool:
        if len(first_row) > 7 or len(first_row) < 6:
            return False
        else:
            print("Column name confirmed valid:" + str(len(first_row)))
            return True

    @staticmethod
    def __row_param_validation(row: list) -> bool:
        # Get the original content
        english_content = row[3]
        # Check that there is at least one {
        open_brace_en = english_content.count("{")
        if open_brace_en == 0:
            return True
        # Check if the number of } is the same as {
        closed_brace_en = english_content.count("}")
        if open_brace_en != closed_brace_en:
            return False
        # Check if the number is equal to the translated content
        translated_content = row[4]
        if translated_content.count("{") != translated_content.count("}"):
            return False
        if translated_content.count("{") != open_brace_en:
            return False
        if "STEAM_APP_IMAGE" in translated_content:
            # Check that STEAM_APP_IMAGE is equal
            steam_app_image_en = english_content.count("STEAM_APP_IMAGE")
            if translated_content.count("STEAM_APP_IMAGE") != steam_app_image_en:
                return False
        else:
            # Check that the parameter number is correct
            for i in range(0, open_brace_en):
                parameter = "{" + str(i) + "}"
                if parameter not in translated_content:
                    return False
        # Everything is fine
        return True

    @staticmethod
    def __row_extract_tags(english_content: str) -> list:
        soup = BeautifulSoup(english_content, "html.parser")
        # I have to check manually if a tag is closed or not to add both
        return_list = []
        for tag in soup.find_all():
            # Add the normal tag
            return_list.append("<" + tag.name + ">")
            # Check if the tag is also closed
            closed_tag = "</" + tag.name + ">"
            if closed_tag in english_content:
                return_list.append(closed_tag)
        # Return the list of tags
        return return_list

    def __row_tags_validation(self, row: list) -> bool:
        # Get the original content and the translated content
        english_content = row[3]
        translated_content = row[4]
        # Count and list tags from english content
        tags = self.__row_extract_tags(english_content)
        if len(tags) > 0:
            # For every tag
            for tag in tags:
                # Check if the tag is present
                if tag in translated_content:
                    # Remove the found tag from the string because it's checked
                    translated_content = translated_content.replace(tag, "", 1)
                else:
                    # Tag not present return false
                    return False
        # Everything is fine
        return True

    def __row_grammar_validation(self, row: list) -> bool:
        # Get the original content and the translated content
        english_content = row[3]
        translated_content = row[4]
        for grammar_element in self.elements_to_check:
            # Get the number of occurrences in english phrase
            en_count = english_content.count(grammar_element)
            if en_count == 0 and grammar_element not in self.allowed_elements_difference:
                tr_count = translated_content.count(grammar_element)
                if en_count != tr_count:
                    return False
            else:
                # If the counter is not 0, check the translated content
                for i in range(0, en_count):
                    # For every element check that's in the translated content
                    if grammar_element in translated_content:
                        # If is present remove the occurrence
                        translated_content = translated_content.replace(grammar_element, "", 1)
                    else:
                        # If is not present return false
                        return False
        return True

    def process_file(self, filename: str):
        with open(filename, encoding="utf8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_counter = 1

            # Init file
            file_manager = ValidatorFileManager()
            file_manager.init_result_file(self.lines_to_ignore)

            if len(self.lines_to_ignore) > 0:
                print("-----")
                print("WARNING")
                print("THIS CHECK IS IGNORING FEW LINES, MAKE SURE THIS IS INTENDED")
                print("-----")
            errors_found = 0
            for row in csv_reader:
                if line_counter == 1:
                    if not self.__csv_columns_validation(row):
                        raise Exception("Column name not valid (LINE 1)! Found: " + str(len(row)) + " expected 6 or 7!")
                else:
                    if line_counter in self.lines_to_ignore:
                        file_manager.write_line_separator(str(line_counter))
                        file_manager.write_string_to_file("---Skipped line " + str(line_counter) +
                                                          " because in ignore list!\n\n")
                    else:
                        if not self.__row_param_validation(row):
                            errors_found += 1
                            file_manager.write_line_separator(str(line_counter))
                            file_manager.write_string_to_file(
                                "Error [Parameters]: " +
                                "The parameters (ex: {0}) looks invalid, " +
                                "check the line:\n'" + str(row[4]) + "'\n\n")
                        if not self.__row_grammar_validation(row):
                            errors_found += 1
                            file_manager.write_line_separator(str(line_counter))
                            file_manager.write_string_to_file(
                                "Error [Grammar]: " +
                                "The grammar (ex: .(dot) or !(exclamation point)) looks invalid, "
                                "check the line:\n'" + str(row[4]) + "'\n\n")
                        if not self.__row_tags_validation(row):
                            errors_found += 1
                            file_manager.write_line_separator(str(line_counter))
                            file_manager.write_string_to_file(
                                "Error [Tags]: " +
                                "The tags (ex. <cat>) looks invalid, check the line:\n'" + str(row[4]) + "'\n\n")
                line_counter += 1
            # For end
            print("Errors counter:" + str(errors_found))
            if errors_found > 0:
                print("For-loop Ended - ERRORS FOUND, see file:'" + file_manager.file_output_name + "' for more...")
                sys.exit("QUIT: The translation file contains errors!")
            else:
                file_manager.write_string_to_file("Check ended without errors, " +
                                                  "no other check needed until you edit the translation file")
                print("For-loop Ended - No errors found...")
