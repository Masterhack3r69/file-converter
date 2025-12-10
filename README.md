# Codebase to PDF Converter

A Python tool to convert a codebase (folder structure and files) into a single, well-formatted PDF document. This is useful for archiving code, sharing code snippets in a readable format, or reviewing code offline.

## Features

- **Recursive Scanning**: Traverses all subdirectories.
- **Gitignore Support**: Respects `.gitignore` rules to exclude unwanted files (like `node_modules`, `venv`, etc.).
- **Customizable**:
  - Font size
  - Page size (A4, Letter, Legal)
  - Margins
  - Author name
- **Clean Formatting**: Generates a structured PDF with folder hierarchy and syntax-highlighted-style code blocks.

## Installation

1.  **Clone the repository**:

    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the `main.py` script with the target directory path.

```bash
python main.py <path_to_codebase> [options]
```

### Examples

**Basic Usage:**

```bash
python main.py ./my_project
```

This will generate `codebase.pdf` in the current directory.

**Custom Output and Author:**

```bash
python main.py ./my_project --output my_project_v1.pdf --author "Jane Doe"
```

**Adjusting Formatting:**

```bash
python main.py ./src --font-size 8 --page-size LETTER --margin 0.5
```

### Options

- `root_dir`: (Required) Path to the codebase root directory.
- `--output`, `-o`: Output PDF filename (default: `codebase.pdf`).
- `--font-size`, `-f`: Font size for code content (default: 10).
- `--page-size`, `-p`: Page size: `A4`, `LETTER`, `LEGAL` (default: `A4`).
- `--margin`, `-m`: Page margin in inches (default: 1.0).
- `--author`, `-a`: Author name to appear in the header (default: "Author").

## Requirements

- Python 3.x
- `reportlab`
- `pathspec`

![alt text](image.png)