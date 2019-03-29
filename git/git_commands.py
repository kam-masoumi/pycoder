from subprocess import Popen, PIPE
from os import path


class Git:
    def __init__(self, directory=None):
        self.directory = directory+'/'

    def clone(self, repository):
        git_command = ['git', 'clone', f'{repository}']
        choiceDirectory = path.dirname(self.directory)

        git_query = Popen(git_command, cwd=choiceDirectory, stdout=PIPE, stderr=PIPE)
        (git_status, error) = git_query.communicate()

        git_query.wait()
        if git_status.decode() != '':
            return git_status.decode()
        else:
            return error.decode()

    def status(self):
        git_command = ['git', 'status']
        repository = path.dirname(self.directory)

        git_query = Popen(git_command, cwd=repository, stdout=PIPE, stderr=PIPE)
        (git_status, error) = git_query.communicate()

        git_query.wait()
        if git_status.decode() != '':
            return git_status.decode()
        else:
            return error.decode()

    def diff(self):
        git_command = ['git', 'diff']
        repository = path.dirname(self.directory)

        git_query = Popen(git_command, cwd=repository, stdout=PIPE, stderr=PIPE)
        (git_status, error) = git_query.communicate()

        git_query.wait()
        if git_status.decode() != '':
            return git_status.decode()
        else:
            return error.decode()

    def commit(self, message):
        git_command = ['git', 'commit', '-am', f'"{message}"']
        repository = path.dirname(self.directory)

        git_query = Popen(git_command, cwd=repository, stdout=PIPE, stderr=PIPE)
        (git_status, error) = git_query.communicate()

        git_query.wait()
        if git_status.decode() != '':
            return git_status.decode()
        else:
            return error.decode()

    def push(self, branch_name):
        git_command = ['git', 'push', 'origin', f'{branch_name}']
        repository = path.dirname(self.directory)

        git_query = Popen(git_command, cwd=repository, stdout=PIPE, stderr=PIPE)
        (git_status, error) = git_query.communicate()

        git_query.wait()
        if git_status.decode() != '':
            return git_status.decode()
        else:
            return error.decode()

    def pull(self, branch_name):
        git_command = ['git', 'pull', 'origin', f'{branch_name}']
        repository = path.dirname(self.directory)

        git_query = Popen(git_command, cwd=repository, stdout=PIPE, stderr=PIPE)
        (git_status, error) = git_query.communicate()

        git_query.wait()
        if git_status.decode() != '':
            return git_status.decode()
        else:
            return error.decode()

    def branchs(self):
        git_command = ['git', 'branch']
        repository = path.dirname(self.directory)

        git_query = Popen(git_command, cwd=repository, stdout=PIPE, stderr=PIPE)
        (git_status, error) = git_query.communicate()

        git_query.wait()
        if git_status.decode() != '':
            branchs = []
            allBranch = git_status.decode().split('\n')[:-1]
            for branch in allBranch:
                branchs.append(branch.replace(' ', ''))
            return branchs
        else:
            return error.decode()

    def checkout(self, branch_name):
        git_command = ['git', 'checkout', f'{branch_name}']
        repository = path.dirname(self.directory)

        git_query = Popen(git_command, cwd=repository, stdout=PIPE, stderr=PIPE)
        (git_status, error) = git_query.communicate()

        git_query.wait()
        if git_status.decode() != '':
            return git_status.decode()
        else:
            return error.decode()

    def create(self, branch_name):
        git_command = ['git', 'checkout', '-b', f'{branch_name}']
        repository = path.dirname(self.directory)

        git_query = Popen(git_command, cwd=repository, stdout=PIPE, stderr=PIPE)
        (git_status, error) = git_query.communicate()

        git_query.wait()
        if git_status.decode() != '':
            return git_status.decode()
        else:
            return error.decode()

    def merge(self):
        pass
