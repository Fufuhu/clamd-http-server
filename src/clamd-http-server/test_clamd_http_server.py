import unittest
import io
import json

import requests


class TestServer(unittest.TestCase):

    def test_upload_eicar(self):
        url = 'http://localhost:5000/upload'
        # EICAR test virus sequence
        file_name = "EICAR"
        content = 'X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*'

        upload_file = io.StringIO(content)

        file = {
            'file': (file_name, upload_file)
        }

        res = requests.post(url, files=file)

        # check if statsu code is 200 OK
        self.assertEqual(res.status_code, requests.codes.ok)

        response_body = res.content.decode('utf-8')
        response_json = json.loads(response_body)

        expected_message = "{} is uploaded.".format(file_name)
        expected_result = "stream: Win.Test.EICAR_HDB-1 FOUND"

        self.assertEqual(expected_message, response_json.get('Message'))
        self.assertEqual(expected_result, response_json.get('Result'))

        print(response_json.get('Result'))
        print(response_json.get('Message'))


if __name__ == '__main__':
    unittest.main()
