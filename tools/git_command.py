import bpy
import subprocess
import traceback
from .utilidades import save_mainfile

def get_global_params(p):
    try:
        return subprocess.check_output(['git', 'config', '--global', '--get', f'user.{p}']).decode().strip(), True
    except subprocess.CalledProcessError as e:
        print(f'Error al obtener parámetros globales: {e.output}')
        traceback.print_exc()
        return "", False

def set_global_params(p, v):
    try:
        subprocess.check_output(['git', 'config', '--global', f'user.{p}', v])
        return True
    except subprocess.CalledProcessError as e:
        print(f'Error al establecer parámetros globales: {e.output}')
        traceback.print_exc()
        return False


def git_init(cwd):
    try:
        subprocess.check_output(['git','init'], cwd=cwd)
        return True
    except subprocess.CalledProcessError as e:
        print('Error: ', e.output)
        traceback.print_exc()
        return False
    
    

def git_add(cwd):
    try:
        subprocess.check_output(['git','add', "."], cwd=cwd)
        return True
    except subprocess.CalledProcessError as e:
        print('Error: ', e.output)
        traceback.print_exc()
        return False
    

def git_commit(cwd, message):
    try:
        if bpy.context.scene.commits.has_ramas():
            bpy.context.scene.branch = "0"
            bpy.context.scene.commits.clear()  

        if not save_mainfile():
            return False

        if not git_add(cwd):
            return False
    
        subprocess.check_output(['git','commit', '-m', message], cwd=cwd)
        return True
    except subprocess.CalledProcessError as e:
        print('Error: ', e.output)
        traceback.print_exc()
        return False
    

def load_commits(cwd):
    try:
        count = subprocess.check_output(['git', 'rev-list', '--all', '--count'], cwd=cwd).decode().strip()
        if int(count) > 0:
            cmd = ['git', 'log', '--pretty=format:"%h": {"commit": "%h", "parent": "%p", "refs": "%D", "subject": "%s"},', '--reflog']
            commits = subprocess.check_output(cmd, cwd=cwd).decode().strip()
            bpy.context.scene.commits.add_commits(commits)
    except subprocess.CalledProcessError as e:
        print(f'Error al cargar commits: {e.output}')
        traceback.print_exc()


def git_select_version(id, cwd):
    try:
        subprocess.check_output(['git', 'reset', '--hard', id], cwd=cwd)
        bpy.ops.wm.revert_mainfile()
        bpy.context.scene.commits.clear()
    except subprocess.CalledProcessError as e:
        print(f'Error al seleccionar versión: {e.output}')
        traceback.print_exc()

def git_status(cwd):
    try:
        return subprocess.check_output(['git', 'status', '-s'], cwd=cwd).decode().strip(), True
    except subprocess.CalledProcessError as e:
        print('Error: ', e.output)
        traceback.print_exc()
        return "", False
