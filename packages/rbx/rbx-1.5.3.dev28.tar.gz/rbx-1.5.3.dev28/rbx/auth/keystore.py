from dataclasses import asdict, dataclass, field, InitVar
import logging
import os
from unittest import mock

import google.auth.credentials
from google.cloud.firestore import Client

logger = logging.getLogger('rbx.auth')


class Keystore:
    """Manages API Keys stored in Google Cloud Firestore (Native Mode)."""

    def __init__(self):
        if os.getenv('GAE_ENV', '').startswith('standard'):
            db = Client()
        else:
            os.environ['FIRESTORE_DATASET'] = 'testing'
            os.environ['FIRESTORE_EMULATOR_HOST'] = '0.0.0.0:8082'
            os.environ['FIRESTORE_EMULATOR_HOST_PATH'] = '0.0.0.0:8082/firestore'
            os.environ['FIRESTORE_HOST'] = 'http://0.0.0.0:8082'
            os.environ['FIRESTORE_PROJECT_ID'] = 'firestore-emulator'

            credentials = mock.Mock(spec=google.auth.credentials.Credentials)
            db = Client(project='firestore-emulator', credentials=credentials)

        self.collection = db.collection('api_keys')

    def _key(self, document):
        """Given a DocumentSnapshot, return the fully loaded Key object."""
        return Key(**{'keystore': self, 'key_id': document.id, **document.to_dict()})

    def create_key(self, email, name, campaigns=None, services=None):
        """Make a new API key.

        A key is associated with a user via her email address. If a key already exists for that
        user, the key is updated instead.
        """
        key = self.get_key(email=email)
        if not key:
            key = {
                'campaigns': campaigns or [],
                'email': email,
                'name': name,
                'services': services or ['*.*'],
                'status': 'active',
            }

            _, ref = self.collection.add(key)
            key = self._key(ref.get())
        else:
            key.update(**{
                'campaigns': campaigns or key.campaigns,
                'name': name or key.name,
                'services': services or key.services,
                'status': 'active',  # the key is resuscitated
            })

        return key

    def get_key(self, key_id=None, email=None):
        """Retrieve a key by ID or email."""
        if key_id:
            document = self.collection.document(key_id).get()
            if document.exists:
                return self._key(document)

        if email:
            document = next(self.collection.where('email', '==', email).stream(), False)
            if document:
                return self._key(document)

    def update_key(self, key, attributes):
        """Set the new Key values in Firestore."""
        assert type(key) is Key, f'Excepted rbx.auth.Key, got {type(key)}'
        document = self.collection.document(key.key_id)
        document.set(attributes, merge=True)


@dataclass
class Key:
    key_id: InitVar[str]
    keystore: InitVar[Keystore]
    email: str
    name: str
    campaigns: list = field(default_factory=list)
    services: list = field(default_factory=['*.*'])
    status: str = 'active'

    def __post_init__(self, key_id, keystore):
        # These are defined as InitVar so that they are not part of the pickled data, and aren't
        # included in the to_dict() representation.
        self.key_id = key_id
        self.keystore = keystore

    def activate(self):
        self.update(status='active')

    def deactivate(self):
        self.update(status='inactive')

    def has_access(self, service, operation):
        """Check whether the service and operation are granted access by this Key."""
        for grant in self.services:
            grant = dict(zip(
                ('service', 'operation'),
                grant.split('.')
            ))
            if grant['service'] == '*':
                return True
            elif grant['service'] == service and grant['operation'] == '*':
                return True
            elif grant['service'] == service and grant['operation'] == operation:
                return True

        return False

    def has_campaign_access(self, campaign):
        """Check whether the campaign is granted access by this Key."""
        if self.campaigns is None:
            return True

        return campaign in self.campaigns

    def to_dict(self):
        return asdict(self)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.__annotations__.keys() and key not in ('email', 'key_id', 'keystore'):
                setattr(self, key, value)

        self.keystore.update_key(self, self.to_dict())
