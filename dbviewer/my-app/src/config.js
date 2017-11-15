export default {
  authUrl: 'https://aqueous-reef-70776.herokuapp.com/authenticate/',
  clientId: 'bdf880910c19a91f4a7f',
  redirectUri: 'http://localhost:8080',
  tables: ['projects', 'subjects'],
  url: 'http://ec2-54-218-51-130.us-west-2.compute.amazonaws.com/api/v1/', // 'http://localhost/api/v1',
  projects: {
    sha: {
      type: 'string',
    },
    url: {
      type: 'string',
    },
    scan_parameters: {
      type: 'dict',
    },
  },
  subjects: {
    subjectID: {
      type: 'string',
    },
    sessionID: {
      type: 'string',
    },
    metadata: {
      type: 'dict',
    },
    nodes: {
      type: 'list-dict',
    },
    project_id: {
      type: 'objectid',
      relation: 'projects',
    },
  },
};
