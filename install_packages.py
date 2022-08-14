import subprocess


def install_interactions():
    subprocess.check_call('pip install --user discord-py-interactions')


def install_interactions_get():
    subprocess.check_call('pip install --user interactions-get')


def install_mysql_connector():
    subprocess.check_call('pip install mysql-connector-python')


def install_quickchart():
    subprocess.check_call('pip install quickchart-io')


def install_beautifulsoup4():
    subprocess.check_call('pip install beautifulsoup4')


def install_h11():
    subprocess.check_call('pip install h11')


install_interactions()
install_interactions_get()
install_mysql_connector()
install_quickchart()
install_beautifulsoup4()
install_h11()
