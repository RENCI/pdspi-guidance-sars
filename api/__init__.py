import os
import requests

from api.utils import generate_time_series_exponential_growth_data, generate_multi_time_series_exponential_growth_data, \
    generate_scatter_plot_data, generate_multi_scatter_plot_data, generate_histogram_data, get_multi_time_series_data, \
    get_multi_time_series_nytimes_data


pds_host = os.getenv("PDS_HOST", "localhost")
pds_port = os.getenv("PDS_PORT", "8080")
pds_version = os.getenv("PDS_VERSION", "v1")

selector_val = os.getenv("SELECTOR_VALUE", "treatment")
selector_config = {
    "title": "SARS",
    "id": "PDS:sars",
    "selectorValue": {
        "value": "PDS:sars:treatment",
        "title": "Treatment" }
}
summary_card = "Recommend patient be tested for COVID-19 and self-quarantine."
details = "The patient is estimated to have a high risk of infection based on current patient-local " \
          "SARS-CoV-2 spread patterns and reported symptoms and behaviors. Based on current and " \
          "projected capacity and patient disease status, recommend to test the patient for COVID-19 " \
          "and isolate at home until results are received."
suggestion_card = {
    "uuid": "e1187895-ad57-4ff7-a1f1-ccf954b2fe46",
    "label": "High risk patient",
    "actions": [
        {
            "type": "create",
            "description": "Create an order for a diagnostic test for COVID19",
            "resource": "DiagnosticOrder"
        }
    ]
}

piid = "pdspi-guidance-sars-treatment"
pi_title = "SARS guidance for patient treatment"

if selector_val == 'resource':
    piid = "pdspi-guidance-sars-resource"
    pi_title = "SARS guidance for resource management"
    selector_config = {
        "title": "SARS",
        "id": "PDS:sars",
        "selectorValue": {
            "value": "PDS:sars:resource",
            "title": "Resource"}
    }
    summary_card = "Recommend 70% of clinicians change their PPE."
    details = "Recommend 70% of clinicians change their PPE based on current patient-local SARS-CoV-2 spread " \
              "patterns, patient disease status, and current and projected PPE capacity."
    suggestion_card = {
        "uuid": "e1187895-ad57-4ff7-a1f1-ccf954b2fe46",
        "label": "Change PPE",
        "actions": [
            {
                "type": "create",
                "description": "Create a resource management plan for clinicians to change PPE",
                "resource": "ProcedureRequest"
            }
        ]
    }

config = {
    "title": pi_title,
    "piid": piid,
    "pluginType": "g",
    "pluginSelectors": [
        selector_config
    ],
    "pluginParameterDefaults": [ {
        "id": "pdspi-guidance-sars:loc",
        "title": "Hospital location (State)",
        "parameterDescription": "Please choose a state to indicate the hospital location for which you would like to get triage guidance.",
        "parameterValue": { "value": "NC" },
        "legalValues": {
            "type": "string",
            "enum": [ "NC", "NY", "PA", "SC", "VA"] }
    } ],
    "requiredPatientVariables": [ {
        "id": "LOINC:30525-0",
        "title": "Age",
        "legalValues": { "type": "number", "minimum": "0" },
        "group": "Profile",
        "why": "Age is used to assess patient risk for SARS"
    },
    {
        "id": "LOINC:21840-4",
        "title": "Sex",
        "legalValues": { "type": "string", "enum": ['female', 'male'] },
        "group": "Profile",
        "why": "Sex is used to assess patient risk for SARS"
    },
    {
        "id": "LOINC:39156-5",
        "title": "BMI",
        "legalValues": { "type": "number", "minimum": "0" },
        "group": "Profile",
        "why": "BMI is used to assess patient risk for SARS"
    },
    {
        "id": "LOINC:LP21258-6",
        "title": "Oxygen saturation",
        "group": "Profile",
        "legalValues": { "type": "number", "minimum": "0" },
        "why": "Oxygen saturation is used to assess patient risk for SARS."
    },
    {
        "id": "LOINC:56799-0",
        "title": "Address",
        "group": "Profile",
        "legalValues": { "type": "string" },
        "why": "Address of the patient's residence is used to assess patient risk for SARS."
    },
    {
        "id": "LOINC:LP172921-1",
        "title": "Cardiovascular disease",
        "group": "Pre-existing Condition",
        "legalValues": { "type": "boolean" },
        "why": "cardiovascular disease pre-existing condition is used to assess patient risk for SARS."
    },
    {
        "id": "LOINC:54542-6",
        "title": "Pulmonary disease",
        "group": "Pre-existing Condition",
        "legalValues": { "type": "boolean" },
        "why": "pulmonary disease pre-existing condition is used to assess patient risk for SARS."
    },
    {
        "id": "LOINC:LP128504-0",
        "title": "Autoimmune disease",
        "group": "Pre-existing Condition",
        "legalValues": { "type": "boolean" },
        "why": "Autoimmune disease pre-existing condition is used to assess patient risk for SARS."
    },
    {
        "id": "LOINC:45701-0",
        "title": "Fever",
        "legalValues": { "type": "boolean"},
        "group": "Symptom",
        "why": "Fever is one major symptom of SARS"
    },
    {
        "id": "LOINC:LP212175-6",
        "title": "Date of fever onset",
        "legalValues": { "type": "string"},
        "group": "Symptom",
        "why": "Date of fever onset info is important for SARS patient risk assessment"
    },
    {
        "id": "LOINC:64145-6",
        "title": "Cough",
        "legalValues": { "type": "boolean"},
        "group": "Symptom",
        "why": "Cough is one major symptom of SARS"
    },
    {
        "id": "LOINC:85932-2",
        "title": "Date of cough onset",
        "legalValues": { "type": "string"},
        "group": "Symptom",
        "why": "Date of cough onset info is important for SARS patient risk assessment"
    },
    {
        "id": "LOINC:54564-0",
        "title": "Shortness of breath",
        "legalValues": { "type": "boolean"},
        "group": "Symptom",
        "why": "Shortness of breath is one major symptom of SARS"
    } ]
}

