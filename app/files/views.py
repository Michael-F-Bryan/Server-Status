from flask import (render_template, redirect, request, url_for, flash,
        current_app, send_from_directory)
from flask.ext.login import (login_required, current_user)
import os
from markdown import markdown

from .. import db
from . import files


@files.route('/', methods=['GET'])
@login_required
def file_system():
    # TODO: Using markdown to format the file tree feels like a massive hack
    # Should definitely find a better way to do it
    project_root = os.path.dirname(current_app.root_path)
    stuff = list_files(current_app.config['FILE_UPLOAD_FOLDER'])
    stuff = markdown(stuff)
    with open(os.path.join(project_root, 'tmp.txt'), 'w') as fp:
        fp.write(stuff)

    return render_template('files/file_system.html', 
            file_tree=stuff,
            project_root=project_root)


@files.route('/get/<path:filename>', methods=['GET'])
@login_required
def get_file(filename):
    return send_from_directory(current_app.config.get('FILE_UPLOAD_FOLDER'), 
        filename)

def list_files(startpath):
    tree = []
    indent_char = '\t'

    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = indent_char * (level)
        tree.append('{}* {}/'.format(indent, os.path.basename(root)))
        subindent = indent_char * (level + 1)
        for f in files:
            link = os.path.join(root, f).replace(startpath, '')
            link = url_for('files.get_file', filename=link[1:])
            tree.append('{}* [{}]({})'.format(subindent, f, link))

    return '\n'.join(tree)
