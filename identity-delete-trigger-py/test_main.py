import unittest
from unittest.mock import MagicMock, patch
from main import firestoreUserDelete
from cloudevents.http import CloudEvent
import json
import base64
import os

current_dir = os.path.dirname(__file__)


def create_cloud_event(payload):
    attributes = {
        "type": "com.example.someevent",
        "source": "urn:event:from:myapi/resource/123",
    }
    data = {
        "message": {
            "data": base64.b64encode(json.dumps(payload).encode("utf-8")).decode(
                "utf-8"
            )
        }
    }
    return CloudEvent(attributes, data)


class FirestoreUserDeleteTests(unittest.TestCase):
    @patch("google.cloud.logging.Client", autospec=True)
    @patch("google.cloud.firestore.Client", autospec=True)
    @patch("google.auth.default", return_value=(MagicMock(), "test-project"))
    @patch("main.logging")
    def test_firestoreUserDelete_success(
        self,
        mock_logging,
        mock_auth_default,
        mock_firestore_client,
        mock_logging_client,
    ):
        # read file user-delete.json
        with open(os.path.join(current_dir, "user-delete.json")) as f:
            user_delete = json.load(f)
        cloud_event = create_cloud_event(user_delete)

        # Setup the mock Firestore client
        mock_firestore_instance = mock_firestore_client.return_value
        mock_collection = mock_firestore_instance.collection.return_value
        mock_doc = mock_collection.document.return_value

        # Setup the mock logger
        mock_logger = MagicMock()
        mock_logging_instance = mock_logging_client.return_value
        mock_logging_instance.logger.return_value = mock_logger

        # Calling the function
        firestoreUserDelete(cloud_event)

        # Print out what was called
        print(f"Collection called: {mock_firestore_instance.collection.call_args_list}")
        print(f"Document called: {mock_collection.document.call_args_list}")
        print(f"Delete called: {mock_doc.delete.call_args_list}")


if __name__ == "__main__":
    unittest.main()
