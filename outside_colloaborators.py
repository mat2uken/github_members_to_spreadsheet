#!/usr/bin/python3
# condig: utf-8

from github import Github

github_instance = None
def get_github_instance():
    global github_instance
    if github_instance is None:
        import yaml
        secrets = yaml.load(open('secret.yaml'))
        github_instance = Github(secrets['env']['access_token'])
    return github_instance

def get_collaborators():
    github = get_github_instance()
    user = github.get_user()
    orgs = user.get_orgs()
    for o in orgs:
        if o.name == 'Shiftall':
            org = o
            break

    # get outside collaborators
    collaborators = []
    for m in org.get_outside_collaborators():
        collaborators.append(m.login)

    return collaborators

def main():
    print(get_collaborators())

if __name__ == '__main__':
    main()

