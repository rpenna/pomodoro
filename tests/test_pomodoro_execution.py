import pytest
from datetime import datetime
from pomodoro import run, get_duration, get_next_break


@pytest.fixture
def pomodoro_settings():
    return {
        'pomodoro_time': 25,
        'short_break_time': 5,
        'long_break_time': 15,
        'buffer_length': 4
    }


def test_run_interval_given_interval_time_when_run_then_it_should_take_the_previewed_duration_to_run():
    before = datetime.now()
    start = run(1, 'pomodoro')
    after = datetime.now()
    assert start > before
    assert after > start
    duration = after - start
    assert duration.seconds == 1


def test_run_pomodoro_given_pomodoro_execution_when_executed_then_shows_message_to_user(capfd):
    run(1, 'pomodoro')
    out, err = capfd.readouterr()
    assert out.replace('\n', '').startswith('Running focus time...')
    assert out.replace('\n', '').endswith('Focus time finished')


@pytest.mark.parametrize(
    'seconds, minutes',
    [
        (0, 0),
        (2, 120),
        (25, 1500)
    ]
)
def test_get_duration_given_duration_in_seconds_when_number_is_positive_or_zero_then_it_should_return_duration_in_minutes(seconds, minutes):
    assert get_duration(seconds) == minutes


@pytest.mark.parametrize(
    'seconds',
    [-1, -5, -25, -100000]
)
def test_get_duration_given_duration_in_seconds_when_number_is_negative_then_it_should_return_zero(seconds):
    assert get_duration(seconds) == 0


@pytest.mark.parametrize(
    'counter, expected_break, expected_duration',
    [
        (1, 'short_break', 5 * 60),
        (2, 'short_break', 5 * 60),
        (3, 'short_break', 5 * 60),
        (4, 'long_break', 15 * 60),
        (5, 'short_break', 5 * 60),
    ]
)
def test_get_next_break_given_a_pomodoro_cycle_it_should_return_the_proper_next_break(pomodoro_settings, counter, expected_break, expected_duration):
    next_break = get_next_break(counter, pomodoro_settings)
    assert next_break['description'] == expected_break
    assert next_break['duration'] == expected_duration
