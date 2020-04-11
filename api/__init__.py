import os
import requests

from api.utils import generate_time_series_data, generate_multi_time_series_data, generate_scatter_plot_data, \
    generate_multi_scatter_plot_data, generate_histogram_data, generate_dosing_data


pds_host = os.getenv("PDS_HOST", "localhost")
pds_port = os.getenv("PDS_PORT", "8080")
pds_version = os.getenv("PDS_VERSION", "v1")

config = {
    "title": "SARS Triage guidance",
    "piid": "pdspi-sars-triage",
    "pluginType": "g",
    "pluginSelectors": [ {
        "title": "Type",
        "id": "PDS:sars-covid-19",
        "selectorValue": {
            "value": "covid-19",
            "title": "Covid-19" }
    } ],
    "pluginParameterDefaults": [ {
        "id": "pdspi-guidance-sars-triage:1",
        "title": "Location (State)",
        "parameterDescription": "Please choose a state to indicate the location for which you would like to get triage guidance.",
        "parameterValue": { "value": "NC" },
        "legalValues": {
            "type": "string",
            "enum": [ "NC", "NY", "PA", "SC", "VA"] }
    } ],
    "requiredPatientVariables": [ {
        "id": "LOINC:30525-0",
        "title": "Age",
        "legalValues": { "type": "number", "minimum": "0" },
        "why": "Age is used to assess patient risk for Covid-19."
    },
    {
        "id": "LOINC:21840-4",
        "title": "Sex",
        "legalValues": { "type": "string" },
        "why": "Sex is used to assess patient risk for Covid-19."
    },
    {
        "id": "LOINC:39156-5",
        "title": "BMI",
        "legalValues": { "type": "number", "minimum": "0" },
        "why": "BMI is used to assess patient risk for Covid-19."
    },
    {
      "id": "LOINC:45701-0",
      "title": "Fever",
      "legalValues": { "type": "boolean"},
      "why": "Fever is one major symptom of Covid-19"
    },
    {
      "id": "LOINC:64145-6",
      "title": "Cough",
      "legalValues": { "type": "boolean"},
      "why": "Cough is one major symptom of Covid-19"
    },
    {
      "id": "LOINC:54564-0",
      "title": "Shortness of breath",
      "legalValues": { "type": "boolean"},
      "why": "Shortness of breath is one major symptom of Covid-19"
    } ]
}

guidance = {
    "piid": "pdspi-guidance-sars-triage",
    "title": "SARS triage guidance",
    "txid": "38-1",
    "cards": [
        {
            "id": "string",
            "title": "string",
            "summary": "some <140 char Summary Message",
            "detail": "some sort of optional GitHub Markdown details",
            "indicator": "info",
            "source": {
                "label": "Human-readable source label",
                "url": "https://example.com",
                "icon": "https://example.com/img/icon-100px.png"
            },
            "suggestions": [
                {
                    "uuid": "e1187895-ad57-4ff7-a1f1-ccf954b2fe46",
                    "label": "Human-readable suggestion label",
                    "actions": [
                        {
                            "title": "string",
                            "id": "string",
                            "type": "create",
                            "description": "Create a triage plan for the patient",
                            "resource": "ResourceRequest"
                        }
                    ]
                }
            ],
            "selectionBehavior": "string",
            "links": [
                {
                    "label": "SMART Example App",
                    "url": "string",
                    "type": "string",
                    "appContext": "string"
                }
            ]
        }
    ]
}


def generate_vis_spec(typeid, x_axis_title, y_axis_title, chart_title, chart_desc):
    json_post_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    vega_spec_input = {
        "typeid": typeid,
        "x_axis_title": x_axis_title,
        "y_axis_title": y_axis_title,
        "chart_title": chart_title,
        "chart_description": chart_desc
    }
    url_str = "http://{}:{}/{}/plugin/tx-vis/vega_spec".format(pds_host, pds_port, pds_version)
    resp = requests.post(url_str, headers=json_post_headers, json=vega_spec_input)
    # resp = requests.post("http://tx-vis:8080/vega_spec", headers=json_post_headers, json=vega_spec_input)
    if resp.status_code == 200:
        return resp.json()
    else:
        return {}


