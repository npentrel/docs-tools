import logging
import os.path

logger = logging.getLogger(os.path.basename(__file__))

from giza.git import GitRepo
from giza.config.base import ConfigurationBase

class GitConfigBase(ConfigurationBase):
    def __init__(self, obj, conf, repo=None):
        super(GitConfigBase, self).__init__(obj)
        self._conf = conf
        self._repo = repo

    @property
    def repo(self):
        return self._repo

    @repo.setter
    def repo(self, path=None):
        if self._repo is None:
            self._repo = GitRepo(path)

    @property
    def conf(self):
        return self._conf

    @conf.setter
    def conf(self, value):
        logger.error("cannot set conf at this level")

class GitConfig(GitConfigBase):
    @property
    def commit(self):
        c = self.repo.sha('HEAD')
        self.state['commit'] = c
        return c

    @property
    def branches(self):
        if 'branches' not in self.state:
            self.branches = None
        return self.state['branches']

    @branches.setter
    def branches(self, value):
        self.state['branches'] = GitBranchConfig(None, self.conf, self.repo)

    @property
    def remote(self):
        if 'remote' not in self.state:
            self.remote = None
        return self.state['remote']

    @remote.setter
    def remote(self, value):
        self.state['remote'] = GitRemoteConfig(value)

class GitBranchConfig(GitConfigBase):
    @property
    def current(self):
        if 'current' not in self.state:
            self.current = None

        return self.state['current']

    @current.setter
    def current(self, value):
        self.state['current'] = self.repo.current_branch()

    @property
    def manual(self):
        if 'manual' not in self.state:
            self.manual = None

        return self.state['manual']

    @manual.setter
    def manual(self, value):
        if 'git' in self.conf.runstate.branch_conf and 'branches' in self.conf.runstate.branch_conf['git']:
            if 'manual' in self.conf.runstate.branch_conf['git']['branches']:
                self.state['manual'] = self.conf.runstate.branch_conf['git']['branches']['manual']
            else:
                self.state['manual'] = None
        else:
            self.state['manual'] = None

    @property
    def published(self):
        if 'published' not in self.state:
            self.published = None

        return self.state['published']

    @published.setter
    def published(self, value):
        if 'git' in self.conf.runstate.branch_conf and 'branches' in self.conf.runstate.branch_conf['git']:
            if 'published' in self.conf.runstate.branch_conf['git']['branches']:
                p = self.conf.runstate.branch_conf['git']['branches']['published']

                if not isinstance(p, list):
                    msg = "published branches must be a list"
                    logger.critical(msg)
                    raise TypeError(msg)
                elif p[0] != 'master':
                    msg = "right now, we must publish master"
                    logger.critical(msg)
                    raise TypeError(msg)


                self.state['published'] = p

            else:
                self.state['published'] = []
        else:
            self.state['published'] = 'master'

class GitRemoteConfig(ConfigurationBase):
    @property
    def upstream(self):
        return self.state['upstream']

    @upstream.setter
    def upstream(self, value):
        self.state['upstream'] = value

    @property
    def tools(self):
        return self.state['tools']

    @tools.setter
    def tools(self, value):
        self.state['tools'] = value
