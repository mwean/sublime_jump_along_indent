import sublime
from unittest import TestCase

class TestHelper(TestCase):
  def setUp(self):
    self.view = sublime.active_window().new_file()
    self.view.settings().set("tab_size", 2)

  def tearDown(self):
    if self.view:
      self.view.set_scratch(True)
      self.view.window().run_command('close_file')

  def set_text(self, lines):
    for line in lines:
      self.view.run_command('move_to', { 'to': 'bol', 'extend': True })
      self.view.run_command('insert', { 'characters': line + "\n" })

  def check_command(self, text, start, end, extend_selection=False, indent_offset=0):
    self.set_text(text)
    self.view.sel().clear()
    self.view.sel().add(sublime.Region(start[0], start[1]))
    self.view.run_command(self.command(), { 'extend_selection': extend_selection, 'indent_offset': indent_offset })

    self.assertEqual(self.view.sel()[0], sublime.Region(end[0], end[1]))
