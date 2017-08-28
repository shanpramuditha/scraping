#!/usr/bin/env python
"""
This script was written by Gregory Bolet for the Instructables Community

Description:
        This program was written to serve as a starting point for those
    experimenting with the Google Drive API for Python with a
    service account
"""

from __future__ import print_function
import httplib2
import os
import time
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.service_account import ServiceAccountCredentials


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/drive'

KEY_FILE_NAME = 'my_project_key_file.json'


def get_service():
    print("Acquiring credentials...")
    credentials = ServiceAccountCredentials.from_json_keyfile_name(filename=KEY_FILE_NAME, scopes=SCOPES)

    #Has to check the credentials with the Google servers
    print("Authorizing...")
    http = credentials.authorize(httplib2.Http())

    # Build the service object for use with any API
    print("Acquiring service...")
    service = discovery.build(serviceName="drive", version="v3", http=http, credentials=credentials)

    print("Service acquired!")
    return service


def main():
    print("This is an example script for working with a Google Drive API service account\n")

    #get the service object using the credentials file
    service = get_service()

    #Do whatever service object calls here...

    print("Requested operations complete. Exiting...\n")

if __name__ == '__main__':
    main()
