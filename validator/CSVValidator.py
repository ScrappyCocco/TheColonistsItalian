# ---------------------------------------------------------------------
# IMPORTS

import csv

from bs4 import BeautifulSoup


# ---------------------------------------------------------------------


class CSVValidator:
    # ---------------------------------------------------------------------

    # List of lines to ignore
    # For example [500, 1025] will make the check skip line 500 and line 1025
    lines_to_ignore = []

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

    @staticmethod
    def __row_grammar_validation(row: list) -> bool:
        elements_to_check = [",", ".", ":", "!"]
        # Get the original content and the translated content
        english_content = row[3]
        translated_content = row[4]
        for grammar_element in elements_to_check:
            # Get the number of occurrences in english phrase
            en_count = english_content.count(grammar_element)
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
            if len(self.lines_to_ignore) > 0:
                print("-----")
                print("WARNING")
                print("THIS CHECK IS IGNORING FEW LINES, MAKE SURE THIS IS INTENDED")
                print("-----")
            for row in csv_reader:
                if line_counter == 1:
                    if not self.__csv_columns_validation(row):
                        raise Exception("Column name not valid (LINE 1)! Found: " + str(len(row)) + " expected 6 or 7!")
                else:
                    if line_counter in self.lines_to_ignore:
                        print("---Skipped line " + str(line_counter) + " because in ignore list!")
                    else:
                        if not self.__row_param_validation(row):
                            raise Exception("Looks like there is an error on ENTRY " + str(line_counter) + "!" +
                                            "The parameters (ex: {0}) looks invalid, check the line:\n'" + str(
                                row[4]) + "'")
                        if not self.__row_grammar_validation(row):
                            raise Exception("Looks like there is an error on ENTRY " + str(line_counter) + "!" +
                                            "The grammar (ex: .(dot) or !(exclamation point)) looks invalid, "
                                            "check the line:\n'" + str(row[4]) + "'")
                        if not self.__row_tags_validation(row):
                            raise Exception("Looks like there is an error on ENTRY " + str(line_counter) + "!" +
                                            "The tags looks invalid, check the line:\n'" + str(row[4]) + "'")
                line_counter += 1
            print("For-loop Ended - No errors found...")
