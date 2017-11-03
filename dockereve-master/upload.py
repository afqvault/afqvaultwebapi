import pandas as pd
import requests
import simplejson as json
from copy import deepcopy

url_tmpl = "http://localhost/api/v1/{}" #subjects" #"http://ec2-54-218-51-130.us-west-2.compute.amazonaws.com/api/v1/subjects"
secret_password = "PHNlY3JldF90b2tlbj46"

headers = {
    'content-type': "application/json",
    'authorization': "Basic {}".format(secret_password),
    'cache-control': "no-cache",
    }

def upload_subjects(df, projectID, sessionID=0):
    subj_data = df.to_dict("records")
    data = []
    for sub in subj_data:
      entry = {"projectID": projectID, "sessionID": sessionID}
      sid = sub.pop("subjectID")
      entry["subjectID"] = sid
      entry["demographics"] = {}
      for key, val in sub.items():
        if not pd.isnull(val):
          entry["demographics"][key] = val
      data.append(entry)

      payload = json.dumps(data)
      response = requests.request("POST", url_tmpl.format("subjects"), data=payload, headers=headers)
      assert response.ok, response.text
      output = json.loads(response.text)["_items"]
      for i, out in enumerate(output):
          out["subjectID"] = data[i]["subjectID"]
      return output

def upload_nodes(df_node):
    data = []
    for node in df_node.to_dict("records"):
        entry = {}
    for key in ["subjectID", "tractID", "nodeID"]:
        entry[key] = str(node.pop(key))
    entry["metrics"] = {}
    for key, value in node.items():
        if not pd.isnull(value):
            entry["metrics"][key] = value
    data.append(entry)

    response = requests.request("POST", url_tmpl.format("nodes"), data=json.dumps(data),
                              headers=headers)

    assert response.ok, response.text

def upload_project(projectID, doi="", url="", scan_parameters={}):
    # see if the project is already there. If not, POST it
    response = requests.request("GET", url_tmpl.format("projects"),
                                headers=headers)
    assert response.ok, response.text

    res = json.loads(response.text)["_items"]

    if not len(res):
        payload = {"projectID": projectID,
                   "doi": doi,
                   "url": url,
                   "scan_parameters": scan_parameters
                    }

        response = requests.request("POST", url_tmpl.format("projects"),
                                    data=json.dumps(payload),
                                    headers=headers)
        assert response.ok, response.text
        res = json.loads(response.text)


        return res["_items"]

    else:
        print("Found existing project. PATCHING data")
        etag = res[0]["_etag"]
        doc_id = res[0]["_id"]
        patch_header = deepcopy(headers)
        patch_header["if-match"] = etag
        url = url_tmpl.format("projects/{}".format(doc_id))
        payload = {
                   "doi": doi,
                   "url": url,
                   "scan_parameters": scan_parameters
                  }
        response = requests.request("PATCH", url, data=json.dumps(payload), headers=patch_header)
        assert response.ok, "ERROR\n\n"+response.text
        return json.loads(response.text)


subjects_csv = "https://yeatmanlab.github.io/AFQBrowser-demo/data/subjects.csv"
nodes_path = "https://yeatmanlab.github.io/AFQBrowser-demo/data/nodes.csv"
scan_params_path = "" #TODO: fill this in

df = pd.read_csv(subjects_csv, index_col=0)
df_node = pd.read_csv(nodes_path)

#upload_subjects(df, "test_project")
#upload_nodes(df_node)
project_info = upload_project("test", doi="4567")
print(project_info)
