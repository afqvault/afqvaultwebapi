import os
import re
from copy import deepcopy
import json

def validate_metrics(field, value, error):
    if isinstance(value, str):
        try:
            jv = json.loads(value)
        except json.JSONDecodeError as e:
            error(field, "If a string is posted as the mask, it must be decodable to a JSON. JSON decoding failed with the following error: %s"%e)
    #TODO: make sure value in jv is isnumeric, but not for scan parameters


subjects_schema = {
    'subjectID': {
        'type': 'string',
        'required': True
    },
    'projectID': {
        'type': 'string',
        'required': True
    },
    'sessionID': {
        'type': 'string',
        'required': True
    },
    "metadata": {
        'validator': validate_metrics
    }
}

projects_schema = {
    'projectID': {
        'type': 'string',
        'required': True
    },
    'doi': {
        'type': 'string',
        'required': True
    },
    'url': {
        'type': 'string',
        'required': True
    },
    'scan_parameters': {
        'validator': validate_metrics
    }
}

nodes_schema = {
    'subjectID': {
        'type': 'string',
        'required': True
    },
    'nodeID': {
        'type': 'string',
        'required': True
    },
    'tractID': {
        'type': 'string',
        'required': True
    },
    'metrics': {
        'validator': validate_metrics
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
        'subjects': {
            'item_title': 'subjects',
        },
        'projects': {
            'item_title': "projects"
        },
        'nodes': {
            'item_title': "nodes"
        }

    }
}


settings['DOMAIN']['subjects']['schema'] = deepcopy(subjects_schema)
settings['DOMAIN']['projects']['schema'] = deepcopy(projects_schema)
settings['DOMAIN']['nodes']['schema'] = deepcopy(nodes_schema)
