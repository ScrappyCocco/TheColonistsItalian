# ---------------------------------------------------------------------
# IMPORTS

import csv

from bs4 import BeautifulSoup


# ---------------------------------------------------------------------


class CSVValidator:

    # ---------------------------------------------------------------------

    # ---------------------------------------------------------------------

    def csv_columns_validation(self, first_row: list) -> bool:
        if len(first_row) != 7:
            return False
        else:
            print("Column name confirmed valid:" + str(len(first_row)))
            return True

    def row_param_validation(self, row: list) -> bool:
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

    def row_extract_tags(self, english_content: str) -> list:
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

    def row_tags_validation(self, row: list) -> bool:
        # Get the original content and the translated content
        english_content = row[3]
        translated_content = row[4]
        # Count and list tags from english content
        tags = self.row_extract_tags(english_content)
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

    def process_file(self, filename: str):
        with open(filename, encoding="utf8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_counter = 1
            for row in csv_reader:
                if line_counter == 0:
                    if not self.csv_columns_validation(row):
                        raise Exception("Column name not valid (LINE 1)! Found: " + str(len(row)) + " expected 7!")
                else:
                    if not self.row_param_validation(row):
                        raise Exception("Looks like there is an error on ENTRY " + str(line_counter) + "!" +
                                        "The parameters (ex: {0}) looks invalid, check the line:\n'" + str(
                            row[4]) + "'")
                    if not self.row_tags_validation(row):
                        raise Exception("Looks like there is an error on ENTRY " + str(line_counter) + "!" +
                                        "The tags looks invalid, check the line:\n'" + str(row[4]) + "'")
                line_counter += 1
            print("For-loop Ended - No errors found...")
