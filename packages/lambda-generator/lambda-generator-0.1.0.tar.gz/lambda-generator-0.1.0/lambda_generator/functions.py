import os
from distutils.dir_util import copy_tree


def create_lambda(template_path: str, project_path: str):
    create_project_dir(project_path)
    copy_tree(template_path, project_path)


def create_project_dir(path: str):
    if not os.path.isdir(path):
        os.mkdir(path)
