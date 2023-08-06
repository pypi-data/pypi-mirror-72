import click


@click.command()
@click.argument('pkg_name')
@click.argument('robot_id')
def cli_show_py_pkg(pkg_name: str, robot_id: str):
    from mini import query_py_pkg
    print(f'{query_py_pkg(pkg_name, robot_id)}')


@click.command()
@click.argument('robot_id')
def cli_list_py_pkg(robot_id: str):
    from mini import list_py_pkg
    print(f'{list_py_pkg(robot_id)}')


@click.command()
@click.argument('project_dir')
def cli_setup_py_pkg(project_dir: str):
    from mini import setup_py_pkg
    print(f'{setup_py_pkg(project_dir)}')


@click.command()
@click.option('--debug', is_flag=True)
@click.argument('pkg_path')
@click.argument('robot_id')
def cli_install_py_pkg(pkg_path: str, robot_id: str, debug: bool = True):
    from mini import install_py_pkg
    install_py_pkg(pkg_path, robot_id, debug)


@click.command()
@click.option('--debug', is_flag=True)
@click.argument('pkg_name')
@click.argument('robot_id')
def cli_uninstall_py_pkg(pkg_name: str, robot_id: str, debug: bool = True):
    from mini import uninstall_py_pkg
    uninstall_py_pkg(pkg_name, robot_id, debug)


@click.command()
@click.option('--debug', is_flag=True)
@click.argument('entry_point')
@click.argument('robot_id')
def cli_run_py_pkg(entry_point: str, robot_id: str, debug: bool = True):
    from mini import run_py_pkg
    run_py_pkg(entry_point, robot_id, debug)


@click.command()
@click.option('--debug', is_flag=True)
@click.argument('cmd')
@click.argument('robot_id')
def cli_run_cmd(cmd: str, robot_id: str, debug: bool = True):
    from mini import run_py_pkg
    run_py_pkg(cmd, robot_id, debug)
