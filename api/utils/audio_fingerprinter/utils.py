import base64
import re

import requests
import urllib3

from api import settings

from . import exception


class PostFields:
    FILENAME = "filename"
    TITLE = "title"
    USER_ID = "userId"


class ResponseFields:
    class Ok:
        FINGERPRINT = "fingerprint"
        DURATION = "duration"

    class Error:
        STATUS = "status"
        MESSAGE = "message"


SERVICE_ERROR_CODE_PREFIXE = "Audio Fingerprinter Error Code "


def _get_service_exception_code_from_message(message: str):
    start_index = message.find(SERVICE_ERROR_CODE_PREFIXE)
    if start_index != -1:
        substring_after_prefix = message[start_index + len(SERVICE_ERROR_CODE_PREFIXE) :]

        match = re.search(r"\d+", substring_after_prefix)
        if match:
            return int(match.group(0))
    return None


def post_fingerprint_audio(filename: str, title: str, user_id: str) -> tuple[bytes, float]:
    try:
        json_data = {PostFields.FILENAME: filename, PostFields.TITLE: title, PostFields.USER_ID: user_id}
        headers = {"Content-Type": "application/json"}
        url = f"http://{settings.AFP_BASE_URL}:{settings.AFP_PORT}/{settings.AFP_POST_ENDPOINT}"
        response = requests.post(url, json=json_data, headers=headers)

        response_json = response.json()
        if response.status_code == 200:
            fingerprint_bytes = base64.b64decode(response_json[ResponseFields.Ok.FINGERPRINT])
            duration = response_json[ResponseFields.Ok.DURATION]
            return fingerprint_bytes, duration
        if response.status_code == 400:
            exception_code = _get_service_exception_code_from_message(response_json[ResponseFields.Error.MESSAGE])
            if exception_code == 2:
                raise exception.WrongFileExtension(response_json[ResponseFields.Error.MESSAGE])
            if exception_code == 3:
                raise exception.WrongFileType(response_json[ResponseFields.Error.MESSAGE])
            if exception_code == 4:
                raise exception.FileNotInPool(response_json[ResponseFields.Error.MESSAGE])
            raise exception.BadRequestException(response_json)
        if response.status_code == 500:
            raise exception.InternalServerException(response_json)
        if response.status_code == 504:
            raise TimeoutError
        if response.status_code == 422:
            exception_code = _get_service_exception_code_from_message(response_json[ResponseFields.Error.MESSAGE])
            if exception_code == 1:
                raise exception.FpcalcStatusException(response_json)
            raise exception.UnprocessableEntityException(response_json)
        if response.status_code == 404:
            raise exception.ServiceNotFoundException()
        raise exception.AudioFingerprinterException(response_json)
    except requests.exceptions.ConnectionError as e:
        if str(e).find("Errno 61") != -1 or str(e).find("Errno 111") != -1:
            raise exception.ServiceNotFoundException()
        raise ConnectionError(str(e))
    except urllib3.exceptions.MaxRetryError as e:
        raise exception.ServiceNotFoundException()
