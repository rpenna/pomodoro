from datetime import datetime
from pomodoro import run_focus_time, run_break


def test_run_pomodoro_given_pomodoro_time_when_run_then_it_should_take_the_time_duration_to_run():
    before = datetime.now()
    start = run_focus_time(1)
    after = datetime.now()
    assert start > before
    assert after > start
    duration = after - start
    assert duration.seconds == 1

def test_run_break_given_break_time_when_run_then_it_should_take_the_time_duration_to_run():
    before = datetime.now()
    start = run_break(1)
    after = datetime.now()
    assert start > before
    assert after > start
    duration = after - start
    assert duration.seconds == 1

def test_run_pomodoro_given_pomodoro_execution_when_executed_then_shows_message_to_user(capfd):
    run_focus_time(1)
    out, err = capfd.readouterr()
    assert out.replace('\n', '').startswith('Running pomodoro...')
    assert out.replace('\n', '').endswith('Pomodoro finished')

def test_run_break_given_break_execution_when_executed_then_shows_message_to_user(capfd):
    run_break(1)
    out, err = capfd.readouterr()
    message = out.replace('\n', '')
    assert message.startswith('Running break...')
    assert message.endswith('Break finished')
