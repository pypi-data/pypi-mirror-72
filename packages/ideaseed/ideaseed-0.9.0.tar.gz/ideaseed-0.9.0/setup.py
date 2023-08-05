# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ideaseed']

package_data = \
{'': ['*']}

install_requires = \
['cli-box>=0.2.0,<0.3.0',
 'colr>=0.9.1,<0.10.0',
 'docopt>=0.6.2,<0.7.0',
 'flatten-list>=0.2.0,<0.3.0',
 'gkeepapi>=0.11.16,<0.12.0',
 'inquirer>=2.7.0,<3.0.0',
 'pygithub>=1.51,<2.0',
 'semantic-version>=2.8.5,<3.0.0',
 'strip-ansi>=0.1.1,<0.2.0']

entry_points = \
{'console_scripts': ['ideaseed = ideaseed.cli:run']}

setup_kwargs = {
    'name': 'ideaseed',
    'version': '0.9.0',
    'description': 'Note down your ideas and get them to the right place, without switching away from your terminal',
    'long_description': '# ![ideaseed](visual-identity/ideaseed-logomark-color-transparent.svg)\n\nDo you have ideas suddenly and just wished you could catch them as fast as possible, as to not loose them, without having to interrupt what you were doing?\n\nAs I guy without a lot of more or less stupid ideas, I use Google Keep as a centralized place to put all of my thoughts that I deem worthy of consideration.\n\nI recently started to use GitHub Projects for _coding_ project ideas as a [single project called "incubator" on my GitHub profile directly](https://github.com/ewen-lbh?tab=projects), and as issues or notes when the idea is related to an already-existing project and repo.\n\nBut when I don\'t get to decide _when_ this idea comes, and I often need to interrupt what am I doing to open github, get to the right page, input my idea and get back. And I find it frustrating.\n\nEnough rambling. Here\'s what you came for.\n\nNote down your ideas and get them to the right place, without switching away from your terminal\n\n## Installation\n\nIdeaseed is available [on PyPI.org](https://pypi.org/project/ideaseed):\n\n```sh-session\npip install ideaseed\n```\n\nSee [Installation troubleshooting](#installation-troubleshooting) if you can\'t install it like this.\n\n## Usage\n\n```bash\nideaseed (--help | --about | --version)\nideaseed [options] ARGUMENTS...\n```\n\n### Examples\n\n```sh-session\n# Save a card "test" in schoolsyst/webapp > project "UX" > column "To-Do"\n$ ideaseed schoolsyst/webapp UX "test"\n# Save a card "lorem" in your-username/ipsum > project "ipsum" > column "To-Do"\n$ ideaseed ipsum "lorem"\n# Save a card "a CLI to note down ideas named ideaseed" in your user profile > project "incubator" > column "willmake"\n$ ideaseed --user-keyword=project --user-project=incubator project "a CLI to note down ideas named ideaseed"\n```\n\n### Arguments\n\n| Argument | Meaning                                                                                                              | Default value  |\n| -------- | -------------------------------------------------------------------------------------------------------------------- | -------------- |\n| REPO     | Select a repository by name                                                                                          |\n|          | If not given, uses Google Keep instead of GitHub (or uses your user profile\'s projects if --project is used)         |\n|          | If --user-keyword\'s value is given, creates a card on your user\'s project (select which project with --user-project) |\n|          | If given in the form OWNER/REPO, uses the repository OWNER/REPO                                                      |\n|          | If given in the form REPO, uses the repository "your username/REPO"                                                  |\n| PROJECT  | Select a project by name to put your card to [default: REPO\'s value]                                                 | `REPO`\'s value |\n|          | If creating a card on your user\'s project, this becomes the COLUMN                                                   |\n| COLUMN   | Select a project\'s column by name [default: To-Do]                                                                   | To-Do          |\n|          | If creating a card on your user\'s project, this is ignored                                                           |\n\n### Options\n\n| Shorthand | Full-length            | Description                                                                                                     |\n| --------- | ---------------------- | --------------------------------------------------------------------------------------------------------------- |\n| -c        | --color COLOR          | Chooses which color to use for Google Keep cards. See [Color names](#color-names) for a list of valid values    |\n| -t        | --tag TAG              | Adds tags to the Google Keep card. Can also be used on GitHub together with --issue to add labels to the issue. |\n| -i        | --issue TITLE          | Creates an issue with title TITLE.                                                                              |\n| -I        | --interactive          | Prompts you for the above options when they are not provided.                                                   |\n| -L        | --logout               | Clears the authentification cache                                                                               |\n| -m        | --create-missing       | Create non-existant tags, projects or columns specified (needs confirmation if -I is used)                      |\n| -o        | --open                 | Open the relevant URL in your web browser.                                                                      |\n| -l        | --label LABEL          | Alias for --tag. See --tag\'s description.                                                                       |\n| -@        | --assign-to USERNAME   | Assigns users to the created issue. Only works when --issue is used.                                            |\n| -M        | --milestone TITLE      | Assign the issue to a milestone with title TITLE.                                                               |\n|           | --pin                  | Pin the Google Keep card                                                                                        |\n|           | --about                | Details about ideaseed like currently-installed version                                                         |\n|           | --version              | Like --about, without dumb and useless stuff                                                                    |\n|           | --user-project NAME    | Name of the project to use as your user project                                                                 |\n|           | --user-keyword NAME    | When REPO is NAME, creates a GitHub card on your user profile instead of putting it on REPO                     |\n|           | --no-auth-cache        | Don\'t save credentials in a temporary file                                                                      |\n|           | --no-check-for-updates | Don\'t check for updates, don\'t prompt to update when current version is outdated                                |\n|           | --no-self-assign       | Don\'t assign the issue to yourself                                                                              |\n\n#### Color names\n\n- blue\n- brown\n- darkblue\n- gray\n- green\n- orange\n- pink\n- purple\n- red\n- teal\n- white\n- yellow\n\nYou don\'t have to specify the whole color name, just enough to be non-ambiguous:\n\n- bl\n- br\n- d\n- gra\n- gre\n- o\n- pi\n- pu\n- r\n- t\n- w\n- y\n\nSome color have aliases:\n\n- cyan is the same as teal\n- indigo is the same as darkblue\n- grey is the same as gray\n- magenta is the same as purple\n\n#### Relax. You don\'t need to remember those options\n\nYou can also use `ideaseed -I` to prompt you for some information:\n\n- Where do you want to upload this idea? (github, google keep)\n- If you decide to use github,\n  - On your profile?\n  - If not:\n    - Which repo? (using REPO or OWNER/REPO) (autocompletes with repositories you contribute to)\n    - Which column? (choices are the column names, and you can type the column\'s index to be quicker)\n- If you decide to use google keep,\n  - Which color? (defaults to white)\n  - Some tags?\n\n## Installation troubleshooting\n\nIf you get an error message saying "No matching distribution found":\n\n```sh-session\n$ pip install ideaseed\nCollecting ideaseed\n  Could not find a version that satisfies the requirement ideaseed (from versions: )\nNo matching distribution found for ideaseed\n```\n\nSee if the python version `pip` uses is at least 3.6:\n\n```sh-session\n$ pip --version\npip 9.0.1 from /usr/lib/python2.7/dist-packages (python 2.7) # Should be at least "(python 3.6)"\n```\n\nYou can then try with `pip3` (`pip3 --version` should report a python version of at least 3.6):\n\n```sh-session\n$ pip3 --version\npip 20.0.2 from /home/ewen/.local/lib/python3.7/site-packages/pip (python 3.7)\n$ pip3 install ideaseed\n```\n',
    'author': 'Ewen Le Bihan',
    'author_email': 'ewen.lebihan7@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ewen-lbh/ideaseed',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
