import subprocess

filename = './CoralPet_app/app.py'
while True:
    p = subprocess.Popen('python '+filename, shell=True).wait()
    if p != 0:
        continue
    else:
        pass