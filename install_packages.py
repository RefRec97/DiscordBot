import subprocess


def install_interactions():
    subprocess.check_call('pip install --user discord-py-interactions')


def install_interactions_get():
    subprocess.check_call('pip install --user interactions-get')


def install_mysql_connector():
    subprocess.check_call('pip install mysql-connector-python')


def install_quickchart():
    subprocess.check_call('pip install quickchart-io')


install_interactions()
install_interactions_get()
install_mysql_connector()
install_quickchart()
