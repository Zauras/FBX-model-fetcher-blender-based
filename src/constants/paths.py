import os

solution_dir_path = os.path.dirname(os.path.realpath('__file__'))

# join - make path compatible with any OS:
downloads_dir_path = os.path.join(solution_dir_path, 'downloads')
resources_dir_path = os.path.join(solution_dir_path, 'resources')
imports_dir_path = os.path.join(resources_dir_path, 'imports')
exports_dir_path = os.path.join(solution_dir_path, 'exports')
src_directory = os.path.join(solution_dir_path, 'src')
