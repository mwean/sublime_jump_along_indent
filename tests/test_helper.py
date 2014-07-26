import sublime, sys, json, sublime_plugin
from unittest import TestCase

class TestHelper(TestCase):
  def setUp(self):
    self.view = sublime.active_window().new_file()

  def tearDown(self):
    if self.view:
      self.view.set_scratch(True)
      self.view.window().run_command('close_file')

  def set_text(self, lines):
    for line in lines:
      self.view.run_command('move_to', { 'to': 'bol', 'extend': True })
      self.view.run_command('insert', { 'characters': line + "\n" })

  def check_command(self, text, start, end, extend_selection=False):
    self.set_text(text)
    self.view.sel().clear()
    self.view.sel().add(sublime.Region(start[0], start[1]))
    self.view.run_command(self.command(), { 'extend_selection': extend_selection })

    self.assertEqual(self.view.sel()[0], sublime.Region(end[0], end[1]))
