# -*- coding: utf-8 -*-
"""Base pytest configuration file."""
import os
import shutil
from app_lib import AppLib

# can't import TCEX profile until the system path is fixed
if os.getenv('TCEX_SITE_PACKAGE') is None:
    # update the path to ensure the App has access to required modules
    AppLib().update_path()

from tcex.app_config_object.profile import Profile  # pylint: disable=wrong-import-position


def profiles(profiles_dir):
    """Get all testing profile names for current feature."""
    profile_names = []
    for filename in sorted(os.listdir(profiles_dir)):
        if filename.endswith('.json'):
            profile_names.append(filename.replace('.json', ''))
    return profile_names


def pytest_addoption(parser):
    """Add arg flag to control replacement of outputs."""
    parser.addoption('--merge_inputs', action='store_true')
    parser.addoption('--merge_outputs', action='store_true')
    parser.addoption('--replace_exit_message', action='store_true')
    parser.addoption('--replace_outputs', action='store_true')
    parser.addoption('--update', action='store_true')
    parser.addoption('--record_session', action='store_true')
    parser.addoption('--ignore_session', action='store_true')
    parser.addoption('--enable_autostage', action='store_true')
    parser.addoption('--disable_autostage', action='store_true')
    parser.addoption(
        '--environment', action='append', help='Sets the TCEX_TEST_ENVS environment variable',
    )


def pytest_generate_tests(metafunc):
    """Generate parametrize values for test_profiles.py::test_profiles tests case.

    Replacing "@pytest.mark.parametrize('profile_name', profile_names)"

    Skip functions that do not accept "profile_name" as an input, specifically this should
    only be used for the test_profiles method in test_profiles.py.
    """
    # we don't add automatic parameterization to anything that doesn't request profile_name
    if 'profile_name' not in metafunc.fixturenames:
        return

    # get the profile.d directory containing JSON profile files
    profile_dir = os.path.join(
        os.path.dirname(os.path.abspath(metafunc.module.__file__)), 'profiles.d'
    )

    permutations = []
    ids = []
    for profile_name in profiles(profile_dir):
        # At this point, we append one permutation record for *each* variation of the profile
        feature = profile_dir.split(os.sep)[-2]

        profile = Profile(name=profile_name, feature=feature, pytestconfig=metafunc.config)
        # test_permutations will give us back a list of (id, base_name, options)
        for test_permutation in profile.test_permutations():
            # collect last two items of returned tuple to match 'profile_name,options' of
            # parametrized inputs
            permutations.append(test_permutation[1:])
            # collect updated profile name (e.g., get_incident or get_incident:autostage)
            ids.append(test_permutation[0])

    # decorate "test_profiles()" method with parametrize profiles (standard and permuted)
    metafunc.parametrize('profile_name,options', permutations, ids=ids)


# clear log directory
def clear_log_directory():
    """Clear the App log directory."""
    log_directory = 'log'
    if os.path.isdir(log_directory):
        print('Clearing log directory.')
        for log_file in os.listdir(log_directory):
            file_path = os.path.join(log_directory, log_file)
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            if os.path.isfile(file_path):
                os.remove(file_path)


def pytest_unconfigure(config):  # pylint: disable=unused-argument
    """Execute unconfigure logic before test process is exited."""
    log_directory = os.path.join(os.getcwd(), 'log')

    # remove any 0 byte files from log directory
    for root, dirs, files in os.walk(log_directory):  # pylint: disable=unused-variable
        for f in files:
            f = os.path.join(root, f)
            try:
                if os.path.getsize(f) == 0:
                    os.remove(f)
            except OSError:
                continue

    # display any Errors or Warnings in tests.log
    test_log_file = os.path.join(log_directory, 'tests.log')
    if os.path.isfile(test_log_file):
        with open(test_log_file, 'r') as fh:
            issues = []
            for line in fh:
                if '- ERROR - ' in line or '- WARNING - ' in line:
                    issues.append(line.strip())

            if issues:
                print('\nErrors and Warnings:')
                for i in issues:
                    print(f'- {i}')

    # remove service started file
    try:
        os.remove('./SERVICE_STARTED')
    except OSError:
        pass


clear_log_directory()
