from helper import TestHelper

class TestJumpOffsetIndent(TestHelper):
  def command(self):
    return 'jump_prev_indent'

  def test_positive_indent_offset(self):
    lines = [
      '  Lorem ipsum dolor sit amet',
      '',
      'Lorem ipsum dolor sit amet',
      'Lorem ipsum dolor sit amet'
    ]
    starting_selection = [57, 57]
    ending_selection = [0, 0]

    self.check_command(lines, starting_selection, ending_selection, indent_offset = 1)

  def test_negative_indent_offset(self):
    lines = [
      '  Lorem ipsum dolor sit amet',
      '',
      'Lorem ipsum dolor sit amet',
      '  Lorem ipsum dolor sit amet'
    ]
    starting_selection = [59, 59]
    ending_selection = [32, 32]

    self.check_command(lines, starting_selection, ending_selection, indent_offset = -1)


  def test_block_skip(self):
    lines = [
      '',
      'Lorem ipsum dolor sit amet',
      'Lorem ipsum dolor sit amet',
      '  Lorem ipsum dolor sit amet'
    ]
    starting_selection = [57, 57]
    ending_selection = [30, 30]

    self.check_command(lines, starting_selection, ending_selection, indent_offset = -1)
