from pathlib import Path

DEPENDENCY_FILES = [
    "requirements.txt",
    "pyproject.toml",
    "package.json",
]

def find_dependency(repo_path: Path) -> list[Path]:
    dependency_files = []

    for filename in DEPENDENCY_FILES:
        for file in repo_path.rglob(filename):
            dependency_files.append(file)

    print(dependency_files)
    return dependency_files