import subprocess


subprocess.run('python main.py & python API/API.py &', shell=True, check=False)