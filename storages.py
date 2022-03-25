from urllib import parse
from instagrapi import Client
from tinydb import TinyDB, Query
import json

class ClientStorage:

    db = TinyDB('./db.json')

    def client(self):
        """Get new client (helper)
        """
        cl = Client()
        cl.request_timeout = 0.1
        return cl

    def get(self, sessionid: str) -> Client:
        """Get client settings
        """
        key = parse.unquote(sessionid.strip(" \""))
        try:
            # print("\n\n\nDB:")
            # with open('./db.json','r') as f:
            #    print(f.read())
            settings = json.loads(self.db.search(Query().sessionid == key)[0]['settings'])
            cl = Client()
            cl.set_settings(settings)
            # commented out because it gave error
            #cl.get_timeline_feed()
            return cl
        except IndexError:
            raise Exception('Session not found (e.g. after reload process), please relogin!')
        except Exception as e:
            print("EXCEPTION IN storages.py GET")
            print(e)

    def set(self, cl: Client) -> bool:
        """Set client settings
        """
        key = parse.unquote(cl.sessionid.strip(" \""))
        self.db.insert({'sessionid': key, 'settings': json.dumps(cl.get_settings())})
        return True

    def add_session(self,sessionid) -> bool:
            """Add real session
            """
            try:
                print("\n\nADD SESSION:")
                key = parse.unquote(sessionid.strip(" \""))
                my_settings = "{\"uuids\": {\"phone_id\": \"2a25c508-e5c1-44a7-b6d4-ab474e8dc9fc\", \"uuid\": \"a707cdd0-64ad-47dd-a74b-0f1b5f87a2d3\", \"client_session_id\": \"c3c9ba10-87c1-46ee-be04-66ae2bcefa9e\", \"advertising_id\": \"2fc75ace-f327-4481-b042-dd3dd757d9bd\", \"android_device_id\": \"android-4a1b9f224d992e26\", \"request_id\": \"3f58a499-e77d-4069-b60a-219f66dbcd31\", \"tray_session_id\": \"c96f2b3d-c486-4fee-baf6-e22eb4120fe8\"}, \"mid\": null, \"ig_u_rur\": null, \"ig_www_claim\": null, \"authorization_data\": {}, \"cookies\": {}, \"last_login\": null, \"device_settings\": {\"app_version\": \"203.0.0.29.118\", \"android_version\": 26, \"android_release\": \"8.0.0\", \"dpi\": \"480dpi\", \"resolution\": \"1080x1920\", \"manufacturer\": \"Xiaomi\", \"device\": \"capricorn\", \"model\": \"MI 5s\", \"cpu\": \"qcom\", \"version_code\": \"314665256\"}, \"user_agent\": \"Instagram 203.0.0.29.118 Android (26/8.0.0; 480dpi; 1080x1920; Xiaomi; MI 5s; capricorn; qcom; en_US; 314665256)\", \"country\": \"US\", \"country_code\": 1, \"locale\": \"en_US\", \"timezone_offset\": -14400}"
                self.db.insert({'sessionid': key, 'settings': my_settings})
            except Exception as e: 
                print(e)
                return False
            return True

    def close(self):
        pass
