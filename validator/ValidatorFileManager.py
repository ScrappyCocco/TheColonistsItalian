# ---------------------------------------------------------------------
# IMPORTS

import io
from datetime import datetime


# ---------------------------------------------------------------------


class ValidatorFileManager:
    # ---------------------------------------------------------------------

    # Standard file-name for the output result
    file_output_name = "result.txt"

    # If every execution should generate a new different file
    every_output_file_different = False

    # Variable to check what lines headers have been already been written
    # This should NOT be touched by the user
    lines_headers: set = set()

    # ---------------------------------------------------------------------

    def init_result_file(self, lines_to_ignore: list):
        self.lines_headers = set()

        time_format_string = "%d.%m.%Y-%H.%M.%S"
        dt_string = datetime.now().strftime(time_format_string)

        if self.every_output_file_different:
            extension = self.file_output_name[-4:]
            self.file_output_name = self.file_output_name[:-3] + dt_string + extension

        with io.open(self.file_output_name, 'w', encoding='utf8') as output_file:
            output_file.write("The Colonist Validator - Execution: " + dt_string)
            output_file.write(" - (Time format: " + time_format_string.replace("%", "") + ")\n")
            output_file.write("Lines to ignore: " + str(lines_to_ignore) + "\n")
            output_file.write("REMEMBER that you need to execute this check UNTIL there are no more errors. \n"
                              "Not all errors can be found with a single execution.")
            output_file.write("\n\n")

    def write_string_to_file(self, text: str):
        with io.open(self.file_output_name, 'a', encoding='utf8') as output_file:
            output_file.write(text)

    def write_line_separator(self, line: str):
        if line not in self.lines_headers:
            self.lines_headers.add(line)

            with io.open(self.file_output_name, 'a', encoding='utf8') as output_file:
                output_file.write("\n\n")
                output_file.write("//-----------------------------------------")
                output_file.write("// LINE: " + line + " ")
                output_file.write("//-----------------------------------------")
                output_file.write("\n\n")
