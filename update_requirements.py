import subprocess
from shutil import copyfile


def post_install():
    # Run pipenv lock command to update the lock file
    subprocess.run(['pipenv', 'lock'], check=True)
    import pdb;pdb.set_trace()
    # Generate the requirements.txt file from the updated lock file
    subprocess.run(['pipenv', 'run', 'pip', 'freeze', '--dev', '>', 'requirements.txt'], shell=True, check=True)

    # Optional: Copy the generated requirements.txt file to a desired location
    copyfile('requirements.txt', 'requirements.txt')


post_install()
