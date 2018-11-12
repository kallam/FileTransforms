import csv
from subprocess import DEVNULL, STDOUT, check_call


class _BaseCSV:

    mode = 'r'

    def __init__(self, file_path, delimiter=',', quotechar='"'):
        self.file_path = file_path
        self.delimiter = delimiter
        self.quotechar = quotechar

    def __enter__(self):
        self.file = open(self.file_path, self.mode, newline='')
        self.file.__enter__()
        return self.file

    def __exit__(self, _type, value, traceback):
        self.file.__exit__(_type, value, traceback)


class CSVReader(_BaseCSV):

    mode = 'r'

    def __init__(self, file_path, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC):
        if 'xls' in file_path[-4:]:
            file_path = convert_to_csv(file_path)
        super().__init__(file_path, delimiter=delimiter, quotechar=quotechar)
        self.quoting = quoting

    def __enter__(self):
        super().__enter__()
        return csv.reader((line.replace('\0', '') for line in self.file), delimiter=self.delimiter,
                          quotechar=self.quotechar)


class CSVWriter(_BaseCSV):

    mode = 'w'

    def __init__(self, file_path, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC):
        super().__init__(file_path, delimiter=delimiter, quotechar=quotechar)
        self.quoting = quoting

    def __enter__(self):
        super().__enter__()
        return csv.writer(self.file, delimiter=self.delimiter, quotechar=self.quotechar, quoting=self.quoting)


def read_csv(*args, **kwargs):
    with CSVReader(*args, **kwargs) as csv_data:
        return list(csv_data)


def convert_to_csv(file_path, file_type=None):
    csv_file_path = file_path + '.csv'
    file_type = '-f ' + file_type if file_type is not None else ''
    check_call('in2csv {} "{}" > "{}"'.format(file_type, file_path, csv_file_path), stdout=DEVNULL, stderr=STDOUT,
               shell=True)
    return csv_file_path
