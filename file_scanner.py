import sublime, re
from .view_helper import ViewHelper

class FileScanner:
  def __init__(self, view, viewhelper):
    self.view = view
    self.view_helper = viewhelper

  def scan(self, direction = 'forward'):
    if direction == 'forward':
      indent_match = self.search(self.search_str(), self.next_point()) or 0
      block_match = self.find_last_line_of_block()
      return max([indent_match, block_match])
    else:
      if self.previous_point() < 0:
        end = 0
      else:
        end = self.previous_point()

      indent_match = self.reverse_search(self.search_str(), 0, end)
      block_match = self.find_first_line_of_block(end)
      return min([indent_match, block_match])

  def search_str(self):
    if re.match(r"^\s*$", self.str_to_left()) and re.match(r"^\s+\S+", self.str_to_right()):
      search_str = "^ {0," + str(len(self.str_to_left())) + "}\S+"
    else:
      search_str = "^" + self.leading_spaces() + "\S"
    return search_str

  def str_to_left(self):
    view = self.view
    sel_pt = self.view_helper.initial_cursor_position()
    left_pt = view.line(sel_pt).a
    left_region = sublime.Region(left_pt, sel_pt)
    return view.substr(left_region)

  def str_to_right(self):
    view = self.view
    sel_pt = self.view_helper.initial_cursor_position()
    right_pt = view.line(sel_pt).b
    right_region = sublime.Region(sel_pt, right_pt)
    return view.substr(right_region)

  def leading_spaces(self):
    spaces = re.match(r"(\s*)", self.current_line())
    return spaces.group(0)

  def current_line(self):
    view = self.view
    line_region = view.line(self.view_helper.initial_cursor_position())
    return view.substr(line_region)

  def previous_point(self, position = None):
    position = position or self.view_helper.initial_cursor_position()
    return self.view.line(position).a - 1

  def previous_line(self, position = None):
    return self.view.rowcol(self.previous_point(position))[0]

  def next_point(self, position = None):
    position = position or self.view_helper.initial_cursor_position()
    return self.view.line(position).b + 1

  def next_line(self, position = None):
    return self.view.rowcol(self.next_point(position))[0]

  def search(self, pattern, start = None, flags = 0):
    view = self.view
    start = start or self.view_helper.initial_cursor_position()
    match = view.find(pattern, start, flags)

    if not match.a == -1:
      matched_row = view.rowcol(match.begin())[0]
      return matched_row

  def reverse_search(self, pattern, start = 0, end = -1):
    view = self.view

    if end == -1:
      end = view.size()

    end = self.view_helper.find_eol(view.line(end).a)
    match = self.find_last_match(pattern, start, end)

    if match == None:
      return self.view_helper.initial_row()
    else:
      matched_row = view.rowcol(match.begin())[0]
      return matched_row

  def find_last_match(self, pattern, start, end):
    matches = self.view.find_all(pattern)
    filtered_matches = [match for match in matches if match.begin() >= start and match.begin() <= end]

    if len(filtered_matches) > 0:
      return filtered_matches[-1]

  def find_last_line_of_block(self):
    view = self.view
    matched_line = self.search(self.block_pattern())
    last_line = view.rowcol(view.size())[0]

    if not matched_line or (matched_line == last_line - 1 and self.block_extends_to_bottom()):
      return last_line
    else:
      return matched_line - 1

  def find_first_line_of_block(self, end):
    pattern = self.block_pattern() + "|(^\A.*$)"
    matched_line = self.reverse_search(pattern, 0, end)

    if matched_line == 0 and self.block_extends_to_top():
      return 0
    else:
      return matched_line + 1

  def block_extends_to_top(self):
    return self.view.find("\A" + self.leading_spaces() + "\S", 0)

  def block_extends_to_bottom(self):
    return self.view.find("^" + self.leading_spaces() + "\S.*\z", self.next_point())

  def block_pattern(self):
    pattern = "(^\s*$)"
    space_count = len(self.leading_spaces())

    if space_count > 0:
      pattern += "|(^ {0," + str(space_count - 1) + "}\S+)"

    pattern += "|(^ {" + str(space_count + 1) + ",}\S+)"
    return pattern
