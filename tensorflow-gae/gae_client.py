import json
import urllib2

#url = "http://localhost:8080/predict/"

url = "https://babyweight-estimator-dot-ksalama-gcp-playground.appspot.com/predict/"

data = {
    "instance": {
        "is_male": "True",
        "mother_age": 26.0,
        "mother_race": "Asian Indian",
        "plurality": 1.0,
        "gestation_weeks": 39,
        "mother_married": "True",
        "cigarette_use": "False",
        "alcohol_use": "False"
    }
}

request = urllib2.Request(url, json.dumps(data), headers={'Content-type': 'application/json', 'Accept': 'application/json'})
response = urllib2.urlopen(request)
result = response.read()

print result