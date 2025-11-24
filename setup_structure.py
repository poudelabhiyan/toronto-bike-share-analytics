from pathlib import Path

# Base directory: the folder where this script is saved
BASE_DIR = Path(__file__).parent

def create_file(path: Path, content: str = "") -> None:
    """
    Create a file at 'path' with the given content.
    If the file already exists, it will NOT be overwritten.
    """
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"Created: {path}")
    else:
        print(f"Exists, skipped: {path}")

def main() -> None:
    # 1. src package
    create_file(BASE_DIR / "src" / "__init__.py", "# src package\n")

    # 2. data_processing package and modules
    create_file(BASE_DIR / "src" / "data_processing" / "__init__.py", "# data processing package\n")
    create_file(BASE_DIR / "src" / "data_processing" / "load.py", "# functions for loading data\n")
    create_file(BASE_DIR / "src" / "data_processing" / "clean.py", "# functions for cleaning data\n")
    create_file(BASE_DIR / "src" / "data_processing" / "summary.py", "# functions for summary statistics\n")
    create_file(BASE_DIR / "src" / "data_processing" / "visualize.py", "# functions for visualizations\n")

    # 3. tests package and test modules
    create_file(BASE_DIR / "tests" / "__init__.py", "# tests package\n")
    create_file(BASE_DIR / "tests" / "test_load.py", "# tests for load functions\n")
    create_file(BASE_DIR / "tests" / "test_clean.py", "# tests for clean functions\n")
    create_file(BASE_DIR / "tests" / "test_summary.py", "# tests for summary statistics\n")
    create_file(BASE_DIR / "tests" / "test_visualize.py", "# tests for visualizations\n")

    # 4. dashboard folder
    create_file(BASE_DIR / "dashboard" / "app.py", "# Streamlit dashboard entry point\n")

    # 5. docs folder
    create_file(BASE_DIR / "docs" / "README.md", "# Project documentation\n")

    # 6. Basic README content if README.md exists but is empty
    readme_path = BASE_DIR / "README.md"
    if readme_path.exists():
        content = readme_path.read_text(encoding="utf-8").strip()
        if not content:
            readme_path.write_text(
                "# Toronto Bike Analytics Tool\n\n"
                "This project analyzes Toronto Bike-Sharing data using Agile development, "
                "TDD, refactoring, and a simple dashboard.\n\n"
                "## How to run\n\n"
                "pip install -r requirements.txt\n\n"
                "## How to test\n\n"
                "pytest\n",
                encoding="utf-8",
            )
            print("Updated README.md with basic content.")
        else:
            print("README.md already has content, left unchanged.")
    else:
        # If no README exists (just in case)
        create_file(
            readme_path,
            "# Toronto Bike Analytics Tool\n\n"
            "This project analyzes Toronto Bike-Sharing data using Agile development, "
            "TDD, refactoring, and a simple dashboard.\n\n"
            "## How to run\n\n"
            "pip install -r requirements.txt\n\n"
            "## How to test\n\n"
            "pytest\n",
        )

if __name__ == "__main__":
    main()
