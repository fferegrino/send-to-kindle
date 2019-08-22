from pathlib import Path
from subprocess import run

def html_to_mobi(input_path, file_name):
    kindlegen_path = Path("kindlegen")
    new_env = {
        'PATH': str(kindlegen_path.resolve())
    }
    result =  run(["kindlegen", "-o", f"{file_name}.mobi", str(input_path.resolve())], env = new_env)
    if not result.returncode == 0 and not result.returncode == 1:
        raise ValueError()

    return Path(input_path.parent,f"{file_name}.mobi" )

