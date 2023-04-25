import time
from argparse import Namespace, ArgumentParser
from datetime import datetime
from plyer import notification
from plyer.utils import platform
from tqdm import tqdm
from exceptions.stop_pomodoro_exception import StopPomodoroException


DESCRIPTIONS = {
    'pomodoro': 'Focus time',
    'long_break': 'Long break',
    'short_break': 'Short break'
}


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
    bar_format = '{l_bar}{bar:50}| [{elapsed}/%s:%s]' % (minutes, seconds)
    for _ in tqdm(range(sleep_time), desc=description, bar_format=bar_format):
        time.sleep(1)


def run(interval: int, type: str) -> datetime:
    """Run focus time (pomodoro), showing progression bar and stats.

    Args:
        pomodoro_time (int): Pomodoro duration (seconds)

    Returns:
        datetime: pomodoro start time
    """
    description = DESCRIPTIONS[type]
    print(f'Running {description.lower()}...')
    start_time = datetime.now()
    sleep_with_progress_bar(interval, description)
    print(f'{description} finished')
    return start_time


def show_notification(message: str) -> None:
    """show pop up notification for windows

    Args:
        message (str): Message to be shown
    """
    extension = 'ico' if platform == 'win' else 'png'
    
    notification.notify(
        title='Pomodoro',
        message=message,
        app_name='Pomodoro',
        app_icon=f'./img/tomato.{extension}'
    )


def record_progress(finished_pomodoros: int, start_time: datetime) -> None:
    """Save pomodoro stats

    Args:
        finished_pomodoros (int): number of pomodoros finished
        start_time (datetime): start time of last pomodoro runned
    """
    ...


def show_progress(pomodoro_settings: dict, finished_pomodoros: int) -> None:
    """Print pomodoro stats

    Args:
        pomodoro_settings (dict): Pomodoro settings (use all of them)
        finished_pomodoros (int): number of finished pomodoros
    """
    ...


def get_duration(seconds: int) -> int:
    """Convert seconds to minutes.

    Args:
        seconds (int): seconds to be converted

    Returns:
        int: result in minutes
    """
    return 0 if seconds < 0 else seconds * 60


def get_next_break(counter: int, settings: dict) -> dict:
    """Define the next break according to number of pomodoros finished and
    settings defined by user.

    Args:
        counter (int): number of pomodoros finished
        settings (dict): pomodoro settings

    Returns:
        dict: description and duration of next break
    """
    if counter % settings['buffer_length'] == 0:
        return {
            'description': 'long_break',
            'duration': get_duration(settings['long_break_time'])
        }
    return {
        'description': 'short_break',
        'duration': get_duration(settings['short_break_time'])
    }


def start_pomodoro_counter(pomodoro_settings: dict) -> None:
    finished_pomodoros = 0
    quit_pomodoro = False
    focus_duration = get_duration(pomodoro_settings['pomodoro_time'])
    try:
        while not quit_pomodoro:
            wait_for_permission_to_run()
            start_time = run(focus_duration, 'pomodoro')
            show_notification('Time to take a break :)')
            finished_pomodoros += 1
            record_progress(finished_pomodoros, start_time)
            next_break = get_next_break(
                finished_pomodoros,
                pomodoro_settings,
            )
            wait_for_permission_to_run()
            run(next_break['duration'], next_break['description'])
            show_notification('Time to focus!')
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
