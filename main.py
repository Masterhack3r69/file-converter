import argparse
import os
from converter import CodebaseToPDF

def main():
    parser = argparse.ArgumentParser(description="Convert codebase to PDF.")
    parser.add_argument("root_dir", help="Path to the codebase root directory")
    parser.add_argument("--output", "-o", default="codebase.pdf", help="Output PDF filename")
    parser.add_argument("--font-size", "-f", type=int, default=10, help="Font size for code")
    parser.add_argument("--page-size", "-p", default="A4", help="Page size (A4, LETTER, LEGAL)")
    parser.add_argument("--margin", "-m", type=float, default=1.0, help="Page margin in inches")
    parser.add_argument("--author", "-a", default="Author", help="Author name for the PDF")

    args = parser.parse_args()

    if not os.path.exists(args.root_dir):
        print(f"Error: Directory '{args.root_dir}' does not exist.")
        return

    converter = CodebaseToPDF(
        root_dir=args.root_dir,
        output_file=args.output,
        font_size=args.font_size,
        page_size_name=args.page_size,
        margin=args.margin,
        author=args.author
    )
    
    print(f"Starting conversion for: {args.root_dir}")
    converter.generate()

if __name__ == "__main__":
    main()
