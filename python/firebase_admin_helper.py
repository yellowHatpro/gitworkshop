import os
import firebase_admin
from firebase_admin import auth, credentials, storage, firestore


class FirebaseAdminHelper:
    def __init__(self, credentials_relative_path, storage_bucket, app_name):
        self.credentials_relative_path = credentials_relative_path
        self.storage_bucket = storage_bucket
        self.app_name = app_name
        self.app = None
        self.bucket = None
        self.firestore_db = None
        self.initialize_app()

    def initialize_app(self):
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) + os.sep + os.pardir
        credentials_path = ROOT_DIR + os.sep + self.credentials_relative_path
        app_options = {
            'storageBucket': self.storage_bucket,
        }
        self.app = firebase_admin.initialize_app(credentials.Certificate(credentials_path), app_options, name=self.app_name)
        self.bucket = storage.bucket(app=self.app)
        self.firestore_db = firestore.client(app=self.app)

    def get_firebase_auth_users(self):
        return [self._user_record_to_dict(user) for user in auth.list_users(app=self.app).users]
    
    def get_firestore_collection_docs(self, collection_name):
        return [self._doc_to_dict(doc) for doc in self.firestore_db.collection(collection_name).get()]
    

    def get_firestore_collection_docs_by_field(self, collection_name, field_name, field_value):
        return [self._doc_to_dict(doc) for doc in self.firestore_db.collection(collection_name).where(field_name, '==', field_value).get()]

    @staticmethod
    def _user_record_to_dict(user_record):
        return {
            'uid': user_record.uid,
            'email': user_record.email,
            'display_name': user_record.display_name,
            'phone_number': user_record.phone_number,
            'photo_url': user_record.photo_url,
            'disabled': user_record.disabled,
            'email_verified': user_record.email_verified,
            'custom_claims': user_record.custom_claims
        }

    @staticmethod
    def _doc_to_dict(doc):
        return {
            'id': doc.id,
            'data': doc.to_dict()
        }

if __name__ == '__main__':
    CREDENTIALS_PATH = 'cred/cred.json'
    STORAGE_BUCKET = 'storage-bucket.appspot.com'
    APP_NAME = 'app_name'

    COLLECTION_NAME = 'collection_name'

    FIELD_NAME = 'field'
    FIELD_VALUE = 'value'

    fba_helper = FirebaseAdminHelper(CREDENTIALS_PATH, STORAGE_BUCKET, APP_NAME)
    print(fba_helper.get_firebase_auth_users())
    print(fba_helper.get_firestore_collection_docs(COLLECTION_NAME))
    print(fba_helper.get_firestore_collection_docs_by_field(COLLECTION_NAME, FIELD_NAME, FIELD_VALUE))
