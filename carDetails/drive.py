# -*- coding: utf-8 -*-
import httplib2
import logging
import random
import time

import settings

from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from apiclient import errors
from oauth2client.client import SignedJwtAssertionCredentials

from utils.exceptions import GoogleDriveError


def createDriveService():
    """Builds and returns a Drive service object authorized with the given service account.

    Returns:
      Drive service object.
    """
    f = file(settings.SERVICE_ACCOUNT_PKCS12_FILE_PATH, 'rb')
    key = f.read()
    f.close()
    credentials = SignedJwtAssertionCredentials(settings.SERVICE_ACCOUNT_EMAIL, key,
        scope='https://www.googleapis.com/auth/drive')
    http = httplib2.Http()
    http = credentials.authorize(http)

    return build('drive', 'v2', http=http)


def file_upload(filename, uid):
    logger = logging.getLogger('import_log')
    logging.basicConfig()
    for i in range(0, 3):
        try:
            drive = createDriveService()  # All fine

            media_body = MediaFileUpload(filename, mimetype=mimetype,
                                        resumable=True)  # All fine
            body = {
                'title': filename,
                'description': 'imported file',
                'mimeType': mimetype,
            }

            uploaded_file = drive.files().insert(body=body, media_body=media_body, convert=True, quotaUser=uid).execute() # ERROR
            fid = uploaded_file['id']

            new_permission = {
                'type': 'anyone',
                'role': 'reader',
            }
            drive.permissions().insert(fileId=fid, body=new_permission).execute()
            return uploaded_file
        except errors.HttpError, e:
            logger.error('problems with drive, http')
            logger.info(e)
            time.sleep((2 ** i) + random.randint(0, 1000) / 1000)
        except ExtensionError, e:
            raise e
        except Exception, e:
            logger.error('problems with drive')
            logger.info(e)
            raise e

    raise GoogleDriveError('Sorry, we are having trouble completing your request. Please try again later.')