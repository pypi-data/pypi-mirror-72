# multi-rename

A python module for renaming multiple files in a directory to a common format ending in incrementing numbers.

## Installation

Install using pip:

```sh
pip install multi-rename
```

## Usage

```Python
from multi_rename import renamer

# Full Rename
renamer.full_rename(dir_path='/path/to/dir/here', new_name='new_file_name')

# Add prefix
renamer.add_affix(dir_path='/path/to/dir/here', affix='prefix_to_add', affix_type='prefix')

# Add suffix
renamer.add_affix(dir_path='/path/to/dir/here', affix='suffix_to_add', affix_type='suffix')

```

## Example

```Python
renamer.full_rename('/home/test_imgs/','newname')
```

This will make all the files in the directory to be renamed as:

```
newname1.jpg
newname2.pdf
newname3.png
...
```

## Contributing

If you have any bug fixes / useful feature additions, feel free to fork this repository, make your changes and drop in a pull request.

## License

[MIT](https://github.com/pshkrh/multi-rename/blob/master/LICENSE)