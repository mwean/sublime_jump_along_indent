from helper import TestHelper
import sublime

class TestJumpPrevIndent(TestHelper):
  def command(self):
    return 'jump_prev_indent'

  def test_empty_lines(self):
    lines = [
      'Lorem ipsum dolor sit amet',
      '',
      '',
      'Lorem ipsum dolor sit amet'
    ]
    starting_selection = [29, 29]
    ending_selection = [0, 0]

    self.check_command(lines, starting_selection, ending_selection)

  def test_indented_lines(self):
    lines = [
      'Lorem ipsum dolor sit amet',
      '  Lorem ipsum dolor sit amet',
      '  Lorem ipsum dolor sit amet',
      'Lorem ipsum dolor sit amet'
    ]

    starting_selection = [85, 85]
    ending_selection = [0, 0]

    self.check_command(lines, starting_selection, ending_selection)

  def test_beginning_of_file(self):
    lines = [
      '  Lorem ipsum dolor sit amet',
      '  Lorem ipsum dolor sit amet',
      'Lorem ipsum dolor sit amet'
    ]

    starting_selection = [58, 58]
    ending_selection = [58, 58]

    self.check_command(lines, starting_selection, ending_selection)

  def test_maintain_column(self):
    lines = [
      'Lorem ipsum dolor sit amet',
      'Lorem ipsum dolor sit amet',
      'Lorem ipsum dolor sit amet'
    ]

    starting_selection = [66, 66]
    ending_selection = [12, 12]

  def test_jump_to_shorter_line(self):
    lines = [
      'Lorem ipsum dolor sit amet',
      '',
      'Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet'
    ]

    starting_selection = [81, 81]
    ending_selection = [26, 26]

    self.check_command(lines, starting_selection, ending_selection)

  def test_jump_to_first_intersection(self):
    lines = [
      '  Lorem ipsum dolor sit amet',
      '',
      '    Lorem ipsum dolor sit amet'
    ]

    starting_selection = [33, 33]
    ending_selection = [3, 3]

    self.check_command(lines, starting_selection, ending_selection)

  def test_create_selection(self):
    lines = [
      'Lorem ipsum dolor sit amet',
      '  Lorem ipsum dolor sit amet',
      '  Lorem ipsum dolor sit amet',
      'Lorem ipsum dolor sit amet'
    ]

    starting_selection = [85, 85]
    ending_selection = [85, 0]

    self.check_command(lines, starting_selection, ending_selection, extend_selection = True)

  def test_extend_selection(self):
    lines = [
      'Lorem ipsum dolor sit amet',
      '  Lorem ipsum dolor sit amet',
      '  Lorem ipsum dolor sit amet',
      'Lorem ipsum dolor sit amet'
    ]

    starting_selection = [85, 56]
    ending_selection = [85, 0]

    self.check_command(lines, starting_selection, ending_selection, extend_selection = True)

  def test_subtract_selection(self):
    lines = [
      'Lorem ipsum dolor sit amet',
      '  Lorem ipsum dolor sit amet',
      '  Lorem ipsum dolor sit amet',
      'Lorem ipsum dolor sit amet'
    ]

    starting_selection = [0, 85]
    ending_selection = [0, 0]

    self.check_command(lines, starting_selection, ending_selection, extend_selection = True)

  def test_respect_cursor_position(self):
    lines = [
      'Lorem ipsum dolor sit amet',
      '  Lorem ipsum dolor sit amet',
      '  Lorem ipsum dolor sit amet'
    ]

    starting_selection = [57, 57]
    ending_selection = [1, 1]

    self.check_command(lines, starting_selection, ending_selection)

  def test_disrespect_cursor_position(self):
    settings = sublime.load_settings("jump_along_indent.sublime-settings")
    settings.set("respect_cursor_position", False)

    lines = [
      'Lorem ipsum dolor sit amet',
      '  Lorem ipsum dolor sit amet',
      '  Lorem ipsum dolor sit amet'
    ]

    starting_selection = [57, 57]
    ending_selection = [28, 28]

    self.check_command(lines, starting_selection, ending_selection)

    settings.set("respect_cursor_position", True)
