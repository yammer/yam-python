"""
Shared support for integration tests.
"""

import json
from multiprocessing import Process
import requests
from requests.exceptions import RequestException
from unittest import TestCase

import flask


class FakeYammerServer(object):
    """
    A Flask-based web server that simulates the Yammer API by returning
    static JSON data that has a similar structure to the real API's responses.

    The server runs on port 5000.
    """

    def __init__(self):
        """
        Creates the server and defines the various routes.
        """
        self._server = flask.Flask("FakeYammerServer")

        @self._server.route("/up")
        def up():
            """
            Not part of the Yammer API: This route is polled by the main
            process to determine when the server process is ready.
            """
            return "Server is up"

        @self._server.route("/oauth2/access_token.json")
        def access_token():
            return """{"access_token": {"token": "valid_token"}}"""

        @self._server.route("/api/v1/messages.json", methods=["GET"])
        def messages():
            return self._message_list_json(
                count=3,
                first_id=1,
            )

        @self._server.route("/api/v1/messages.json", methods=["POST"])
        def post_message():
            return self._message_list_json(
                count=1,
                first_id=4,
                body=flask.request.args.get("body"),
            )

        @self._server.route("/api/v1/messages/<id>.json", methods=["DELETE"])
        def delete_message(id):
            return " "

        @self._server.route(
            "/api/v1/messages/liked_by/current.json",
            methods=["POST", "DELETE"],
        )
        def like_or_unlike_message():
            if "message_id" in flask.request.args:
                return " "
            else:
                return " ", 400

    def run_as_process(self):
        """
        Spawns the fake Yammer API server in a new process. Does not return
        until the server is ready to handle requests.
        """
        self.process = Process(target=self._server.run)
        self.process.start()
        self._poll_until_server_responds()

    def stop_process(self):
        """
        Stops the fake Yammer API server's process.
        """
        if hasattr(self, "process"):
            self.process.terminate()
            self.process.join()

    def _message_list_json(self, count=1, first_id=1, body="Hello world"):
        id_range = xrange(first_id, first_id + count)
        messages = [self._message_dict(msg_id, body) for msg_id in id_range]
        return json.dumps({
            "messages": messages,
            "references": [],
            "meta": [],
        })

    def _message_dict(self, msg_id, body):
        return {
            "id": msg_id,
            "body": {
                "plain": body,
                "parsed": body,
                "rich": body,
            }
        }

    def _poll_until_server_responds(self):
        try:
            requests.get("http://localhost:5000/up", timeout=0.1)
        except RequestException:
            self._poll_until_server_responds()


class TestCaseWithFakeYammerServer(TestCase):
    """
    A TestCase that sets up and tears down a FakeYammerServer.

    Subclasses that need to define their own setUp and tearDown methods
    must call the superclass implementations.
    """
    def setUp(self):
        try:
            self._fake_yammer_server = FakeYammerServer()
            self._fake_yammer_server.run_as_process()
        except:
            if hasattr(self, "_fake_yammer_server"):
                self._fake_yammer_server.stop()
            raise

    def tearDown(self):
        self._fake_yammer_server.stop_process()
