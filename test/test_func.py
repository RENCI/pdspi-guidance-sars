import requests


json_headers = {
    "Accept": "application/json"
}


json_post_headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}


config = {
    "title": "SARS guidance for patient treatment",
    "piid": "pdspi-guidance-sars-treatment",
    "pluginType": "g",
    "settingsDefaults": {
        "pluginSelectors": [ {
            "title": "SARS",
            "id": "PDS:sars",
            "selectorValue": {
                "value": "PDS:sars:treatment",
                "title": "Treatment" }
        }],
        "modelParameters": [ {
            "id": "pdspi-guidance-sars:loc",
            "title": "Hospital location (State)",
            "parameterDescription": "Please choose a state to indicate the hospital location for which you would like to "
                                    "get triage guidance.",
            "parameterValue": {"value": "NC"},
            "legalValues": {
                "type": "string",
                "enum": ["NC", "NY", "PA", "SC", "VA"]}
        } ],
        "patientVariables": [ {
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
            "legalValues": {"type": "string"},
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
            "why": "Shortness of breath is"
                   " one major symptom of SARS"
        } ]
    }
}


guidance = {
    "piid": "pdspi-guidance-sars-treatment",
    "title": "SARS guidance for patient treatment",
    "txid": "38-1",
    "settingsUsed": {
        "timestamp": "2019-12-03T13:41:09.942+00:00",
        "patientVariables": [ {
            "id": "LOINC:30525-0",
            "title": "Age",
            "how": "The value was specified by the end user.",
            "why": "Age is used to calculate the creatinine clearance. Dosing is lower for geriatric patient and contraindicated for pediatric patients",
            "variableValue": {
                "value": "0.5",
                "units": "years"
            },
            "legalValues": {
                "type": "number",
                "minimum": "0"
            }
        },
        {
            "how": "The value was specified by the end user.",
            "id": "LOINC:39156-5",
            "title": "BMI",
            "legalValues": { "type": "number", "minimum": "0" },
            "why": "BMI is used to calculate the creatinine clearance. Dosing is higher for patients with higher BMI",
            "variableValue": {
                "value": "0.5",
                "units": "kg/m^2"
            }
        } ]
    },
    "advanced": [
        {
            "id": "oid-1",
            "name": "Time-series data",
            "description": "Information about time-series data",
            "data": [],
            "specs": []
        }
    ],
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
                            "type": "create",
                            "description": "Create a prescription for Acetaminophen 250 MG",
                            "resource": "MedicationRequest"
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


guidance_input = {
    "piid": "pdspi-guidance-sars-treatment",
    "ptid": "38",
    "settingsRequested": {
        "timestamp": "2019-12-03T13:41:09.942+00:00",
        "modelParameters": [ {
            "id": "pdspi-guidance-sars:loc",
            "title": "Hospital location (State)",
            "parameterDescription": "Please choose a state to indicate the hospital location for which you would like "
                                    "to get triage guidance.",
            "parameterValue": {"value": "NC"}
        } ],
        "patientVariables": [ {
            "id": "LOINC:30525-0",
            "title": "Age",
            "variableValue": {
                "value": "0.5",
                "units": "years"
            },
            "how": "The value was specified by the end user.",
            "timestamp": "2019-12-03T13:41:09.942+00:00"
        }, {
            "id": "LOINC:21840-4",
            "title": "Sex",
            "variableValue": {
              "value": "female"
            },
            "how": "The value was specified by the end user."
          }, {
            "id": "LOINC:39156-5",
            "title": "BMI",
            "variableValue": {
                "value": "0.5",
                "units": "kg/m^2"
            },
            "how": "The value was specified by the end user."
        }, {
        "id": "LOINC:45701-0",
        "title": "Fever",
        "variableValue": {
          "value": True
        },
        "how": "The value was specified by the end user."
      },
      {
        "id": "LOINC:64145-6",
        "title": "Cough",
        "variableValue": {
          "value": True
        },
        "how": "The value was specified by the end user."
      },
      {
        "id": "LOINC:54564-0",
        "title": "Shortness of breath",
        "variableValue": {
          "value": True
        },
        "how": "The value was specified by the end user."
      } ]
    }
}


def test_guidance():
    resp = requests.post("http://pdspi-guidance-sars:8080/guidance", headers=json_post_headers, json=guidance_input)
    resp_output = resp.json()
    assert resp.status_code == 200
    assert "piid" in resp_output
    assert "title" in resp_output
    assert "advanced" in resp_output
    assert "settingsUsed" in resp_output
    assert "cards" in resp_output
    for output in resp_output['advanced']:
        assert "data" in output
        assert "specs" in output


def test_config():
    resp = requests.get("http://pdspi-guidance-sars:8080/config", headers=json_headers)

    assert resp.status_code == 200
    assert resp.json() == config

    
def test_ui():
    resp = requests.get("http://pdspi-guidance-sars:8080/ui")

    assert resp.status_code == 200
