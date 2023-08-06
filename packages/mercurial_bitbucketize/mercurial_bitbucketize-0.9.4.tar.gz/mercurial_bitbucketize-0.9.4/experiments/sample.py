# -*- coding: utf-8 -*-

from pybitbucket import bitbucket
from pybitbucket.repository import Repository as BitbucketRepository
import keyring
import getpass
from mercurial import encoding


class MyConfig(bitbucket.Config):
    # bitbucket_url = 'api.bitbucket.org'
    username = 'Mekk'
    email = 'Marcin.Kasperski@mekk.waw.pl'

    def __init__(self):
        self.password = keyring.get_password(self.bitbucket_url, self.username)
        if isinstance(self.password, unicode):
            self.password = encoding.tolocal(self.password.encode('utf-8'))
        if not self.password:
            password = getpass.getpass("Your BitBucket password: ")
            keyring.set_password(self.bitbucket_url, self.username, password)


bitbucket.Client.configurator = MyConfig
bb_client = bitbucket.Client()

print "Connected as", bb_client.get_username()

# repo = BitbucketRepository.create_repository(username, repo_name,
#    fork_policy, is_private, scm=?, name=?, description=?, language=?,
#    has_issues=?, has_wiki=?, client=bb_client)

def print_repo(repo):
    print "Repository data for", repo['full_name']
    for key in ['name', 'has_wiki', 'has_issues', 'is_private',
                'language', 'scm', 'updated_on', 'created_on', 'uuid']:
        print "    {0}: {1}".format(key, repo.get(key))
    # Jest też ['links']['clone']  - lista słowników href, name gdzie
    #  href to https i ssh
    # Jest też ['owner]['username']
    # import pprint; pprint.pprint(repo)

repo = BitbucketRepository.find_repository_by_full_name(
    "Mekk/mercurial-all_dirs", client=bb_client)
print_repo(repo)

repo = BitbucketRepository.find_repository_by_owner_and_name(
    "Mekk", "mercurial-all_paths", client=bb_client)
print_repo(repo)

for repo in BitbucketRepository.find_repositories_by_owner_and_role("Mekk"):
    print_repo(repo)
