import csv
from subprocess import DEVNULL, STDOUT, check_call


def read_csv(file_path, *args, **kwargs):
    with open(file_path, 'r', newline='') as f:
        return list(csv.reader(f, *args, **kwargs))


def write_csv(file_path, data, *args, **kwargs):
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f, *args, **kwargs)
        writer.writerows(data)


def convert_to_csv(file_path, file_type=None):  # pragma: no cover
    csv_file_path = file_path + '.csv'
    file_type = '-f ' + file_type if file_type is not None else ''
    check_call('in2csv {} "{}" > "{}"'.format(file_type, file_path, csv_file_path), stdout=DEVNULL, stderr=STDOUT,
               shell=True)
    return csv_file_path
