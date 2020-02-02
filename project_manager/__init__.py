import os
from pathlib import Path

CONFIG_BASE_DIR = os.getenv('XDG_CONFIG_HOME') or Path.home() / '.config'
CONFIG = Path(CONFIG_BASE_DIR) / 'pm'
PROJECT_CONFIG_DIR = CONFIG / 'projects'

PROJECT_CONFIG_DIR.mkdir(parents=True, exist_ok=True)

ACTIVATE_SHELL_VAR = '_P_CURRENT_PROJECT'
