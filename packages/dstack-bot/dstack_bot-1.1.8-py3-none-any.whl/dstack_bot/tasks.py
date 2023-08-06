import glob
import os

from invoke import run

from dstack_bot.utils import get_env


def cleanup(glob_pattern='*'):
    path = get_env('LOCAL_BACKUP_PATH')
    backups = sorted(glob.glob(f'{path}/{glob_pattern}'), key=os.path.getctime)
    # backups = sorted(os.listdir(path), key=lambda f: os.path.getctime(f'{path}/{f}'))
    backups.reverse()
    while len(backups) > 2:
        run(f'rm -f {backups.pop()}')
