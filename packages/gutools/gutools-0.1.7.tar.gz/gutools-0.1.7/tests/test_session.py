import pytest
import tempfile
import os
import time

from gutools.session import USession

@pytest.fixture
def temp_folder():
    "Create a temp folder that will be deleted on exit"
    with tempfile.TemporaryDirectory() as folder:
        yield folder




def test_session_init(temp_folder):
    """Create a working environment from scratch"""

    required = set([
        '/db/session.db',
        '/bin/install_bash_completer.rc',
        '/bin/activate.sh',
        '/etc/session.yaml',
    ])

    # print(temp_folder)

    session = USession(path=temp_folder)
    session.init()

    for root, _, files in os.walk(temp_folder):
        for name in files:
            name = os.path.join(root, name)
            name = name.split(temp_folder)[-1]
            # print(name)
            required.difference_update([name])

    assert len(required) == 0, f"Some files was not created: {required} are missing"

    # print("test_session_init funciona!")
    # print("- Ends -")



def test_session_activate(temp_folder):
    """Ativate a session in a clean environment"""
    session = USession(path=temp_folder)
    session.init()
    session.activate()

    time.sleep(5)

    session.deactivate()


    # print("test_session_init funciona!")
    # print("- Ends -")

