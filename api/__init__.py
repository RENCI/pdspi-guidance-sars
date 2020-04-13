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
        "id": "pdspi-guidance-sars-triage:loc",
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
            "title": "Recommendation",
            "summary": "The patient has high risk of infection and should be tested for SARS virus with a treatment plan",
            "detail": "some sort of optional GitHub Markdown details",
            "indicator": "critical",
            "source": {
                "label": "Human-readable source label",
                "url": "https://example.com",
                "icon": "https://example.com/img/icon-100px.png"
            },
            "suggestions": [
                {
                    "uuid": "e1187895-ad57-4ff7-a1f1-ccf954b2fe46",
                    "label": "High risk patient",
                    "actions": [
                        {
                            "title": "Diagnosis and treatment",
                            "id": "e1187895-ad57-4ff7-a1f1-ccf954b2fe46-action",
                            "type": "create",
                            "description": "Create a triage plan for patient treatment",
                            "resource": "ProcedureRequest"
                        }
                    ]
                }
            ],
            "selectionBehavior": "1",
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


def generate_vis_outputs(age=None, weight=None, bmi=None, location=None):
    p_loc = location if location else "the patient's location"
    outputs = [
        {
            "id": "oid-1",
            "name": "Active cases",
            "description": "Daily active cases along with model projection for the next week at {}".format(p_loc),
            "data": generate_time_series_data(50),
            "specs": [
                generate_vis_spec("line_chart", "Day", "Total number of active cases",
                                  "Active cases",
                                  "Number of currently infected cases at {} along with model projection for the "
                                  "next week".format(p_loc)),
            ]
        },
        {
            "id": "oid-2",
            "name": "Case growth trend",
            "description": "Daily cases growth trend signified by growth factor at {} along with "
                           "model projection for the next week".format(p_loc),
            "data": generate_multi_time_series_data(50, 2, ['all age group', 'patient age group']),
            "specs": [
                generate_vis_spec("multiple_line_chart", "Day", "Daily cases growth factor",
                                  "Daily cases growth trend",
                                  "Growth factor of daily new cases at {} is computed as every "
                                  "day's new cases divided by new cases on the previous day. A growth factor above 1 "
                                  "indicates an increase while a growth factor between 0 and 1 indicates a decline. "
                                  "A growth factor constantly above 1 could signal exponential growth.".format(p_loc)),
            ]
        },
        {
            "id": "oid-3",
            "name": "Mortality",
            "description": "Patient mortaility projection for the patient age group at {}".format(p_loc),
            "data": generate_scatter_plot_data(100),
            "specs": [
                generate_vis_spec("scatter_plot", "Number of confirmed cases", "Number of deaths",
                                  "Projected patient mortality",
                                  "patient mortality projected by model for the patient age group at {}".format(p_loc))
            ]
        },
        {
            "id": "oid-4",
            "name": "Risk factor by age",
            "description": "Risk factor by age groups at {}".format(p_loc),
            "data": generate_histogram_data(100),
            "specs": [
                generate_vis_spec("histogram", "Age", "Risk factor", "Risk factor by age",
                                  "Risk factor by age prejected by model at {}".format(p_loc))
            ]
        }
    ]
    if bmi:
        outputs.append({
            "id": "oid-5",
            "name": "Risk factor by BMI",
            "description": "Risk factor by BMI at {}".format(p_loc),
            "data": generate_histogram_data(100),
            "specs": [
                generate_vis_spec("histogram", "BMI", "Risk factor", "Risk factor by BMI",
                                  "Risk factor by BMI prejected by model at {}".format(p_loc))
            ]
        })
    outputs.append(
        {
            "id": "oid-6",
            "name": "Clinician to patient plot",
            "description": "Patient to clinician plot at three nearby hospitals",
            "data": generate_multi_scatter_plot_data(50, 3, ['UNC hospital', 'Duke hospital', "WakeMed"]),
            "specs": [
                generate_vis_spec("multiple_scatter_plot", "Number of patients", "Number of clinicians",
                                  "Clinician to patient scatter plot",
                                  "Clinician to patient scatter plot at three nearby hospitals"),
            ]
        })
    outputs.append(
        {
            "id": "oid-7",
            "name": "PPE to clinician plot",
            "description": "PPE to clinician plot at three nearby hospitals",
            "data": generate_multi_scatter_plot_data(50, 3, ['UNC hospital', 'Duke hospital', "WakeMed"]),
            "specs": [
                generate_vis_spec("multiple_scatter_plot", "Number of clinicians", "Number of PPEs",
                                  "PPE to clinician scatter plot",
                                  "PPE to clinician scatter plot at three nearby hospitals"),
            ]
        }
    )
    outputs.append(
        {
            "id": "oid-8",
            "name": "ICU bed to patient plot",
            "description": "ICU bed to patient plot at three nearby hospitals",
            "data": generate_multi_scatter_plot_data(50, 3, ['UNC hospital', 'Duke hospital', "WakeMed"]),
            "specs": [
                generate_vis_spec("multiple_scatter_plot", "Number of patients", "Number of ICU beds",
                                  "ICU bed to patient scatter plot",
                                  "ICU bed to patient scatter plot at three nearby hospitals"),
            ]
        }
    )
    outputs.append(
        {
            "id": "oid-9",
            "name": "Ventilator to patient plot",
            "description": "Ventilator to patient plot at three nearby hospitals",
            "data": generate_multi_scatter_plot_data(50, 3, ['UNC hospital', 'Duke hospital', "WakeMed"]),
            "specs": [
                generate_vis_spec("multiple_scatter_plot", "Number of patients", "Number of ventilators",
                                  "Ventilator to patient scatter plot",
                                  "Ventilator to patient scatter plot at three nearby hospitals"),
            ]
        }
    )
    return outputs


def get_config():
    return config


def get_guidance(body):
    def extract(var, attr):
        return var.get(attr, next(filter(lambda rpv: rpv["id"] == var["id"], config["requiredPatientVariables"]))[attr])

    inputs = []
    location = None
    for var in body["pluginParameterValues"]:
        if var['id'] == 'pdspi-guidance-sars-triage:loc':
            location = var['parameterValue']['value']
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
            "outputs": generate_vis_outputs(age=age, weight=weight, bmi=bmi, location=location)
        }
    }
