"""ODK Instantiate"""
import xlrd


config = {
    'form_content_definitions_worksheet_name': 'forms_content_definitions',
    'survey_content_labels_worksheet_name': 'survey_content_labels',
    'choices_content_labels_worksheet_name': 'choices_content_labels',
    'field_types': {
        'id': int,
        'name': str,
        'set': str,
        'country': str,
        'round': int,
        'type': str,
        'content': bool
    }
}


def instantiate(path, form, outpath=None, form_content_defs=None):
    """Instantiate form.

    Args:
        path (str): Path to template file.
        form (str): The name of the form to instantiate.
        **outpath (str): Path to save file.
        **form_content_defs (dict): A dictionary, indexed either by numeric id
            or string name, which defines the survey, including all content
            that should be included.
    """
    wb = xlrd.open_workbook(path)

    survey_arr = ws_to_2d_arr(wb.sheet_by_name('survey'))
    choices_arr = ws_to_2d_arr(wb.sheet_by_name('choices'))
    survey_content_labels_arr = ws_to_2d_arr(wb.sheet_by_name(
        config['survey_content_labels_worksheet_name']))
    choices_content_labels_arr = ws_to_2d_arr(wb.sheet_by_name(
        config['choices_content_labels_worksheet_name']))

    survey = _2d_arr_to_dict(survey_arr, index_by='id')
    choices = _2d_arr_to_dict(choices_arr, index_by='id')
    survey_content_labels = \
        _2d_arr_to_dict(survey_content_labels_arr, index_by='id')
    choices_content_labels = \
        _2d_arr_to_dict(choices_content_labels_arr, index_by='id')

    _def = form_content_defs[form] if form_content_defs else \
        _2d_arr_to_dict(ws_to_2d_arr(wb.sheet_by_name(
            config['form_content_definitions_worksheet_name'])),
            index_by='name')

    # TODO: Survey and choices content label need to be transformed into a new
    # format, something like: ID: {'types': 'hq': BOOL, ...}, ...}
    # Should that be done here or in instantiate_form_dict()?

    form2 = instantiated_form_dict(
        form_content_def=_def,
        survey_data=survey,
        choices_data=choices,
        survey_content_labels=survey_content_labels,
        choices_content_labels=choices_content_labels)
    form3 = instantiated_form_2d_arr(form2)

    save_file(content=form3, outpath=outpath)


def instantiated_form_dict(form_content_def, survey_data, choices_data,
                           survey_content_labels,
                           choices_content_labels):
    """Instantiated form dictionary.

    Args:
        form_content_def (dict): Definition of what content to include in form.
        survey_data (dict): Survey data, indexed by id.
        choices_data (dict): Choices data, indexed by id.
        survey_content_labels (dict): Content labels for each element (row) of
            survey data, indexed by id.
        choices_content_labels (dict): Content labels for each element (row) of
            choices data, indexed by id.
    """
    _dict = {}

    # Testing
    print(survey_data)
    print(survey_content_labels)
    print(choices_data)
    print(choices_content_labels)
    print(form_content_def)

    return _dict


def instantiated_form_2d_arr(_dict):
    """Instantiated form dictionary."""
    arr = []

    if _dict:
        pass

    return arr


def format_cell_value(raw_value, rule):
    """Format cell."""
    return rule(raw_value)


def format_cell_values(raw_rows, rules):
    """Format cells."""
    raw_header = [field for field in raw_rows[0]]
    blank_indexes = \
        [index for index, val in enumerate(raw_header) if val == '']
    header = [field for field in raw_header if field != '']
    formatted_rows = [header]

    for row in raw_rows[1:]:
        formatted_row = []
        for index, cell in enumerate(row):
            if index not in blank_indexes:
                if cell == '':
                    formatted_row.append(cell)
                else:
                    _rule = rules['content'] if raw_header[index]\
                        .startswith('content_') else rules[raw_header[index]]
                    formatted_cell = format_cell_value(cell, _rule)
                    formatted_row.append(formatted_cell)
        formatted_rows.append(formatted_row)

    return formatted_rows


def ws_to_2d_arr(ws):
    """XLRD Worksheet to 2d array."""
    rows = []
    for i, row in enumerate(range(ws.nrows)):
        cells = []
        for j, col in enumerate(range(ws.ncols)):
            cells.append(ws.cell_value(i, j))
        rows.append(cells)
    return rows


def form_content_file_to_2d_arr(path):  # - Temporary; for mock CLI
    """Get 2d array form content definitions from file."""
    ws_name = config['form_content_definitions_worksheet_name']
    wb = xlrd.open_workbook(path)
    num_worksheets = len(wb.sheet_names())

    if num_worksheets == 1:
        ws = wb.sheet_by_index(0)
    else:
        ws = wb.sheet_by_name(ws_name)

    rows = ws_to_2d_arr(ws)
    rows2 = format_cell_values(raw_rows=rows, rules=config['field_types'])

    return rows2


def _2d_arr_to_dict(arr, index_by='name'):
    """Convert 2d array to dictionary.

    Args:
        arr (list): 2d array.
        index_by (str): What column to index by? Should be 'name' or 'id.
    """
    form_content_defs = {}
    header = arr[0]
    index = {col_name: header.index(col_name) for col_name in header}

    for row in arr[1:]:
        form_content_defs[row[index[index_by]]] = {
            key: row[index[key]]
            for key in index
        }

    return form_content_defs


def save_file(content, outpath=None):
    """Save file."""
    if outpath and content:
        pass


if __name__ == '__main__':
    # template, form, kwargs = cli()

    # - Mock CLI values
    from odk_instantiate.config import ROOT_DIR
    template = ROOT_DIR + 'test/files/templates/SQ.xlsx'
    form_name = 'Core BFR1 HQ'
    form_content_defs_raw = form_content_file_to_2d_arr(template)
    kwargs = {
        'outpath': None,
        'form_content_defs': _2d_arr_to_dict(form_content_defs_raw)
    }

    instantiate(path=template, form=form_name, **kwargs)
