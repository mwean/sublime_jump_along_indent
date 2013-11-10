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
    new_region = sublime.Region(target)
    build_selection(self.view, new_region, target)

  def select_downward(self):
    target = self.target_point()
    new_region = sublime.Region(self.view_helper.initial_selection().begin(), target)
    build_selection(self.view, new_region, target)

  def deselect_downward(self):
    matched_point = self.scanner.scan()
    target = self.target_point(matched_point)
    new_region = sublime.Region(self.view_helper.initial_selection().end(), target)
    build_selection(self.view, new_region, target)

  def target_point(self, matched_point = None):
    matched_point = matched_point or self.scanner.scan()
    return self.view.text_point(matched_point, self.view_helper.target_column(matched_point))

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
    new_region = sublime.Region(target)
    build_selection(self.view, new_region, target)

  def select_upward(self):
    target = self.target_point()
    new_region = sublime.Region(self.view_helper.initial_selection().end(), target)
    build_selection(self.view, new_region, target)

  def deselect_upward(self):
    matched_point = self.scanner.scan('backward')
    target = self.target_point(matched_point)
    new_region = sublime.Region(self.view_helper.initial_selection().begin(), target)
    build_selection(self.view, new_region, target)

  def target_point(self, matched_point = None):
    matched_point = matched_point or self.scanner.scan(direction = 'backward')
    return self.view.text_point(matched_point, self.view_helper.target_column(matched_point))