def generate_vis_outputs(age=None, weight=None, bmi=None):
    outputs = [
        {
            "id": "oid-1",
            "name": "Daily confirmed new cases",
            "description": "Daily confirmed new case outbreak evolution at the patient's location",
            "data": generate_time_series_data(50),
            "specs": [
                generate_vis_spec("line_chart", "Time", "Number of confirmed new cases",
                                  "outbreak evolution",
                                  "Outbreak evolution at the patient's location"),
            ]
        },
        {
            "id": "oid-2",
            "name": "Patient to clinician ratios",
            "description": "Patient to clinician ratios at four nearby hospitals",
            "data": generate_multi_time_series_data(50, 4),
            "specs": [
                generate_vis_spec("multiple_line_chart", "Number of patients", "Number of clinician",
                                  "Patient to clinician ratio",
                                  "Patient to clinician ratio at four nearby hospitals"),
            ]
        },
        {
            "id": "oid-3",
            "name": "PPE to clinician ratios",
            "description": "PPE to clinician ratios at four nearby hospitals",
            "data": generate_multi_time_series_data(50, 4),
            "specs": [
                generate_vis_spec("multiple_line_chart", "Number of clinician", "Number of PPEs",
                                  "PPE to clinician ratio",
                                  "PPE to clinician ratio at four nearby hospitals"),
            ]
        },
        {
            "id": "oid-4",
            "name": "patient to ICU bed ratios",
            "description": "Patients to ICU bed ratios at four nearby hospitals",
            "data": generate_multi_time_series_data(50, 4),
            "specs": [
                generate_vis_spec("multiple_line_chart", "Number of patients", "Number of beds",
                                  "Patient to ICU bed ratio",
                                  "Patient to ICU bed ratio at four nearby hospitals"),
            ]
        },
        {
            "id": "oid-5",
            "name": "Patient mortality data",
            "description": "Patient mortaility analysis in the age group",
            "data": generate_scatter_plot_data(100),
            "specs": [
                generate_vis_spec("scatter_plot", "Confirmed cases", "Deaths", "Patient mortality", "Patient mortality analysis")
            ]
        },
        {
            "id": "oid-6",
            "name": "Patients by age",
            "description": "Patients by age informatoin",
            "data": generate_histogram_data(100),
            "specs": [
                generate_vis_spec("histogram", "Age", "Number of confirmed cases", "Histogram", "Confirmed cases by age")
            ]
        }
    ]
    return outputs


def get_config():
    return config


def get_guidance(body):
    def extract(var, attr):
        return var.get(attr, next(filter(lambda rpv: rpv["id"] == var["id"], config["requiredPatientVariables"]))[attr])

    inputs = []
    age = None
    weight = None
    bmi = None
    for var in body["userSuppliedPatientVariables"]:
        if var['id'] == 'LOINC:30525-0':
            age = var["variableValue"]['value']
        elif var['id'] == 'LOINC:29463-7':
            weight = var["variableValue"]['value']
        elif var['id'] == 'LOINC:39156-5':
            bmi = var["variableValue"]['value']
        inputs.append({
            "id": var["id"],
            "title": extract(var, "title"),
            "how": var["how"],
            "why": extract(var, "why"),
            "variableValue": var["variableValue"],
            "legalValues": extract(var, "legalValues"),
            "timestamp": var.get("timestamp", "2020-02-18T18:54:57.099Z")
        })
    return {
        **guidance,
        "justification": {
            "inputs": inputs,
            "outputs": generate_vis_outputs(age=age, weight=weight, bmi=bmi)
        }
    }
