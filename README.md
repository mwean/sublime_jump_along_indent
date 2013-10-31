# Sublime Jump Along Indent #

## Description ##

A Sublime Text 3 plugin to move the cursor to next/previous line at the same indentation level as the current line.

There are two commands: `jump_next_indent` and `jump_prev_indent`.

![Before jumping downward](https://s3.amazonaws.com/mwean-github/sublime_jump_along_indent/pre_jump.png) → ![After jumping downward](https://s3.amazonaws.com/mwean-github/sublime_jump_along_indent/post_jump.png)

If the cursor is to the left of an indented line, it will jump to the next line that is at that level or less.

![Before jumping downward](https://s3.amazonaws.com/mwean-github/sublime_jump_along_indent/pre_jump_inset.png) → ![After jumping downward](https://s3.amazonaws.com/mwean-github/sublime_jump_along_indent/post_jump_inset.png)

There is also an option to extend the selection while jumping:

![Before selecting downward](https://s3.amazonaws.com/mwean-github/sublime_jump_along_indent/pre_jump.png) → ![After selecting downward](https://s3.amazonaws.com/mwean-github/sublime_jump_along_indent/post_select.png)

## Installation ##

### Using Package Control ###
  - Select "Package Control: Install Package" from the Command Palette
  - Search for "Jump Along Indent"
 
### Using Git ###
  - Clone the repository in your Sublime Text Packages directory:
  - `git clone https://github.com/mwean/sublime_jump_along_indent.git /path/to/sublime/packages`

### Not Using Git ###
  - [Download code archive](https://github.com/mwean/sublime_jump_along_indent/archive/master.zip)
  - Unzip and move to Sublime Text packages folder

## Usage ##

The plugin comes with a set of default keybindings:
  
  - `alt+up`: Jump to previous indented line
  - `alt+down`: Jump to next indented line
  - `alt+shift+up`: Jump to previous indented line and extend selection
  - `alt+shift+down`: Jump to next indented line and extend selection

## Credits ##

Some of the methods in `file_scanner.py` were adapted from the [VintageEx](https://github.com/SublimeText/VintageEx) plugin.
