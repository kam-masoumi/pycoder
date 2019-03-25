from subprocess import Popen, PIPE
from os import path


class Git:
    def __init__(self, repository=None):
        self.repository = repository+'/'

    def status(self):
        git_command = ['git', 'status']
        repository = path.dirname(self.repository)

        git_query = Popen(git_command, cwd=repository, stdout=PIPE, stderr=PIPE)
        (git_status, error) = git_query.communicate()

        if git_query.poll() == 0:
            return git_status.decode()

        return error.decode()

    def diff(self):
        git_command = ['git', 'diff']
        repository = path.dirname(self.repository)

        git_query = Popen(git_command, cwd=repository, stdout=PIPE, stderr=PIPE)
        (git_status, error) = git_query.communicate()

        if git_query.poll() == 0:
            return git_status.decode()

        return error.decode()

    def commit(self, message):
        git_command = ['git', 'commit', '-am', f'"{message}"']
        repository = path.dirname(self.repository)

        git_query = Popen(git_command, cwd=repository, stdout=PIPE, stderr=PIPE)
        (git_status, error) = git_query.communicate()

        if git_query.poll() == 0:
            return git_status.decode()

        return error.decode()

    def push(self, branch_name):
        git_command = ['git', 'push', 'origin', f'{branch_name}']
        repository = path.dirname(self.repository)

        git_query = Popen(git_command, cwd=repository, stdout=PIPE, stderr=PIPE)
        (git_status, error) = git_query.communicate()

        if git_query.poll() == 0:
            return git_status.decode()

        return error.decode()

    def pull(self, branch_name):
        git_command = ['git', 'pull', 'origin', f'{branch_name}']
        repository = path.dirname(self.repository)

        git_query = Popen(git_command, cwd=repository, stdout=PIPE, stderr=PIPE)
        (git_status, error) = git_query.communicate()

        if git_query.poll() == 0:
            return git_status.decode()

        return error.decode()

    def branchs(self):
        git_command = ['git', 'branch']
        repository = path.dirname(self.repository)

        git_query = Popen(git_command, cwd=repository, stdout=PIPE, stderr=PIPE)
        (git_status, error) = git_query.communicate()

        if git_query.poll() == 0:
            branchs = []
            allBranch = git_status.decode().split('\n')[:-1]
            for branch in allBranch:
                branchs.append(branch.replace(' ', ''))
            return branchs

        return error.decode()

    def checkout(self, branch_name):
        git_command = ['git', 'checkout', f'{branch_name}']
        repository = path.dirname(self.repository)

        git_query = Popen(git_command, cwd=repository, stdout=PIPE, stderr=PIPE)
        (git_status, error) = git_query.communicate()

        if git_query.poll() == 0:
            return git_status.decode()

        return error.decode()

    def create(self, branch_name):
        git_command = ['git', 'checkout', '-b', f'{branch_name}']
        repository = path.dirname(self.repository)

        git_query = Popen(git_command, cwd=repository, stdout=PIPE, stderr=PIPE)
        (git_status, error) = git_query.communicate()

        if git_query.poll() == 0:
            return git_status.decode()

        return error.decode()

    def merge(self):
        pass
