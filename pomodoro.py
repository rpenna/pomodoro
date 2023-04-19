import time
from argparse import Namespace, ArgumentParser
from datetime import datetime
from tqdm import tqdm
from exceptions.stop_pomodoro_exception import StopPomodoroException


def get_args() -> Namespace:
    """Read arguments and define pomodoro settings.

    Returns:
        ArgumentParser: pomodoro settings
    """
    parser = ArgumentParser(
        description='Command line pomodoro execution'
    )
    parser.add_argument(
        '-pt',
        default=25,
        type=int,
        help='Pomodoro time: focus time duration (in minutes)'
    )
    parser.add_argument(
        '-sbt',
        default=5,
        type=int,
        help='Short break time: short break durantion (in minutes)'
    )
    parser.add_argument(
        '-lbt',
        default=15,
        type=int,
        help='Long break time: long break duration (in minutes)'
    )
    parser.add_argument(
        '-bl',
        default=4,
        type=int,
        help='Buffer length: number of pomodoros cycles until long break'
    )
    return parser.parse_args()


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


def sleep_with_progress_bar(sleep_time: float, description: str = '') -> None:
    """Show progress bar to user

    Args:
        sleep_time (float): progress duration in seconds
        description (str, optional): Description of what is running. Defaults to ''.
    """
    minutes = str(sleep_time // 60).zfill(2)
    seconds = str(sleep_time % 60).zfill(2)
    bar_format = '{l_bar}{bar:30}| [{elapsed}/%s:%s]' % (minutes, seconds)
    for _ in tqdm(range(sleep_time), desc=description, bar_format=bar_format):
        time.sleep(1)


def run_focus_time(pomodoro_time: int) -> datetime:
    """Run focus time (pomodoro), showing progression bar and pomodoro stats.

    Args:
        pomodoro_time (int): Pomodoro duration (minutes)

    Returns:
        datetime: pomodoro start time
    """
    print('Running pomodoro...')
    one_percent_interval = (pomodoro_time * 60)
    start_time = datetime.now()
    sleep_with_progress_bar(one_percent_interval)
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
        break_time (int): break duration in minutes
    """
    print('Running break...')
    one_percent_interval = (break_time * 60)
    start_time = datetime.now()
    sleep_with_progress_bar(one_percent_interval)
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
        show_progress(pomodoro_settings, finished_pomodoros)


if __name__ == '__main__':
    args = get_args()
    pomodoro_settings = {
        'pomodoro_time': args.pt,
        'short_break_time': args.sbt,
        'long_break_time': args.lbt,
        'buffer_length': args.bl
    }
    start_pomodoro_counter(pomodoro_settings)
