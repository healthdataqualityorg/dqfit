import json
from io import BytesIO
from time import time
from zipfile import ZipFile

import pandas as pd
from flask import Flask, request
from flask_cors import CORS

import dqfit

app = Flask(__name__)
app.debug = True
CORS(app)


@app.route("/cohort-bundles-test", methods=["POST"])
def cohort_zipfile_test():
    t0 = int(time())
    request_json = request.get_json()
    bundles = request_json["bundles"]
    bundles = pd.DataFrame(request_json["bundles"])
    scored_bundles = dqfit.fit_transform(bundles)
    duration = int(time()) - t0
    resp = {
        "patient_level_score": list(scored_bundles["score"]),
        "dqi": scored_bundles["score"].median(),
        "duration": duration,
    }
    return resp


# @app.route("/cohort-zipfile-test", methods=["POST"])
# def cohort_zipfile_test():
#     t0 = int(time())
#     file = request.files['file']
#     print(type(file.read()))
#     zf = ZipFile(BytesIO(file.read()))
#     print("zf loaded")
#     import pdb; pdb.set_trace()
#     bundles = [json.load(zf.read(f)) for f in zf.filelist()[1::]]
#     bundles = pd.DataFrame(bundles)
#     scored_bundles = dqfit.fit_tranform(bundles)
#     duration = int(time()) - t0
#     resp = {
#         "filename": file.filename,
#         "patient_level_score": list(scored_bundles['score']),
#         "dqi": scored_bundles['score'].median(),
#         "duration": duration
#     }
#     return resp
