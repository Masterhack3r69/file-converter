import os
import pathspec

def load_gitignore_spec(root_dir):
    """
    Loads .gitignore patterns from the root directory and returns a PathSpec object.
    """
    gitignore_path = os.path.join(root_dir, '.gitignore')
    patterns = []
    
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            patterns = f.read().splitlines()
            
    # Always ignore .git directory and common temporary files
    patterns.extend(['.git/', '__pycache__/', '*.pyc', '*.pdf'])
    
    return pathspec.PathSpec.from_lines('gitwildmatch', patterns)

def is_ignored(file_path, root_dir, spec):
    """
    Checks if a file path is ignored by the spec.
    file_path: Absolute path to the file.
    root_dir: Absolute path to the root directory.
    spec: PathSpec object.
    """
    if spec is None:
        return False
        
    # Get relative path for matching
    rel_path = os.path.relpath(file_path, root_dir)
    return spec.match_file(rel_path)
