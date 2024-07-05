import os
import json
import base64
from google.cloud import logging as cloud_logging
import logging
from google.cloud import firestore
import functions_framework

logging_client = cloud_logging.Client()
logging_client.setup_logging()
logger = logging_client.logger("identity-delete-trigger")

try:
    db = firestore.Client(project=os.environ.get("PROJECTID"))
except Exception as e:
    logging.error("Can't connect to Firestore Client: {}".format(str(e)))


@functions_framework.cloud_event
def firestoreUserDelete(cloud_event):

    payload = base64.b64decode(cloud_event.data["message"]["data"])
    payload_json = json.loads(str(payload, "utf-8"))
    logging.info(f"Payload: {payload_json}")

    if "protoPayload" in payload_json:
        userId = payload_json["protoPayload"]["request"]["localId"]
        logging.warn(f"User ID: {userId} is deleted by the Admin console")
    else:
        userId = payload_json["jsonPayload"]["metadata"]["tokenInfo"]["claims"][
            "user_id"
        ]

    try:
        db.collection("users").document(userId).delete()
        logging.info(f"Document {userId} successfully deleted!")
    except Exception as e:
        logging.error(f"Error removing document {userId}: {str(e)}")
