
def _read_file(file_path: str) -> str:
    with open(file_path) as f:
        ret = f.read()
    return ret