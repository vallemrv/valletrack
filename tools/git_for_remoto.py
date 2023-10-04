import subprocess
import traceback


def git_fetch(cwd):
    try:
        subprocess.check_output(['git', 'fetch'], cwd=cwd)
        return True
    except subprocess.CalledProcessError as e:
        print('Error: ', e.output)
        traceback.print_exc()
        return False

def git_local_head(cwd):
    try:
        head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=cwd).decode().strip()
        return head, True
    except subprocess.CalledProcessError as e:
        print('Error: ', e.output)
        traceback.print_exc()
        return "", False

def git_remote_head(cwd, branch='master'):
    try:
        head = subprocess.check_output(['git', 'rev-parse', f'origin/{branch}'], cwd=cwd).decode().strip()
        return head, True
    except subprocess.CalledProcessError as e:
        print('Error: ', e.output)
        traceback.print_exc()
        return "", False

def git_has_uncommitted_changes(cwd):
    try:
        status = subprocess.check_output(['git', 'status', '--porcelain'], cwd=cwd).decode().strip()
        return bool(status), True
    except subprocess.CalledProcessError as e:
        print('Error: ', e.output)
        traceback.print_exc()
        return False, False

def git_need_to_push_or_pull(cwd, branch='master'):
    local_head, lh_success = git_local_head(cwd)
    remote_head, rh_success = git_remote_head(cwd, branch)
    if lh_success and rh_success:
        return local_head != remote_head, True
    return False, False
