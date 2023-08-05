"""Command-line interface for creating and adminitrating template projects

Defines module functions for sub-commands
"""
import sys
import platform
import logging
import argparse
import subprocess
import shutil
import devopstemplate
from devopstemplate.config import ProjectConfig
from devopstemplate.template import DevOpsTemplate


def git_user():
    """Obtain git user name and email from git config.

    The function expects that the command 'git' is found on the PATH.

    Returns:
        name: string with git user name, empty string if no 'git' command
        email: string with git user email, empty string if no 'git' command
    """
    name = ''
    email = ''
    if shutil.which('git'):
        name = subprocess.check_output(['git', 'config', 'user.name'],
                                       stderr=subprocess.STDOUT,
                                       encoding='utf-8')
        email = subprocess.check_output(['git', 'config', 'user.email'],
                                        stderr=subprocess.STDOUT,
                                        encoding='utf-8')
    return name.strip(), email.strip()


def create(args):
    """Wrapper for sub-command create

    Params:
        args: argparse.Namespace object with argument parser attributes
    """

    config = ProjectConfig(args)
    template = DevOpsTemplate(projectdirectory=config.project_dir,
                              overwrite_exists=config.overwrite_exists,
                              skip_exists=config.skip_exists,
                              dry_run=config.dry_run)

    params = config.create()
    template.create(projectconfig=params)


def manage(args):
    """Wrapper for sub-command manage

    Params:
        args: argparse.Namespace object with argument parser attributes
    """
    config = ProjectConfig(args)
    template = DevOpsTemplate(projectdirectory=config.project_dir,
                              overwrite_exists=config.overwrite_exists,
                              skip_exists=config.skip_exists,
                              dry_run=config.dry_run)

    params = config.manage()
    template.manage(projectconfig=params)


def cookiecutter(args):
    """Wrapper for sub-command manage

    Params:
        args: argparse.Namespace object with argument parser attributes
    """
    config = ProjectConfig(args)
    template = DevOpsTemplate(projectdirectory=config.project_dir,
                              overwrite_exists=config.overwrite_exists,
                              skip_exists=config.skip_exists,
                              dry_run=config.dry_run)

    params = config.cookiecutter()
    template.cookiecutter(projectconfig=params)


