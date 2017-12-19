export default {
  authUrl: 'http://ec2-54-218-51-130.us-west-2.compute.amazonaws.com/api/authenticate/github', // 'https://aqueous-reef-70776.herokuapp.com/authenticate/',
  clientId: '2f0bef2b6cc228ff321b',
  redirectUri: 'data.afqvault.org/',
  tables: ['projects', 'subjects'],
  url: 'http://ec2-54-218-51-130.us-west-2.compute.amazonaws.com/api/v1/', // 'http://localhost/api/v1',
  delete_url: 'http://ec2-54-218-51-130.us-west-2.compute.amazonaws.com/api/delete_project/',
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
    delete: {
      type: 'button',
      action: 'delete',
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
