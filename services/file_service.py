import os
import fnmatch


def is_binary(file_path: str) -> bool:
    try:
        with open(file_path, "rb") as f:
            return b"\x00" in f.read(1024)
    except Exception:
        return True


def should_ignore(file_path: str, ignore_patterns: list[str], base_path: str) -> bool:
    rel_path = os.path.relpath(file_path, start=base_path)

    for pattern in ignore_patterns:
        pattern = pattern.strip()

        if pattern.endswith("/"):
            if pattern[:-1] in rel_path.split(os.sep):
                return True

        elif fnmatch.fnmatch(file_path, pattern) or fnmatch.fnmatch(rel_path, pattern):
            return True

        elif os.path.basename(file_path) == pattern:
            return True

    return False


def process_directory(path: str, ignore_patterns: list[str]) -> str:
    if not os.path.isdir(path):
        return "Diretório inválido."

    output = []

    for root, dirs, files in os.walk(path):
        dirs[:] = [
            d
            for d in dirs
            if not should_ignore(os.path.join(root, d), ignore_patterns, path)
        ]

        for file in files:
            full_path = os.path.join(root, file)

            if should_ignore(full_path, ignore_patterns, path):
                continue

            if is_binary(full_path):
                continue

            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    output.append(f"-- {full_path} --\n")
                    output.append(f.read())
                    output.append("\n\n")
            except Exception:
                continue

    return "".join(output) if output else "Nenhum arquivo encontrado."
