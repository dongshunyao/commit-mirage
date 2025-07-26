from subprocess import check_output


def get_commit_time(commit, dir="."):
    command = f"git show --no-patch --date=unix --format=%ad {commit}"
    return check_output(command, cwd=dir, encoding="utf-8", shell=True).strip()


def get_head_time(dir="."):
    return get_commit_time("HEAD", dir)


def get_head_hash(dir="."):
    command = "git rev-parse HEAD"
    return check_output(command, cwd=dir, encoding="utf-8", shell=True).strip()


def add_all(dir="."):
    command = "git add -A"
    return check_output(command, cwd=dir, encoding="utf-8", shell=True)


def commit_with_time(message, time, dir="."):
    command = f'git commit --message="{message}" --date="{time}"'
    return check_output(command, cwd=dir, encoding="utf-8", shell=True)

def commit_amend_with_time(time, dir="."):
    command = f'git commit --amend --no-edit --date="{time}"'
    return check_output(command, cwd=dir, encoding="utf-8", shell=True)

def check_dirty(dir="."):
    command = "git status --porcelain --ignore-submodules=dirty"
    return len(check_output(command, cwd=dir, encoding="utf-8", shell=True).strip()) > 0


def get_branch_name(dir="."):
    command = "git rev-parse --abbrev-ref HEAD"
    return check_output(command, cwd=dir, encoding="utf-8", shell=True).strip()


def new_branch(branch, commit, dir="."):
    command = f"git checkout -b {branch} {commit}"
    return check_output(command, cwd=dir, encoding="utf-8", shell=True)


def delete_branch(branch, dir="."):
    command = f"git branch -D {branch}"
    return check_output(command, cwd=dir, encoding="utf-8", shell=True)


def checkout(commit, dir="."):
    command = f"git commit {commit}"
    return check_output(command, cwd=dir, encoding="utf-8", shell=True)


def rebase(branch, target, dir="."):
    command = f"git rebase {branch} {target}"
    return check_output(command, cwd=dir, encoding="utf-8", shell=True)


def diff(old, new, dir="."):
    command = f"git diff {old} {new}"
    return check_output(command, cwd=dir, encoding="utf-8", shell=True)

def apply_reverse(patch, dir="."):
    command = "git apply -R"
    return check_output(command, stdin=patch, cwd=dir, encoding="utf-8", shell=True)
