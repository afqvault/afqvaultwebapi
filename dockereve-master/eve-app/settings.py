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

def validate_nodes(field, value, error):
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
    'sessionID': {
        'type': 'string',
        'required': True
    },
    "metadata": {
        'validator': validate_metrics
    },
    "nodes": {
        'validator': validate_nodes
    },
    'project_id': {
        'type': 'objectid',
        'required': True,
        'data_relation': {
            'resource': 'projects',
            'field': '_id',
            'embeddable': True
        },
    },
}

projects_schema = {
    'projectID': {
        'type': 'string',
        'required': True,
        'unique': True
    },
    'doi': {
        'type': 'string',
        'required': False
    },
    'url': {
        'type': 'string',
        'required': False
    },
    'scan_parameters': {
        'validator': validate_metrics
    },
}

#TODO: kill this and dump w/ subjects

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
    },
    'subject_id': {
        'type': 'objectid',
        'required': True,
        'data_relation': {
            'resource': 'subjects',
            'field': '_id',
            'embeddable': True
        },
    },
}




settings = {
    'URL_PREFIX': 'api',
    'API_VERSION': 'v1',
    'ALLOWED_FILTERS': ['*'],
    'MONGO_HOST': os.environ.get('MONGODB_HOST', ''),
    'MONGO_PORT': os.environ.get('MONGODB_PORT', ''),
    'MONGO_DBNAME': 'mriqc_api',
    'PUBLIC_METHODS': ['GET'],
    'PUBLIC_ITEM_METHODS': ['GET', 'PATCH'],
    'RESOURCE_METHODS': ['GET', 'POST'],
    'ITEM_METHODS': ['GET', 'PATCH'],
    'X_DOMAINS': '*',
    'DOMAIN': {
        'subjects': {
            'item_title': 'subjects',
        },
        'projects': {
            'item_title': "projects"
        },

    }
}


settings['DOMAIN']['subjects']['schema'] = deepcopy(subjects_schema)
settings['DOMAIN']['projects']['schema'] = deepcopy(projects_schema)

settings['X_DOMAINS'] = '*'
settings['X_HEADERS'] = ['Authorization', 'X-Requested-With', "Content-type"]
