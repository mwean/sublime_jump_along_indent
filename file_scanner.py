import sublime, re
from .view_helper import ViewHelper

class FileScanner:
  def __init__(self, view):
    self.view = view
    self.view_helper = ViewHelper(view)

  def scan_from_beginning(self, direction = 'forward'):
    search_start = self.next_line(self.view_helper.initial_selection().begin())
    return self.search(self.search_str(), search_start) - 1

  def scan_from_end(self, direction = 'forward'):
    view_helper = self.view_helper
    search_start = view_helper.find_bol(view_helper.initial_selection().begin())
    search_end = self.previous_line(view_helper.initial_selection().end())
    return self.reverse_search(self.search_str(), search_start, search_end) - 1

  def scan(self, direction = 'forward'):
    if direction == 'forward':
      return self.search(self.search_str(), self.next_line()) - 1
    else:
      return self.reverse_search(self.search_str(), 0, self.previous_line()) - 1

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

  def previous_line(self, position = None):
    position = position or self.view_helper.initial_cursor_position()
    return self.view.line(position).a - 1

  def next_line(self, position = None):
    position = position or self.view_helper.initial_cursor_position()
    view = self.view
    return view.rowcol(view.line(position).b + 1)[0]

  def search(self, pattern, start_line = None, flags = 0):
    view = self.view

    if start_line:
      start = view.text_point(start_line, 0)
    else:
      start = self.view_helper.initial_cursor_position().begin()
    reg = view.find(pattern, start, flags)

    if not reg is None:
      row = (view.rowcol(reg.begin())[0] + 1)
    else:
      row = self.calculate_relative_ref('.', start_line = start_line)
    return row

  def reverse_search(self, pattern, start = 0, end = -1, flags = 0):
    view = self.view

    if end == -1:
        end = view.size()

    end = self.view_helper.find_eol(view.line(end).a)
    match = self.find_last_match(pattern, start, end)
    return view.rowcol(match.begin())[0] + 1

  def search_in_range(self, pattern, start, end, flags = 0):
    match = self.view.find(pattern, start, flags)
    if match and ((match.begin() >= start) and (match.end() <= end)):
      return True

  def find_last_match(self, pattern, start, end, flags = 0):
    """Find last occurrence of `pattern` between `start`, `end`.
    """
    view = self.view
    match = view.find(pattern, start, flags)
    new_match = None
    while match:
      new_match = view.find(pattern, match.end(), flags)
      if new_match and new_match.end() <= end:
        match = new_match
      else:
        return match

  def calculate_relative_ref(self, where, start_line = None):
    view = self.view

    if where == '$':
      return view.rowcol(view.size())[0] + 1
    if where == '.':
      if start_line:
          return view.rowcol(view.text_point(start_line, 0))[0] + 1
      return view.rowcol(view.sel()[0].begin())[0] + 1
