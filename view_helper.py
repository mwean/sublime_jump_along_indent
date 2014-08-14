class ViewHelpers:
  def __init__(self, view):
    self.view = view

  def __iter__(self):
    for sel in self.view.sel():
      yield ViewHelper(self.view, sel)


class ViewHelper:
  def __init__(self, view, sel):
    self.view = view
    self.sel = sel

  def initial_xpos(self):
    return self.view.text_to_layout(self.initial_cursor_position())[0]

  def initial_cursor_position(self):
    return self.initial_selection().b

  def initial_selection(self):
    return self.sel

  def initial_column(self):
    return self.view.rowcol(self.initial_cursor_position())[1]

  def initial_row(self):
    return self.view.rowcol(self.initial_cursor_position())[0]

  def cursor_at_top_of_selection(self):
    return self.initial_selection().a > self.initial_selection().b

  def cursor_at_bottom_of_selection(self):
    return self.initial_selection().b > self.initial_selection().a

  def target_column(self, target, indent_offset):
    tab_size = self.view.settings().get("tab_size")
    offset_column = self.initial_column() + tab_size * indent_offset
    end_of_line = self.view.rowcol(self.find_eol(target))[1]

    if offset_column > end_of_line:
      return end_of_line
    else:
      return offset_column

  def find_eol(self, point):
    return self.view.line(point).end()

  def find_bol(self, point):
    return self.view.line(point).begin()
