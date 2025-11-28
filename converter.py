import os
from reportlab.lib.pagesizes import A4, LETTER, LEGAL
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Preformatted
from reportlab.lib.units import inch
from reportlab.lib import colors
from utils import load_gitignore_spec, is_ignored

PAGE_SIZES = {
    'A4': A4,
    'LETTER': LETTER,
    'LEGAL': LEGAL
}

class CodebaseToPDF:
    def __init__(self, root_dir, output_file, font_size=10, page_size_name='A4', margin=1.0, author="Author"):
        self.root_dir = os.path.abspath(root_dir)
        self.output_file = output_file
        self.font_size = font_size
        self.page_size = PAGE_SIZES.get(page_size_name.upper(), A4)
        self.margin = margin * inch
        self.author = author
        self.spec = load_gitignore_spec(self.root_dir)
        
        self.styles = getSampleStyleSheet()
        self._setup_styles()

    def _setup_styles(self):
        # Custom styles based on the user's request
        self.styles.add(ParagraphStyle(
            name='CodeContent',
            parent=self.styles['Code'],
            fontSize=self.font_size,
            leading=self.font_size * 1.2,
            fontName='Courier',
            spaceAfter=10,
        ))
        
        self.styles.add(ParagraphStyle(
            name='FolderHeading',
            parent=self.styles['Normal'],
            fontSize=self.font_size + 2,
            fontName='Helvetica-Bold',
            spaceBefore=10,
            spaceAfter=5,
            textColor=colors.black
        ))

        self.styles.add(ParagraphStyle(
            name='FileHeading',
            parent=self.styles['Normal'],
            fontSize=self.font_size + 1,
            fontName='Helvetica-Oblique',
            spaceBefore=5,
            spaceAfter=2,
            textColor=colors.black
        ))
        
        self.styles.add(ParagraphStyle(
            name='RootTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=20,
            alignment=0 # Left
        ))
        
        self.styles.add(ParagraphStyle(
            name='MetaInfo',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=6,
        ))

    def generate(self):
        doc = SimpleDocTemplate(
            self.output_file,
            pagesize=self.page_size,
            rightMargin=self.margin,
            leftMargin=self.margin,
            topMargin=self.margin,
            bottomMargin=self.margin
        )
        
        story = []
        
        # Add Header Info
        root_name = os.path.basename(self.root_dir)
        story.append(Paragraph(f"{root_name.upper()}", self.styles['RootTitle']))
        story.append(Paragraph(f"Author: {self.author}", self.styles['MetaInfo']))
        
        import datetime
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        story.append(Paragraph(f"Date: {date_str}", self.styles['MetaInfo']))
        story.append(Spacer(1, 20))
        
        # Traverse directory
        self._process_directory(self.root_dir, story)
        
        doc.build(story)
        print(f"PDF generated successfully: {self.output_file}")

    def _process_directory(self, current_dir, story):
        # Sort directories and files for consistent order
        try:
            items = sorted(os.listdir(current_dir))
        except PermissionError:
            return

        # Separate dirs and files
        dirs = []
        files = []
        
        for item in items:
            full_path = os.path.join(current_dir, item)
            if is_ignored(full_path, self.root_dir, self.spec):
                continue
                
            if os.path.isdir(full_path):
                dirs.append(item)
            else:
                files.append(item)
        
        # Process current directory files first (or folders first? User image shows Folder1 then files inside)
        # The user image shows:
        # - Folder1
        # - file name1.1
        # Codes...
        #
        # This implies a depth-first traversal where we print the folder name, then its contents.
        
        # However, to represent the structure clearly in a flat PDF, indentation or breadcrumbs are usually good.
        # Given the simple request: "Root -> Folder -> File", I will just print the Folder Name when I enter it.
        
        # If this is the root dir, we don't print it again as it's the title.
        if current_dir != self.root_dir:
            rel_path = os.path.relpath(current_dir, self.root_dir)
            # Use dashes to represent depth or just the folder name
            # User image: "- Folder1"
            depth = rel_path.count(os.sep)
            indent = "&nbsp;" * (depth * 4)
            story.append(Paragraph(f"{indent}— {os.path.basename(current_dir)}", self.styles['FolderHeading']))

        # Process Files in this directory
        for f in files:
            self._add_file_content(os.path.join(current_dir, f), story, current_dir)

        # Recurse into subdirectories
        for d in dirs:
            self._process_directory(os.path.join(current_dir, d), story)

    def _add_file_content(self, file_path, story, current_dir):
        rel_path = os.path.relpath(file_path, self.root_dir)
        filename = os.path.basename(file_path)
        
        # Calculate indentation based on depth
        # If file is in root, depth is 0. If in Folder1, depth is 1.
        depth = rel_path.count(os.sep)
        indent = "&nbsp;" * (depth * 4)
        
        story.append(Paragraph(f"{indent}— {filename}", self.styles['FileHeading']))
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
                
            # Wrap code in Preformatted or Paragraph with Courier
            # Preformatted is better for code to preserve whitespace
            # We need to handle very long lines or large files? 
            # For now, simple Preformatted.
            
            # Escape XML characters for ReportLab
            from xml.sax.saxutils import escape
            content = escape(content)
            
            # Split into lines to avoid super long blocks if needed, but Preformatted handles newlines.
            # We might want to limit font size for code.
            
            story.append(Preformatted(content, self.styles['CodeContent']))
            story.append(Spacer(1, 10))
            
        except Exception as e:
            story.append(Paragraph(f"[Error reading file: {e}]", self.styles['Normal']))
