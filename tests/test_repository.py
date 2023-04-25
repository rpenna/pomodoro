import copy
import pytest
from datetime import datetime, timedelta
from repository.pomodoro_repository import PomodoroRepository


@pytest.fixture
def setup_repo():
    return PomodoroRepository('test')


@pytest.fixture
def repo_controller(setup_repo):
    yield setup_repo
    setup_repo.teardown()


@pytest.fixture
def pomodoro_info():
    return {
        'start_time': datetime(2023, 1, 1, 12),
        'end_time': datetime(2023, 1, 1, 12, 25)
    }


def test_generate_new_pomodoro_given_a_new_pomodoro_when_inserted_then_it_should_generate_a_new_pomodoro_id(repo_controller):
    repo = repo_controller
    pomodoro_id = repo.generate_new_pomodoro()
    assert pomodoro_id > 0


def test_save_pomodoro_given_a_pomodoro_when_saved_then_it_should_save_a_new_line_into_database(repo_controller, pomodoro_info):
    repo = repo_controller
    pomodoro_id = repo.generate_new_pomodoro()
    repo.save_pomodoro(pomodoro_id, pomodoro_info)
    pomodoros = repo.get_pomodoros(pomodoro_id)
    assert pomodoros[-1].pomodoro_id == pomodoro_id
    assert pomodoros[-1].start_time == pomodoro_info['start_time']
    assert pomodoros[-1].end_time == pomodoro_info['end_time']


@pytest.mark.parametrize(
    'quantity',
    [
        (0),
        (1),
        (5),
        (10),
        (20),
    ]
)
def test_save_pomodoro_given_a_quantity_of_pomodoro_executed_when_get_pomodoros_the_it_should_return_the_same_quantity_of_pomodoros_executed(repo_controller, pomodoro_info, quantity):
    info = copy.deepcopy(pomodoro_info)
    repo = repo_controller
    pomodoro_id = repo.generate_new_pomodoro()
    for _ in range(quantity):
        info['start_time'] += timedelta(minutes=25)
        info['end_time'] += timedelta(minutes=25)
        repo.save_pomodoro(pomodoro_id, info)
    pomodoros = repo.get_pomodoros(pomodoro_id)
    assert len(pomodoros) == quantity
