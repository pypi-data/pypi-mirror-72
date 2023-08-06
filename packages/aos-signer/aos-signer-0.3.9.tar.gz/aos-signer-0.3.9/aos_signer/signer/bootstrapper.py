#
#  Copyright (c) 2018-2019 Renesas Inc.
#  Copyright (c) 2018-2019 EPAM Systems Inc.
#

import os

_meta_folder_name = 'meta'
_src_folder_name = 'src'
_config_file_name = 'config.yaml'


def run_bootstrap():
    _create_folder_if_not_exist(_meta_folder_name)
    _create_folder_if_not_exist(_src_folder_name)
    _init_conf_file()
    _print_epilog()


def _create_folder_if_not_exist(folder_name):
    if os.path.isdir(folder_name):
        print("Folder {} exists... Skipping".format(folder_name))
    else:
        os.mkdir(folder_name)
        print("Folder {} created".format(folder_name))


def _init_conf_file():
    conf_file_path = os.path.join(_meta_folder_name, _config_file_name)
    if os.path.isfile(conf_file_path):
        print("Config file {} exists... Skipping".format(_config_file_name))
    else:
        with open(conf_file_path, 'x') as cfp:
            cfp.write(_config_bootstrap)
        print("Config file {}/{} created".format(_meta_folder_name, _config_file_name))


def _print_epilog():
    print('------------')
    print('Further steps:')
    print("Copy your service files with desired folders to 'src' folder.")
    print("Copy your private key (private_key.pem) and Service Provider certificate (sp-client.pem) to meta folder.")
    print("Update meta/config.yaml with desired values.")
    print("Run 'aos-signer sign' to sign service and 'aos-signer upload' to upload signed service to the cloud")


_config_bootstrap = """
# Commented sections are optional. Uncomment them if you want to include them in config

#publisher: # General publisher info section
#    author: # Author info
#    company: # Company info

# How to build and sign package
build:
    os: linux
    arch: string
    sign_key: private_key.pem
    sign_certificate: sp-client.pem
    remove_non_regular_files: True
    # context: string, optional

# Information about publishing process (URI, cert, etc)
publish:
    url: aoscloud.io
    service_uid: #Service UID Can be found on Service page 
    tls_key: private_key.pem
    tls_certificate: sp-client.pem

# Service configuration
configuration:
    state:
        filename: state.dat
        required: False

    # Strartup command
    cmd: string

    workingDir: string

#    Quotas assigned to service
#      quotas:
#        cpu: 50
#        mem: 2KB
#        state: 64KB
#        storage: 64KB
#        upload_speed: 32Kb
#        download_speed: 32Kb
#        upload: 1GB
#        download: 1GB
#        temp: 32KB
#   
#  Resource alerts
#    alerts:
#        ram:
#            minTime: string
#            minThreshold: 10,
#            maxThreshold: 150
#        cpu:
#            minTime: string
#            minThreshold: 40,
#            maxThreshold: 45
#        storage:
#            minTime: string
#            minThreshold: 10,
#            maxThreshold: 150
#        upload:
#            minTime: string
#            minThreshold: 10,
#            maxThreshold: 150
#        download:
#            minTime: string
#            minThreshold: 10,
#            maxThreshold: 150
"""
