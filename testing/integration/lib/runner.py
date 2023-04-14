from .helper import *
import subprocess
import time
import logging

_env_var = os.environ
_env_path = get_project_folder()
logging.config.fileConfig(os.path.join(get_integration_folder(), "logging.conf"))
nozzle_logger = logging.getLogger("nozzle")


def login_pcf(nozzle_logger):
    path = os.path.join(get_integration_folder(), "scripts")
    cmd = "cd {0}; ./pre_perf.sh".format(path, _env_path)
    try:
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        output, error = proc.communicate()
        if error:
            nozzle_logger.error(error.strip())
    except OSError as e:
        nozzle_logger.error(e)


def start_local_nozzle_binary(time_interval=20):
    path = os.path.join(get_integration_folder(), "scripts")
    cmd = "cd {0}; ./start_nozzle.sh {1} {2}".format(path, _env_path, time_interval)
    try:
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        output, error = proc.communicate()
        if error:
            nozzle_logger.error(error.strip())
    except OSError as e:
        nozzle_logger.error(e)


def deploy_nozzle_to_pcf():
    cmd = f"cd {_env_path}; make deploy-nozzle"
    try:
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        output, error = proc.communicate()
        if error:
            nozzle_logger.error(error.strip())
    except OSError as e:
        nozzle_logger.error(e)


def deploy_date_gen_to_pcf():
    cmd = f"cd {_env_path}; make deploy-data-gen"
    try:
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        output, error = proc.communicate()
        if error:
            nozzle_logger.error(error.strip())
    except OSError as e:
        nozzle_logger.error(e)


def delete_data_gen(name='data_gen'):
    cmd = f"cf delete {name} -f"

    try:
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        output, error = proc.communicate()
        if error:
            nozzle_logger.error(error.strip())
    except OSError as e:
        nozzle_logger.error(e)


def delete_pcf_org():
    nozzle_logger.info("Deleting pcf org...")
    cmd = "cf delete-org splunk-ci-org -f"

    try:
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        output, error = proc.communicate()
        if error:
            nozzle_logger.error(error.strip())
    except OSError as e:
        nozzle_logger.error(e)


def wait_until_date_gen_done(name=None):
    cmd = f"cf logs {name} --recent"
    try:
        while True:
            time.sleep(10)
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
            output, error = proc.communicate()
            if 'data generation done' in str(output):
                break
    except OSError as e:
        nozzle_logger.error(e)
