import os

solution_dir_path = os.path.dirname(os.path.realpath('__file__'))

# join - make path compatible with any OS:
downloads_dir_path = os.path.join(solution_dir_path, 'downloads')
exports_dir_path = os.path.join(solution_dir_path, 'exports')
resources_dir_path = os.path.join(solution_dir_path, 'resources')
src_directory = os.path.join(solution_dir_path, 'src')
