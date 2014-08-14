from helper import TestHelper

class TestJumpNextIndent(TestHelper):
  def command(self):
    return 'jump_next_indent'

  def test_empty_lines(self):
    lines = [
      'Lorem ipsum dolor sit amet',
      '',
      '',
      'Lorem ipsum dolor sit amet'
    ]
    starting_selection = [0, 0]
    ending_selection = [29, 29]

    self.check_command(lines, starting_selection, ending_selection)

  def test_indented_lines(self):
    lines = [
      'Lorem ipsum dolor sit amet',
      '  Lorem ipsum dolor sit amet',
      '  Lorem ipsum dolor sit amet',
      'Lorem ipsum dolor sit amet'
    ]

    starting_selection = [0, 0]
    ending_selection = [85, 85]

    self.check_command(lines, starting_selection, ending_selection)

  def test_end_of_file(self):
    lines = [
      'Lorem ipsum dolor sit amet',
      '  Lorem ipsum dolor sit amet',
      '  Lorem ipsum dolor sit amet'
    ]

    starting_selection = [0, 0]
    ending_selection = [0, 0]

    self.check_command(lines, starting_selection, ending_selection)

  def test_maintain_column(self):
    lines = [
      'Lorem ipsum dolor sit amet',
      'Lorem ipsum dolor sit amet',
      'Lorem ipsum dolor sit amet'
    ]

    starting_selection = [12, 12]
    ending_selection = [66, 66]

    self.check_command(lines, starting_selection, ending_selection)

  def test_jump_to_shorter_line(self):
    lines = [
      'Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet',
      '',
      'Lorem ipsum dolor sit amet'
    ]

    starting_selection = [53, 53]
    ending_selection = [81, 81]

    self.check_command(lines, starting_selection, ending_selection)

  def test_jump_to_first_intersection(self):
    lines = [
      '    Lorem ipsum dolor sit amet',
      '',
      '  Lorem ipsum dolor sit amet'
    ]

    starting_selection = [3, 3]
    ending_selection = [35, 35]

    self.check_command(lines, starting_selection, ending_selection)

  def test_create_selection(self):
    lines = [
      'Lorem ipsum dolor sit amet',
      '  Lorem ipsum dolor sit amet',
      '  Lorem ipsum dolor sit amet',
      'Lorem ipsum dolor sit amet'
    ]

    starting_selection = [0, 0]
    ending_selection = [0, 85]

    self.check_command(lines, starting_selection, ending_selection, extend_selection = True)

  def test_extend_selection(self):
    lines = [
      'Lorem ipsum dolor sit amet',
      '  Lorem ipsum dolor sit amet',
      '  Lorem ipsum dolor sit amet',
      'Lorem ipsum dolor sit amet'
    ]

    starting_selection = [0, 27]
    ending_selection = [0, 85]

    self.check_command(lines, starting_selection, ending_selection, extend_selection = True)

  def test_subtract_selection(self):
    lines = [
      'Lorem ipsum dolor sit amet',
      '  Lorem ipsum dolor sit amet',
      '  Lorem ipsum dolor sit amet',
      'Lorem ipsum dolor sit amet'
    ]

    starting_selection = [111, 0]
    ending_selection = [111, 85]

    self.check_command(lines, starting_selection, ending_selection, extend_selection = True)
