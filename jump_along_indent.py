import sublime, sublime_plugin, re, sys
from .file_scanner import FileScanner
from .view_helper import ViewHelper

def cursor_position(view):
  return view.sel()[0]

def build_selection(view, new_region, target):
  view.sel().clear()
  view.sel().add(new_region)
  view.show(target)

class JumpNextIndentCommand(sublime_plugin.TextCommand):
  def run(self, edit, extend_selection = False):
    view = self.view
    self.view_helper = ViewHelper(view)
    self.scanner = FileScanner(view)
    cursor_at_top_of_selection = self.view_helper.cursor_at_top_of_selection()

    if not extend_selection:
      self.jump_downward()
    elif cursor_at_top_of_selection:
      self.deselect_downward()
    else:
      self.select_downward()

  def jump_downward(self):
    target = self.target_point()
    new_region = sublime.Region(target, target, self.view_helper.initial_xpos())
    build_selection(self.view, new_region, target)

  def select_downward(self):
    target = self.target_point()
    view_helper = self.view_helper
    new_region = sublime.Region(view_helper.initial_selection().begin(), target, view_helper.initial_xpos())
    build_selection(self.view, new_region, target)

  def deselect_downward(self):
    matched_row = self.scanner.scan()
    target = self.target_point(matched_row)
    view_helper = self.view_helper
    new_region = sublime.Region(view_helper.initial_selection().end(), target, view_helper.initial_xpos())
    build_selection(self.view, new_region, target)

  def target_point(self, matched_row = None):
    matched_row = matched_row or self.scanner.scan()
    matched_point_bol = self.view.text_point(matched_row, 0)
    return self.view.text_point(matched_row, self.view_helper.target_column(matched_point_bol))

class JumpPrevIndentCommand(sublime_plugin.TextCommand):
  def run(self, edit, extend_selection = False):
    view = self.view
    self.view_helper = ViewHelper(view)
    self.scanner = FileScanner(view)
    cursor_at_bottom_of_selection = self.view_helper.cursor_at_bottom_of_selection()

    if not extend_selection:
      self.jump_upward()
    elif cursor_at_bottom_of_selection:
      self.deselect_upward()
    else:
      self.select_upward()

  def jump_upward(self):
    target = self.target_point()
    new_region = sublime.Region(target, target, self.view_helper.initial_xpos())
    build_selection(self.view, new_region, target)

  def select_upward(self):
    target = self.target_point()
    view_helper = self.view_helper
    new_region = sublime.Region(view_helper.initial_selection().end(), target, view_helper.initial_xpos())
    build_selection(self.view, new_region, target)

  def deselect_upward(self):
    matched_row = self.scanner.scan('backward')
    target = self.target_point(matched_row)
    new_region = sublime.Region(self.view_helper.initial_selection().begin(), target)
    view_helper = self.view_helper
    new_region = sublime.Region(view_helper.initial_selection().begin(), target, view_helper.initial_xpos())
    build_selection(self.view, new_region, target)

  def target_point(self, matched_row = None):
    matched_row = matched_row or self.scanner.scan(direction = 'backward')
    matched_point_bol = self.view.text_point(matched_row, 0)
    return self.view.text_point(matched_row, self.view_helper.target_column(matched_point_bol))
