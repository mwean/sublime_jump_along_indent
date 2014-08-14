import sublime
import sublime_plugin
from .file_scanner import FileScanner
from .view_helper import ViewHelpers


class JumpIndentCommand(object):
  def run(self, edit, extend_selection=False, indent_offset=0):
    self.indent_offset = indent_offset
    self.clear_selection()
    for self.view_helper in ViewHelpers(self.view):
      self.scanner = FileScanner(self.view, self.view_helper)

      if not extend_selection:
        self.jump()
      elif self.check_selection_pos():
        self.deselect()
      else:
        self.select()

    self.update_selection()

  def clear_selection(self):
    self.listsel = []

  def build_selection(self, new_region):
    self.listsel.append(new_region)

  def update_selection(self):
    self.view.sel().clear()
    for s in self.listsel:
      self.view.sel().add(s)
    self.view.show(s)

  def jump(self):
    target = self.target_point()
    new_region = sublime.Region(target, target, self.view_helper.initial_xpos())
    self.build_selection(new_region)

  def select(self):
    target = self.target_point()
    new_region = sublime.Region(self.get_select_begin_pos(), target, self.view_helper.initial_xpos())
    self.build_selection(new_region)

  def deselect(self):
    matched_row = self.scanner.scan(self.direction, self.indent_offset)
    target = self.target_point(matched_row)
    new_region = sublime.Region(self.get_deselect_begin_pos(), target, self.view_helper.initial_xpos())
    self.build_selection(new_region)

  def target_point(self, matched_row=None):
    matched_row = matched_row or self.scanner.scan(self.direction, self.indent_offset)
    selection_offset = self.indent_offset

    if matched_row == self.view_helper.initial_row():
      selection_offset = 0

    matched_point_bol = self.view.text_point(matched_row, 0)
    return self.view.text_point(matched_row, self.view_helper.target_column(matched_point_bol, selection_offset))


class JumpNextIndentCommand(JumpIndentCommand, sublime_plugin.TextCommand):
  def __init__(self, *args, **kwargs):
    super(JumpNextIndentCommand, self).__init__(*args, **kwargs)
    self.direction = 'forward'

  def check_selection_pos(self):
    return self.view_helper.cursor_at_top_of_selection()

  def get_select_begin_pos(self):
    return self.view_helper.initial_selection().begin()

  def get_deselect_begin_pos(self):
    return self.view_helper.initial_selection().end()


class JumpPrevIndentCommand(JumpIndentCommand, sublime_plugin.TextCommand):
  def __init__(self, *args, **kwargs):
    super(JumpPrevIndentCommand, self).__init__(*args, **kwargs)
    self.direction = 'backward'

  def check_selection_pos(self):
    return self.view_helper.cursor_at_bottom_of_selection()

  def get_select_begin_pos(self):
    return self.view_helper.initial_selection().end()

  def get_deselect_begin_pos(self):
    return self.view_helper.initial_selection().begin()
