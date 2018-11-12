from typing import Dict, Callable, Union
import struct


class TextImporter:
    """
    Imports a fixed width file
    """

    def __init__(self, field_widths):
        """
        Set the initial field widths values. Negative values indicate that section should be skipped.

        :param field_widths: A single list of integers (or dictionary with int values) that indicate the field widths
        """
        self.parse: Union[Dict, Callable, None] = None
        self.verbose = False

        if not isinstance(field_widths, dict):
            field_widths = list(field_widths)

        self.field_widths = field_widths

    def read_fixed_width(self, s: str):
        """
        Parse a single line of input with the field widths values.

        :param s: A single line of text that needs to be separated
        :returns: A list of values that are parsed from the input text based on the field widths.
                  This list is empty if a field widths dictionary cannot be matched to the input text.
        """

        def build_fmt_string(field_widths):
            """
            Build the formatting function that splits the input text.

            :param field_widths: A list of integers that indicate the field widths
            :returns: A function that is used to split a string into a list of strings
            """
            fmt_string = ' '.join('{}{}'.format(abs(fw), 'x' if fw < 0 else 's') for fw in field_widths)
            field_struct = struct.Struct(fmt_string)
            return field_struct.unpack_from

        def fw_length(field_widths):
            """
            Calculate the total length of the field width definition. Absolute values are used so that negative values
            (which indicate skipped characters) are accounted for properly.

            :param field_widths: A list of integers that indicate the field widths
            :returns: The sum of field width lengths
            """
            return sum(map(abs, field_widths))

        def build_trimmed_fw(field_widths, line):
            """
            Build a custom parsing function that works on input strings that don't include padding for optional fields.

            :param field_widths: A list of integers that indicate the field widths
            :param line: A single line of text that needs to be separated
            :returns: A function that is used to split a string into a list of strings
            """
            while fw_length(field_widths) > len(line):
                dropped = field_widths.pop()
                if self.verbose:
                    print('Had to drop {} from {}'.format(dropped, key))
            diff = len(line) - fw_length(field_widths)
            if diff > 0:
                if self.verbose:
                    print('Added back {}'.format(diff))
                field_widths.append(diff)
            return build_fmt_string(field_widths)

        if isinstance(self.field_widths, dict):
            # Choose the appropriate field_widths list from the dictionary
            key = None
            for k in self.field_widths:
                if len(k) <= len(s) and k == s[:len(k)]:
                    key = k
                    break

            if key is None:
                print('Could not format line where the first 5 characters are {}'.format(s[:5]))
                return []

            if self.parse is None or key not in self.parse:
                if self.parse is None:
                    self.parse = {}

                self.parse[key] = build_fmt_string(self.field_widths[key])
            if len(s) >= fw_length(self.field_widths[key]):
                parser = self.parse[key]
            else:
                parser = build_trimmed_fw(self.field_widths[key][:], s)

        else:
            # Only one field_widths list is available
            if self.parse is None:
                self.parse = build_fmt_string(self.field_widths)

            if len(s) >= fw_length(self.field_widths):
                parser = self.parse
            else:
                parser = build_trimmed_fw(self.field_widths[:], s)

        ret = []
        parsed = parser(str.encode(s))
        for p in parsed:
            ret.append(p.decode(encoding='latin-1').strip())
        return ret

    def read_file(self, file_path):
        """
        Parse all the lines of a file.

        :param file_path: Input file path
        :returns: A list of parsed lines from the input file.
        """
        input_data = []
        with open(file_path, 'r') as f:
            for i, l in enumerate(f):
                try:
                    v = self.read_fixed_width(l)
                except Exception as e:
                    print('Failed within \'{}\' on line {}: {}'.format(file_path, i, l))
                    raise e
                input_data.append(v)
                if self.verbose:
                    print(v)
        return input_data
