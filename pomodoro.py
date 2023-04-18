import time
from argparse import Namespace, ArgumentParser
from datetime import datetime
from exceptions.stop_pomodoro_exception import StopPomodoroException


def get_args() -> ArgumentParser:
    """Read arguments and define pomodoro settings.

    Returns:
        ArgumentParser: pomodoro settings
    """
    ...


def wait_for_permission_to_run() -> None:
    """Print possible commands and wait for user's input.

    Raises:
        StopPomodoroException: raised when user wants to end pomodoro
        execution.
    """
    print(
        """
        Type next step: "r" or "run" to run, "s" or "stop" to exit pomodoro
        """
    )
    step = input()
    if step.lower() in ('stop', 's'):
        raise StopPomodoroException


def run_focus_time(pomodoro_time: int) -> datetime:
    """Run focus time (pomodoro), showing progression bar and pomodoro stats.

    Args:
        pomodoro_time (int): Pomodoro duration (seconds)

    Returns:
        datetime: pomodoro start time
    """
    print('Running pomodoro...')
    start_time = datetime.now()
    time.sleep(pomodoro_time)
    print('Pomodoro finished')
    return start_time


def record_progress(finished_pomodoros: int, start_time: datetime) -> None:
    """Save pomodoro stats

    Args:
        finished_pomodoros (int): number of pomodoros finished
        start_time (datetime): start time of last pomodoro runned
    """
    ...


def get_break_duration(
    finished_pomodoros: int,
    pomodoro_settings: dict
) -> int:
    """Calculates next break duration

    Args:
        finished_pomodoros (int): number of finished pomodoros
        pomodoro_settings (dict): pomodoro settings (needs buffer length and
        breaks duration)

    Returns:
        int: next break duration (seconds)
    """
    ...


def run_break(break_time: int) -> None:
    """Run break, showing progress bar and pomodoro stats

    Args:
        break_time (int): break length in seconds
    """
    print('Running break...')
    start_time = datetime.now()
    time.sleep(break_time)
    print('Break finished')
    return start_time


def show_progress(pomodoro_settings: dict, finished_pomodoros: int) -> None:
    """Print pomodoro stats

    Args:
        pomodoro_settings (dict): Pomodoro settings (use all of them)
        finished_pomodoros (int): number of finished pomodoros
    """
    ...


def start_pomodoro_counter(pomodoro_settings: dict) -> None:
    finished_pomodoros = 0
    quit_pomodoro = False
    try:
        while not quit_pomodoro:
            wait_for_permission_to_run()
            start_time = run_focus_time(pomodoro_settings['pomodoro_time'])
            finished_pomodoros += 1
            break_duration = get_break_duration(
                finished_pomodoros,
                pomodoro_settings,
            )
            record_progress(finished_pomodoros, start_time)
            wait_for_permission_to_run()
            run_break(break_duration)
    except (StopPomodoroException, KeyboardInterrupt):
        show_progress(pomodoro_settings)


if __name__ == '__main__':
    args = get_args()
    pomodoro_settings = {
        'pomodoro_time': args.pt,
        'short_break_time': args.sbt,
        'long_break_time': args.lbt,
        'buffer_length': args.bl
    }
    start_pomodoro_counter(pomodoro_settings)
