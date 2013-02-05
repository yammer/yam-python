"""
Tests for excercising the whole system in concert.
"""

from multiprocessing import Process
from unittest import TestCase

from flask import Flask, request

import yampy


class FakeYammerServer(object):
    def __init__(self):
        self._server = Flask("FakeYammerServer")

        @self._server.route("/oauth2/access_token.json")
        def access_token():
            return """{"access_token": {"token": "valid_token"}}"""

        @self._server.route("/api/v1/messages.json")
        def messages():
            return """{"messages": [{}, {}, {}]}"""

    def run_as_process(self):
        self.process = Process(target=self._server.run)
        self.process.start()

    def stop_process(self):
        self.process.terminate()
        self.process.join()


class MessageIntegrationTest(TestCase):
    def setUp(self):
        self.fake_yammer_server = FakeYammerServer()
        self.fake_yammer_server.run_as_process()

    def tearDown(self):
        self.fake_yammer_server.stop_process()

    def test_fetching_messages(self):
        authenticator = yampy.Authenticator(
            client_id="valid_client_id",
            client_secret="valid_client_secret",
            oauth_base_url="http://localhost:5000/oauth2",
        )

        access_token = authenticator.fetch_access_token("valid_code")

        yammer = yampy.Yammer(
            access_token=access_token,
            base_url="http://localhost:5000/api/v1",
        )
        message_result = yammer.messages.all()

        self.assertEqual(3, len(message_result["messages"]))
