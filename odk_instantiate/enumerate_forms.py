"""Enumerate set of forms from source data."""
import csv

from odk_instantiate.config import DATA_DIR


FORMS_DIR = DATA_DIR + 'forms/'
FORMS_SRC_DIR = FORMS_DIR + 'src/'
FORMS_ELEMENTS = FORMS_SRC_DIR + 'form_elements.csv'


def csv_to_2d_arr(path):
    """Serialize CSV file to a 2d array."""
    _2d_arr = []

    with open(path, 'r') as csv_data:
        rows = csv.reader(csv_data, delimiter=',')
        for row in rows:
            _2d_arr.append(row)

    return _2d_arr


def _2d_arr_to_dict(arr):
    """Convert 2d array to dictionary."""
    _dict = {}

    for row in arr[1:]:
        _dict[row[0]] = row[1].split(',')

    return _dict


def generate_form_set(form_elements):
    """Generate form set."""
    header = ['id', 'name', 'set', 'country', 'round', 'type']
    forms = [header]

    counter = 0
    for _set in form_elements['set']:
        for country in form_elements['country']:
            for _round in form_elements['round']:
                for _type in form_elements['type']:
                    name = _set + ' ' + country + 'R' + _round + ' ' + _type
                    row = [counter, name, _set, country, _round, _type]
                    forms.append(row)
                    counter += 1

    return forms


def save_forms_as_csv(path, _form_set):
    """Save forms as csv"""

    with open(path, 'w') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',')
        csv_writer.writerows(_form_set)
        #

def run():
    """Run."""
    form_elements1 = csv_to_2d_arr(FORMS_ELEMENTS)
    form_elements2 = _2d_arr_to_dict(form_elements1)
    form_set = generate_form_set(form_elements2)

    print(form_set)

    save_forms_as_csv(path=FORMS_DIR+'forms.csv', _form_set=form_set)


if __name__ == '__main__':
    run()
