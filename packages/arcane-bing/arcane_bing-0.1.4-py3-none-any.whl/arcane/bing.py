import webbrowser
import socket
import time
import json
import sys
import logging

import backoff
from bingads.v13.bulk import *
from bingads.v13.reporting import *
from google.api_core import exceptions
from http.client import HTTPException
import uuid
from pathlib import Path
import os


TEMP_FILE_DIRECTORY = "/tmp/"
WORKING_DIRECTORY = "/tmp/BingAdsSDKPython"


class Client:
    def __init__(self, credentials, secrets_bucket, refresh_token_location, storage_client):
        super()
        if credentials is not None:
            self.credentials = json.load(open(credentials))
            self.authorization_data = AuthorizationData(developer_token=self.credentials["developer_token"])
        else:
            logging.warning('WARNING: Empty credentials provided')
        self.secrets_bucket = secrets_bucket
        self.refresh_token_location = refresh_token_location
        self.storage_client = storage_client

    @backoff.on_exception(backoff.expo, (socket.timeout, ConnectionResetError), max_tries=3)
    def get_bing_ads_api_client(self):

        # You should authenticate for Bing Ads services with a Microsoft Account,
        # instead of providing the Bing Ads username and password set.
        try:
            self.authenticate_with_oauth()
        except EOFError:
            time.sleep(5)
            self.authenticate_with_oauth()

        if not os.path.exists(WORKING_DIRECTORY):
            try:
                os.makedirs(WORKING_DIRECTORY)
            except FileExistsError:
                # In case of several threads that are trying to create the tmp bing directory simultaneously.
                pass

        reporting_service_manager = ReportingServiceManager(
            authorization_data=self.authorization_data,
            poll_interval_in_milliseconds=5000,
            environment=self.credentials["environment"],
            working_directory=WORKING_DIRECTORY
        )

        # In addition to ReportingServiceManager, you will need a reporting ServiceClient
        # to build the ReportRequest.

        reporting_service=ServiceClient(
            'ReportingService',
            authorization_data=self.authorization_data,
            environment=self.credentials["environment"],
            version=13,
        )

        customer_service = ServiceClient(
            'CustomerManagementService',
            authorization_data=self.authorization_data,
            environment=self.credentials["environment"],
            version=13,
        )

        return reporting_service_manager, reporting_service

    def authenticate_with_oauth(self):
        authentication = OAuthDesktopMobileAuthCodeGrant(
            client_id=self.credentials["client_id"],
            env=self.credentials["environment"]
        )

        # It is recommended that you specify a non guessable 'state' request parameter to help prevent
        # cross site request forgery (CSRF).
        authentication.state = 'ClientStateGoesHere'

        # Assign this authentication instance to the self.authorization_data.
        self.authorization_data.authentication = authentication

        # Register the callback function to automatically save the refresh token anytime it is refreshed.
        # Uncomment this line if you want to store your refresh token. Be sure to save your refresh token securely.
        self.authorization_data.authentication.token_refreshed_callback = self.save_refresh_token

        refresh_token = self.get_refresh_token()

        try:
            # If we have a refresh token let's refresh it
            if refresh_token is not None:
                self.authorization_data.authentication.request_oauth_tokens_by_refresh_token(refresh_token)
            else:
                self.request_user_consent()
        except OAuthTokenRequestException:
            # The user could not be authenticated or the grant is expired.
            # The user must first sign in and if needed grant the client application access to the requested scope.
            self.request_user_consent()

    def request_user_consent(self):
        webbrowser.open(self.authorization_data.authentication.get_authorization_endpoint(), new=1)
        if sys.version_info.major >= 3:
            response_uri = input(
                "You need to provide consent for the application to access your Bing Ads accounts. "
                "After you have granted consent in the web browser for the application to access your Bing Ads accounts, "
                "please enter the response URI that includes the authorization 'code' parameter: \n"
            )
        if self.authorization_data.authentication.state != self.credentials["client_state"]:
            raise Exception("The OAuth response state does not match the client request state.")

        # Request access and refresh tokens using the URI that you provided manually during program execution.
        self.authorization_data.authentication.request_oauth_tokens_by_response_uri(response_uri=response_uri)

    @backoff.on_exception(backoff.expo, (socket.timeout, ConnectionError, HTTPException),  max_tries=3)
    def get_refresh_token(self):
        blob_token = self.storage_client.bucket(self.secrets_bucket).blob(self.refresh_token_location)
        try:
            return blob_token.download_as_string()
        except exceptions.NotFound:
            return None

    @backoff.on_exception(backoff.expo,  (socket.timeout, ConnectionError, HTTPException),  max_tries=5)
    def save_refresh_token(self, oauth_tokens):
        """ Stores a refresh token on a bucket. """
        blob_token = self.storage_client.bucket(self.secrets_bucket).blob(self.refresh_token_location)
        blob_token.upload_from_string(oauth_tokens.refresh_token)

    @backoff.on_exception(backoff.expo,  (socket.timeout, ConnectionError, HTTPException, FileDownloadException, SdkException),  max_tries=3)
    def submit_and_download(self, report_request, reporting_service_manager: ReportingServiceManager) -> str:
        """
        Submit the download request and then store the result file in a local temp file.
        Returns the path to the temporary downloaded file
        :param report_request: created with reporting_service.factory.create('<...ReportRequest>')
        :raises: FileDownloadException if we failed to download the file in a reasonable amount of time
        """

        temp_dir = Path(TEMP_FILE_DIRECTORY)
        if not temp_dir.is_dir():
            os.mkdir(TEMP_FILE_DIRECTORY)

        reporting_download_operation = reporting_service_manager.submit_download(report_request)
        # You may optionally cancel the track() operation after a specified time interval.
        reporting_download_operation.track(timeout_in_milliseconds=3600000)
        temp_file_name = str(uuid.uuid4()) + 'temp-local-report.csv'
        max_ms_to_download_report = 10 * 60 * 1000  # 10 minutes
        result_file_path = reporting_download_operation.download_result_file(
            result_file_directory=TEMP_FILE_DIRECTORY,
            result_file_name=temp_file_name,
            decompress=True,
            overwrite=True,  # Set this value true if you want to overwrite the same file.
            timeout_in_milliseconds=max_ms_to_download_report
            # You may optionally cancel the download after a specified time interval.
        )

        print("Download temporary result file: {0}\n".format(result_file_path))

        return result_file_path
