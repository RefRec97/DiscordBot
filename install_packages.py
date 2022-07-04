import subprocess

interactions = subprocess.Popen(['python' ,'install_interactions.py'])
interactions.wait()

interactions_get = subprocess.Popen(['python' ,'install_interactions_get.py'])
interactions_get.wait()

mysql = subprocess.Popen(['python' ,'install_mysql_connector.py'])
mysql.wait()

quickchart = subprocess.Popen(['python' ,'install_quickchart.py'])
quickchart.wait()