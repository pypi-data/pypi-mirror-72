import requests
import urllib.parse
import requests.adapters


class PIDB_v1():
    def __init__(self, api_url):
        if not api_url.endswith('/'):
            raise ValueError('Ifdb V1 api url must end with / e.g.: http://localhost:5000/v1/')

        self.api_url = api_url

    def _do_post_request(self, endpoint, payload):
        req = requests.post(endpoint, json=payload)

        try:
            retval = req.json()
            if retval is None or len(retval) == 0:
                return None
            return retval
        except ValueError:
            return None

    def _do_put_request(self, endpoint, payload):
        req = requests.put(endpoint, json=payload)

        try:
            retval = req.json()
            if retval is None or len(retval) == 0:
                return None
            return retval
        except ValueError:
            return None

    def _do_get_request(self, endpoint, payload=None):
        req = requests.get(endpoint, params=payload)

        try:
            retval = req.json()
            if retval is None or len(retval) == 0:
                return None
            return retval
        except ValueError:
            return None

    def _do_delete_request(self, endpoint, payload=None):
        req = requests.delete(endpoint, params=payload)

        try:
            retcode = req.status_code
            if retcode == 204:
                return True
        except ValueError:
            pass

        return False

    def ping(self):
        try:
            result = self._do_get_request(self.api_url + 'label')
        except Exception:
            return False
        #return result == 'pong'
        return True

    def post_label(self, label_text):
        return self._do_post_request(self.api_url + 'label', {'label_text': label_text})

    def put_label(self, label_text):
        return self._do_put_request(self.api_url + 'label/bylabeltext/{}'.format(urllib.parse.quote_plus(label_text)), {})

    def get_labels(self):
        return self._do_get_request(self.api_url + 'label')

    def put_subject(self, study_id, generator_url):
        return self._do_put_request(self.api_url + 'subject/bystudyid/{}'.format(urllib.parse.quote_plus(study_id)), {'generator_url': generator_url})

    def put_scan(self, experiment_id, subject_age, scan_date):
        return self._do_put_request(self.api_url + 'scan/byexperiment/{}/{}'.format(urllib.parse.quote_plus(experiment_id), urllib.parse.quote_plus(scan_date)), {'subject_age': subject_age})

    def put_experiment(self, subject_id, experiment_date, task_template):
        return self._do_put_request(self.api_url + 'experiment/bysubject/{}/{}'.format(subject_id, experiment_date), {'task_template': task_template})

    def get_experiment(self, experiment_id):
        return self._do_get_request(self.api_url + 'experiment/' + urllib.parse.quote_plus(experiment_id))

    def new_finding(self, experiment_id, label_id, generator_url, task_template):
        return self._do_post_request(self.api_url + 'finding', {'experiment_id': experiment_id, 'label_id': label_id, 'generator_url': generator_url, 'task_template': task_template})

    def put_property(self, label, value, finding_id):
        return self._do_put_request(self.api_url + 'property/byfindingid/{}/{}'.format(finding_id, label), {"value": value})

    def delete_findings_for_experiment_by_template(self, experiment_id, task_template):
        return self._do_delete_request(self.api_url + 'finding/byexperimentidandtemplateproperty/{}/{}'.format(experiment_id,task_template))
