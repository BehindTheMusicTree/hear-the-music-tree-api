import os
from pathlib import Path

import dotenv

from api.utils.utils import print_django


def load_required_str_env_var(var_name: str, must_print_value: bool = True, *, silent: bool = False) -> str:
    var_value = os.getenv(var_name)
    if var_value is None or var_value == "":
        raise OSError(f"The {var_name} environment variable must be set and non-empty")
    if silent:
        return var_value
    if must_print_value:
        print_django(f"{var_name}: {var_value}")
    else:
        print_django(f"{var_name} is set.")
    return var_value


def load_optional_str_env_var(var_name: str, default: str = "") -> str:
    var_value = os.getenv(var_name)
    return var_value if var_value is not None and var_value != "" else default


def load_optional_secret_env_var(var_name: str, default: str = "") -> str:
    var_value = load_optional_str_env_var(var_name, default)
    if var_value and var_value.startswith('"') and var_value.endswith('"'):
        return var_value[1:-1]
    return var_value


def load_required_bool_env_var(var_name: str) -> bool:
    raw = os.getenv(var_name)
    if raw is None or raw == "":
        raise OSError(f"The {var_name} environment variable must be set and non-empty")
    lower = raw.strip().lower()
    if lower not in ("true", "false"):
        raise OSError(f"The {var_name} environment variable must be 'true' or 'false', got '{raw}'")
    result = lower == "true"
    print_django(f"{var_name}: {result}")
    return result


def load_required_int_env_var(var_name: str) -> int:
    var_value = load_required_str_env_var(var_name)
    try:
        return int(var_value)
    except ValueError as e:
        raise OSError(f"The {var_name} environment variable must be an integer, got '{var_value}'") from e


def load_required_path_env_var(var_name: str, must_print_value: bool = True) -> Path:
    path = Path(load_required_str_env_var(var_name))
    if not path.exists():
        raise OSError(f"The path {path} does not exist")
    print_django(f"The path {path} exists on the system.")
    return path


def load_calculated_env_paths(base_dir: Path):
    calculated_paths_env_file = base_dir / "env/calculated_paths/.env"
    load_env_vars_from_file_if_exists(calculated_paths_env_file)


def load_env_vars_from_file_if_exists(env_file_path: Path):
    if not env_file_path.exists():
        print_django(f"No env file at {env_file_path}")
    else:
        print_django(f"Env file provided at {env_file_path} . Loading...")
        dotenv.load_dotenv(env_file_path)
        print_django("Env file loaded.")


def load_required_secret_env_var(var_name: str, *, silent: bool = False) -> str:
    var_value = load_required_str_env_var(var_name, must_print_value=False, silent=silent)
    if var_value.startswith('"') and var_value.endswith('"'):
        return var_value[1:-1]
    return var_value