def parse_args(args_list):
    """Parse command-line arguments and call a function for processing user
    request.

    The parser defines (sub) commands which are processed with the 'func'
    attribute function obtained from the parsing result, i.e., Namespace object
    ( Namespace=parser.parse_args(args) ).
    Each command sets its function to the func attribute with set_defaults.
    After all command-line flags have been processed, the function associated
    with func is executed.

    Params:
        args_list: list of strings with command-line flags (sys.argv[1:])
    """
    logger = logging.getLogger('main.parse_args')
    descr = ''.join(['Create and manage DevOps template projects'])
    parser = argparse.ArgumentParser(description=descr)
    # top-level arguments (optional)
    parser.add_argument('--project-dir', default='.',
                        help='Project directory, default: current directory')
    parser.add_argument('--skip-exists', action='store_true',
                        help=('Skip copying files if they already '
                              'exist in the project directory'))
    parser.add_argument('--overwrite-exists', action='store_true',
                        help=('Overwrite files if they already '
                              'exist in the project directory'))
    parser.add_argument('--quiet', action='store_true',
                        help='Print only warning/error messages')
    parser.add_argument('--verbose', action='store_true',
                        help='Print debug messages')
    parser.add_argument('--dry-run', action='store_true',
                        help='Pretend to perform actions')
    parser.add_argument('--version', action='store_true',
                        help='Print version')
    # Default for printing help message if no command is provided
    # attribute 'func' is set to a lambda function
    # --> if attribute func keeps the lambda function until the entire parser
    # has been evaluated: call print_help() and show the help message
    parser.set_defaults(func=lambda _: parser.print_help())
    # Subparser commands for project creation and management
    subparsers = parser.add_subparsers(help='Commands')

    create_parser = subparsers.add_parser('create',
                                          help=('Create a new project based '
                                                'on the DevOps template'))
    create_parser.add_argument('-i', '--interactive', action='store_true',
                               help=('Configure project parameters/components'
                                     ' interactively'))
    create_prms = create_parser.add_argument_group('project parameters')
    create_prms.add_argument('projectname',
                             help=('Name of the Python package / '
                                   'top-level import directory'))
    create_prms.add_argument('--project-version',
                             default='0.1.0',
                             help=('default: "0.1.0"'))
    create_prms.add_argument('--project-url',
                             default='',
                             help=('default: ""'))
    create_prms.add_argument('--project-description',
                             default='',
                             help=('default: ""'))
    # git user and email as default for author data
    name, email = git_user()
    create_prms.add_argument('--author-name',
                             default=name,
                             help=(f'default (from git): "{name}"'))
    create_prms.add_argument('--author-email',
                             default=email,
                             help=(f'default (from git): "{email}"'))
    create_cmpnts = create_parser.add_argument_group('project components')
    create_cmpnts.add_argument('--add-scripts-dir', action='store_true',
                               help='Add scripts directory')
    create_cmpnts.add_argument('--add-docs-dir', action='store_true',
                               help='Add docs directory')
    create_cmpnts.add_argument('--no-gitignore-file', action='store_true',
                               help='Do not add .gitignore file')
    create_cmpnts.add_argument('--no-readme-file', action='store_true',
                               help='Do not add README.md file')
    create_cmpnts.add_argument('--no-sonar', action='store_true',
                               help='Do not add SonarQube support')
    # If the create subparser has been activated by the 'create' command,
    # override the func attribute with a pointer to the 'create' function
    # (defined above) --> overrides default defined for the main parser.
    create_parser.set_defaults(func=create)

    manage_parser = subparsers.add_parser('manage',
                                          help=('Add individual components of '
                                                'the DevOps template'))
    manage_parser.add_argument('--add-scripts-dir', action='store_true',
                               help='Add scripts directory')
    manage_parser.add_argument('--add-docs-dir', action='store_true',
                               help='Add docs directory')
    manage_parser.add_argument('--add-gitignore-file', action='store_true',
                               help='Add .gitignore file')
    manage_parser.add_argument('--add-readme-file', action='store_true',
                               help='Add README.md file')
    manage_parser.add_argument('--add-sonar', action='store_true',
                               help='Add SonarQube support')
    # If the manage subparser has been activated by the 'manage' command,
    # override the func attribute with a pointer to the 'manage' function
    # (defined above) --> overrides default defined for the main parser.
    manage_parser.set_defaults(func=manage)

    cc_parser = subparsers.add_parser('cookiecutter',
                                      help=('Create a cookiecutter'
                                            ' template'))
    cc_parser.add_argument('-i', '--interactive', action='store_true',
                           help=('Configure project parameters/components'
                                 ' interactively'))
    cc_prms = cc_parser.add_argument_group('project parameters')
    cc_prms.add_argument('--project-name',
                         default='',
                         help=('Name of the Python package / '
                               'top-level import directory'))
    cc_prms.add_argument('--project-version',
                         default='0.1.0',
                         help=('default: "0.1.0"'))
    cc_prms.add_argument('--project-url',
                         default='',
                         help=('default: ""'))
    cc_prms.add_argument('--project-description',
                         default='',
                         help=('default: ""'))
    cc_prms.add_argument('--author-name',
                         default='',
                         help=('default ""'))
    cc_prms.add_argument('--author-email',
                         default='',
                         help=('default ""'))
    # If the cookiecutter subparser has been activated by the 'cookiecutter'
    # command, override the func attribute with a pointer to the 'cookiecutter'
    # function (defined above) --> overrides default for the main parser.
    cc_parser.set_defaults(func=cookiecutter)
    args_ns = parser.parse_args(args=args_list)

    # If version flag is set: print version and quit
    if args_ns.version:
        logger.info('devopstemplate v%s', devopstemplate.__version__)
        return

    # Set log level according to command-line flags
    if args_ns.verbose:
        devopstemplate.LOGCONFIG.debug()
        logger.debug('%s:: %s', platform.node(), ' '.join(sys.argv))
        logger.debug('devopstemplate v%s\n', devopstemplate.__version__)
    elif args_ns.quiet:
        devopstemplate.LOGCONFIG.warning()

    logger.debug('Command-line args: %s', args_list)
    args_dict = vars(args_ns)
    logger.debug('Options:\n%s', ', '.join(f'{key} : {val}'
                                           for key, val in args_dict.items()))
    args_ns.func(args_ns)


def main():
    """Entrypoint for starting the command-line interface.
    Control-flow continues depending on user arguments.

    Passes all command-line flags sys.argv[1:] to argparse
    (implemented in parse_args)
    """
    parse_args(sys.argv[1:])


if __name__ == "__main__":
    main()