guidance = {
    "piid": piid,
    "title": "SARS guidance",
    "txid": "38-1",
    "cards": [
        {
            "id": "string",
            "title": "Recommendation",
            "summary": summary_card,
            "detail": details,
            "indicator": "critical",
            "source": {
                "label": "PDS SARS guidance",
                "url": "https://github.com/renci/pdspi-guidance-sars",
                "icon": "https://txscience.renci.org/wp-content/uploads/2019/08/cropped-Web-Logo-5.png"
            },
            "suggestions": [
                suggestion_card
            ],
            "selectionBehavior": "1",
            "links": [
                {
                    "label": "Priorities for testing patients with suspected COVID-19 infection",
                    "url": "https://www.cdc.gov/coronavirus/2019-ncov/downloads/priority-testing-patients.pdf",
                    "type": "absolute"
                }
            ]
        }
    ]
}


def generate_vis_spec(typeid, x_axis_title, y_axis_title, chart_title, chart_desc, time_unit=''):
    json_post_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    vega_spec_input = {
        "typeid": typeid,
        "x_axis_title": x_axis_title,
        "y_axis_title": y_axis_title,
        "chart_title": chart_title,
        "chart_description": chart_desc,
        "time_unit": time_unit
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
            "name": "Active cases and deaths",
            "description": "Daily active cases and deaths at {}".format(p_loc),
            "data": get_multi_time_series_nytimes_data(state=location if location else 'NC'),
            "specs": [
                generate_vis_spec("multiple_line_chart", "Date", "Number of people",
                                  "Active cases and deaths",
                                  "Number of currently infected cases and deaths at {}.".format(p_loc),
                                  "monthdate")
            ]
        }
    ]
    if selector_val == 'treatment':
        outputs.append({
            "id": "oid-2",
            "name": "Epidemics trend prediction",
            "description": "SIR (Susceptible-Infected-Removed) predictions for the next "
                           "60 days at {}".format(p_loc),
            "data": get_multi_time_series_data(state=location if location else 'NC'),
            #"data": generate_multi_time_series_exponential_growth_data(50, 2, ['all age group', 'patient age group']),
            "specs": [
                generate_vis_spec("multiple_line_chart", "Date (Days since March 24)", "Number of people",
                                  "Infected, recovered, susceptible, dead predictions",
                                  "Use Penn Death model to make SIR (Susceptible-Infected-Removed) predictions for "
                                  "the next 60 days at {} given the number of susceptible, infected, recovered, and "
                                  "death today".format(p_loc))
            ]
        })
        outputs.append({
            "id": "oid-3",
            "name": "Mortality",
            "description": "Patient mortality projection for the patient age group at {}".format(p_loc),
            "data": generate_scatter_plot_data(100),
            "specs": [
                generate_vis_spec("scatter_plot", "Number of confirmed cases", "Number of deaths",
                                  "Projected patient mortality",
                                  "patient mortality projected by model for the patient age group at {}".format(p_loc))
            ]
        })
        outputs.append({
            "id": "oid-4",
            "name": "Risk factor by age",
            "description": "Risk factor by age groups at {}".format(p_loc),
            "data": generate_histogram_data(100),
            "specs": [
                generate_vis_spec("histogram", "Age", "Risk factor", "Risk factor by age",
                                  "Risk factor by age prejected by model at {}".format(p_loc))
            ]
        })
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
    else:
        # resource management
        outputs.append({
            "id": "oid-2",
            "name": "Hospital resource usage",
            "description": "Projected hospital resource usage at {}".format(p_loc),
            "data": get_multi_time_series_data(state=location if location else 'NC', type='Hospital Use'),
            #"data": generate_multi_time_series_exponential_growth_data(50, 3, ['ICU beds', 'Ventilators', 'All resources']),
            "specs": [
                generate_vis_spec("multiple_line_chart", "Date (Days since March 24)", "Number of people",
                                  "Hospital resources usage",
                                  "Projected hospital resource usage at {}".format(p_loc)),
            ]
        })
        outputs.append(
            {
                "id": "oid-6",
                "name": "Clinician to patient plot",
                "description": "Patient to clinician plot at three nearby hospitals",
                "data": generate_multi_scatter_plot_data(50, 4, ['UNC hospital', 'Duke hospital', "WakeMed",
                                                                 "Mobile hospitals"]),
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
                "data": generate_multi_scatter_plot_data(50, 4, ['UNC hospital', 'Duke hospital', "WakeMed",
                                                                 "Mobile hospitals"]),
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
                "data": generate_multi_scatter_plot_data(50, 3, ['UNC hospital', 'Duke hospital', "WakeMed",
                                                                 "Mobile hospitals"]),
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
                "data": generate_multi_scatter_plot_data(50, 3, ['UNC hospital', 'Duke hospital', "WakeMed",
                                                                 "Mobile hospitals"]),
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
        if var['id'] == 'pdspi-guidance-sars:loc':
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
