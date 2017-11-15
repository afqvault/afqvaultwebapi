import pandas as pd
import requests
import simplejson as json
from copy import deepcopy

# url_tmpl = "http://localhost/api/v1/{}"
url_tmpl = "http://ec2-54-218-51-130.us-west-2.compute.amazonaws.com/api/v1/{}"
secret_password = "PHNlY3JldF90b2tlbj46"

headers = {
    'content-type': "application/json",
    'authorization': "Basic {}".format(secret_password),
    'cache-control': "no-cache",
    }


def upload_subjects(df, df_node, project_id, sessionID="0"):
    subj_data = df.to_dict("records")
    data = []
    for sub in subj_data:
        entry = {"project_id": project_id, "sessionID": sessionID}
        sid = sub.pop("subjectID")
        entry["subjectID"] = sid
        entry["metadata"] = {}
        for key, val in sub.items():
            if not pd.isnull(val):
                entry["metadata"][key] = val

        snode = df_node[df_node.subjectID == sid]
        node_data = format_nodes(snode)
        entry["nodes"] = node_data
        data.append(entry)
        query = url_tmpl.format('subjects?where={"project_id": "%s", \
        "subjectID":"%s"}' % (project_id, sid))
        print(query)
        response = requests.request("GET", query,
                                    headers=headers)
        assert response.ok, response.text

        res = json.loads(response.text)["_items"]
        payload = json.dumps(entry)

        if not len(res):
            response = requests.request("POST",
                                        url_tmpl.format("subjects"),
                                        data=payload, headers=headers)
            assert response.ok, response.text
            output = json.loads(response.text)
            data.append(output)
        else:
            etag = res[0]["_etag"]
            doc_id = res[0]["_id"]
            patch_header = deepcopy(headers)
            patch_header["if-match"] = etag
            url = url_tmpl.format("subjects/{}".format(doc_id))

            response = requests.request("PATCH", url, data=json.dumps(payload),
                                        headers=patch_header)
            assert response.ok, "ERROR\n\n"+response.text
            data.append(json.loads(response.text))

    return data


def format_nodes(df_node):
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

    return data


def upload_project(sha, purl, scan_parameters={}):
    # see if the project is already there. If not, POST it
    query = url_tmpl.format("projects?where=sha=='{}'".format(sha))
    response = requests.request("GET", query,
                                headers=headers)
    assert response.ok, response.text

    res = json.loads(response.text)["_items"]
    print(res)

    if not len(res):
        payload = {"sha": sha,
                   "url": purl,
                   "scan_parameters": scan_parameters
                   }

        response = requests.request("POST", url_tmpl.format("projects"),
                                    data=json.dumps(payload),
                                    headers=headers)
        assert response.ok, response.text
        res = json.loads(response.text)

        return res

    else:
        print("Found existing project. PATCHING data")
        etag = res[0]["_etag"]
        doc_id = res[0]["_id"]
        patch_header = deepcopy(headers)
        patch_header["if-match"] = etag
        url = url_tmpl.format("projects/{}".format(doc_id))
        payload = {
                   "sha": sha,
                   "url": url,
                   "scan_parameters": scan_parameters
                  }
        response = requests.request("PATCH", url, data=json.dumps(payload),
                                    headers=patch_header)
        assert response.ok, "ERROR\n\n"+response.text
        return json.loads(response.text)


subjects_csv = "https://yeatmanlab.github.io/AFQBrowser-demo/data/subjects.csv"
nodes_path = "https://yeatmanlab.github.io/AFQBrowser-demo/data/nodes.csv"
scan_params_path = ""  # TODO: fill this in

df = pd.read_csv(subjects_csv, index_col=0)
df_node = pd.read_csv(nodes_path)

project_info = upload_project("some_sha",
                              purl="http://github.com/akeshavan/")
upload_subjects(df, df_node, project_info["_id"])
print(project_info)
