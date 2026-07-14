from pathlib import Path

LANGUAGE_FILES = {
    "Python": ["requirements.txt", "pyproject.toml", "setup.py"],
    "Javascript": ["package.json"],
    "Java": ["pom.xml", "build.gradle"],
    "Rust": ["Cargo.toml"],
    "Go": ["go.mod"]
}

def detect_language(repo_path: Path):
    for language, files in LANGUAGE_FILES.items():
        for file in files:
            if (repo_path / file).exists():
                return language
    return "unknown"