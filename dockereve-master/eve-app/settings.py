import os
import re
from copy import deepcopy

afq_schema = {
    'subject_id': {
        'type': 'string',
        'required': True
    }
}




settings = {
    'URL_PREFIX': 'api',
    'API_VERSION': 'v1',
    'ALLOWED_FILTERS': ['*'],
    'MONGO_HOST': os.environ.get('MONGODB_HOST', ''),
    'MONGO_PORT': os.environ.get('MONGODB_PORT', ''),
    'MONGO_DBNAME': 'mriqc_api',
    'PUBLIC_METHODS': ['GET'],
    'PUBLIC_ITEM_METHODS': ['GET'],
    'RESOURCE_METHODS': ['GET', 'POST'],
    'ITEM_METHODS': ['GET'],
    'X_DOMAINS': '*',
    'DOMAIN': {
        'afq': {
            'item_title': 'afq',
        },

    }
}


settings['DOMAIN']['afq']['schema'] = deepcopy(afq_schema)
