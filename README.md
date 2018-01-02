# ODK Instantiate
![ODK Instantiate](assets/media/logo/logo_435x388.png?raw=true 
"ODK Instantiate")

A build tool for creating ODK XlsForms from generic reference Excel templates.

## How it works
*# To do*

Notes to add:
- Exclude takes precedence over include.
- all other worksheets will be included if they don't have a build_worksheet.

## How to use
### Prerequisites
**Templates**  
As a prerequisite, you must have one or more stuiable Excel templates 
that can be used to create/instantiate actual ODK forms. Suitable 
templates should, at a minimum, meet the _ODK Instantiate template spec_.

### Command Line Interface (CLI)
*# To do.*

#### Quick-start

| Command Description | Syntax |
|---------------------|--------|
| Build single form from single file. | `python3 -m odk_instantiate INPUT_FILE -n FORM_NAME`|
| Build multiple forms from multiple files. | `python3 -m odk_instantiate INPUT_FILE -n FORM_NAME_1 FORM_NAME_2`|

#### Positional Arguments
- `INPUT_FILE`: _In the form of `path/to/file.xlsx`._

#### Named Arguments
| Short Flag | Long Flag | Required? | Description |
|------------|-----------|-----------|-------------|
| -n         | --form-names | Yes    | What will be the name of the form to instantiate? All rows in the "build" worksheet which have this form name or * in the "includes" field will be added to the created form. |
| -o         | --outpath | No        | Path to write output. If this argument is not supplied, then STDOUT is used. Option Usage: `-o OUPATH`.

## ODK Instantiate Template Specification
### Requirements
This spec is a superset of the XlsForm spec as defined at [XlsForm.org](
http://xlsform.org/). As of _12/28/2017_, the minimum requirements of the spec 
are as shown below.
- File Type
  - Excel file (.xls or .xlsx)
- Required Worksheets & Columns
  - survey
    - type
    - name
    - label
  - choices
    - list_name
    - name
    - label 

In addition to that specification, this spec adds the following requirements.

*# TODO:* Update this
- File Type
  - Excel file (.xlsx)
- Required Worksheets & Columns
  - survey
    - id
  - choices
    - id
  - build
    - worksheet: _Choices, survey, settings, custom worksheets, etc._
    - id: _This must match an value present in the `id` column of the 
    corresponding worksheet. The only requirement for a valid id is that it 
    must be unique._
    - excludes: _Which instantiated forms should this row be excluded from? The 
    value in this cell must be a string representing the form  of a comma 
    delimited list of the form: `[FN_1, FN_2, ..., FN_n]`, where an "`FN`" 
    stands for "Form Name" (see: CLI)._ 
    - includes: _Which instantiated forms should this row be included in? 
    Syntax is the same as for the "excludes" field._

 ### Syntax
*# TODO:* Update this.
 #### Build Worksheet
 - Wildcard character, `*`
   - If present in the `id` field, everything the entire worksheet will be 
   included.
   - If present in the `excludes`/`includes` field, this row will be 
   excluded/included in all templates.
