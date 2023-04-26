import pytest
from pomodoro import pad_title


@pytest.mark.parametrize(
    'title, length, expected_pad_title',
    [
        ('Start', 19, '        Start        '),
        ('End', 19, '         End         '),
        ('Start', 20, '        Start         '),
        ('Start', 2, ' Start '),
    ]
)
def test_pad_title_given_title_string_when_padded_then_it_should_return_padded_title_according_to_expected_column_length(title, length, expected_pad_title):
    padded = pad_title(title, length)
    assert padded == expected_pad_title
