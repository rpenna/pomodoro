import pytest
import pomodoro
from exceptions.stop_pomodoro_exception import StopPomodoroException


def test_given_wait_user_input_status_when_user_type_r_then_wait_for_permission_to_run_funcion_returns_none(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda: 'r')
    result = pomodoro.wait_for_permission_to_run()
    assert result is None


def test_given_wait_user_input_status_when_user_type_run_then_wait_for_permission_to_run_funcion_returns_none(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda: 'run')
    result = pomodoro.wait_for_permission_to_run()
    assert result is None


def test_given_wait_user_input_status_when_user_type_s_then_wait_for_permission_to_run_funcion_raises_exception(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda: 's')
    with pytest.raises(StopPomodoroException):
        pomodoro.wait_for_permission_to_run()


def test_given_wait_user_input_status_when_user_type_stop_then_wait_for_permission_to_run_funcion_raises_exception(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda: 'stop')
    with pytest.raises(StopPomodoroException):
        pomodoro.wait_for_permission_to_run()
