import pytest
import docker
import time
import requests
import logging

logger = logging.getLogger()

client = docker.from_env()
container_name = "test-aoa-img"
max_retries = 10


def pytest_addoption(parser):
    parser.addoption("--img", action="store", help="specify image name")
    parser.addoption("--port", action="store", help="specify port number")
    parser.addoption("--skip-docker", action="store_true", help="don't start the docker container")


def check_aoa_up(aoa_url, auth):
    retries = 0
    while retries < max_retries:
        try:
            resp = requests.get(
                url=aoa_url + "/admin/health",
                auth=auth
            )
            return resp.status_code
        except:
            logger.info('aoa demo container...waiting')
            retries += 1
            time.sleep(5)
    assert (5 == 4), 'aoa demo container...unable to access'


@pytest.fixture(scope="session")
def setup(request):
    skip_docker = request.config.getoption("skip-docker", False)

    if not skip_docker:
        img_name = request.config.getoption("img") if request.config.getoption("img") is not None \
            else "thinkbiganalytics/aoa-demo:2.6.0.rc2"
        port_number = request.config.getoption("port") if request.config.getoption("port") is not None \
            else 8080

        logger.info('aoa demo container...starting')
        client.containers.run(image=img_name,
                              name=container_name,
                              auto_remove=True,
                              privileged=True,
                              ports={
                                  '8080/tcp': port_number,
                                  '9000/tcp': 9000,
                                  '61613/tcp': 61613
                              },
                              volumes={
                                  '/var/run/docker.sock': {
                                      'bind': '/var/run/docker.sock'
                                  }
                              },
                              detach=True)

        def fin():
            logger.info('aoa demo container...removing')
            client.containers.list(all=True, filters={
                "name": container_name
            })[0].remove(force=True)
            logger.info('aoa demo container...removed')

        request.addfinalizer(fin)

    from aoa.api_client import AoaClient
    pytest.aoa_client = AoaClient(aoa_url="http://localhost:8080",
                                  auth_mode="basic",
                                  auth_user="admin",
                                  auth_pass="admin")
    pytest.aoa_client.set_project_id("23e1df4b-b630-47a1-ab80-7ad5385fcd8d")

    check_aoa_up(pytest.aoa_client.aoa_url, pytest.aoa_client.auth)
    logger.info('aoa demo container...started')
