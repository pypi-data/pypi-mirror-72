import os
from requests.auth import HTTPBasicAuth
import requests
from datetime import datetime, timedelta
import uuid


class Bitbucket():

    def __init__(self, **kwargs):
        pass

    def is_bitbucket(self):
        if os.environ.get('CI', 'false') == 'true':
            return True
        else:
            return False

    def is_pull_request(self):
        if self.is_bitbucket() and os.environ.get('BITBUCKET_PR_ID', None) is not None:
            return True
        else:
            return False

    def branch(self):
        if self.is_bitbucket():
            return os.environ.get('BITBUCKET_BRANCH')
        else:
            return 'master'

    def commit_hash(self):
        return os.environ.get('BITBUCKET_COMMIT', '0' * 30)

    def short_commit_hash(self):
        return os.environ.get('BITBUCKET_COMMIT', '0' * 30)[:7]

    def tag(self):
        return os.environ.get('BITBUCKET_TAG', None)

    def is_tag(self):
        if os.environ.get('BITBUCKET_TAG', False):
            return True
        else:
            return False

    def home_dir(self):
        return os.environ.get('HOME', '/dev/null')

    def build_dir(self):
        return os.environ.get('BITBUCKET_CLONE_DIR', '/dev/null')

    def build_number(self):
        return os.environ.get('BITBUCKET_BUILD_NUMBER', 0)

    def find_pipeline_down(self, branch, number):
        page = 0
        created_on_not_later = datetime.utcnow() - timedelta(hours=1)
        created_on_not_later = created_on_not_later.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        result = list()
        while True:
            page = page + 1
            resp = self._api_get('/pipelines/?sort=-created_on&page={page}'.format(page=page)).json()

            if resp['pagelen'] == 0:
                print('No more results returned form API')
                return result

            for val in resp['values']:
                if val['created_on'] < created_on_not_later:
                    print('Stopping on (1 hour diff): {}: {}'.format(val['build_number'], val['created_on']))
                    return result
                if val['build_number'] >= int(number):
                    print('Skipping (number higher): {}: {}'.format(val['build_number'], val['created_on']))
                    continue

                if (val['target']['ref_type'] == 'branch' and
                        val['target']['ref_name'] == branch and
                        val['state']['name'] == 'IN_PROGRESS'):
                    print('Adding to results {}: {}'.format(val['build_number'], val['created_on']))
                    result.append(val['build_number'])

        return None

    def find_pipeline_up(self, branch, number):
        page = 0
        result = list()
        while True:
            page = page + 1
            resp = self._api_get('/pipelines/?sort=-created_on&page={page}'.format(page=page)).json()

            if resp['pagelen'] == 0:
                print('No more results returned form API')
                return result

            for val in resp['values']:
                if val['build_number'] <= int(number):
                    print('Stopping on (number lower): {}: {}'.format(val['build_number'], val['created_on']))
                    return result

                if (val['target']['ref_type'] == 'branch' and
                        val['target']['ref_name'] == branch and
                        val['state']['name'] == 'IN_PROGRESS'):
                    print('Adding to results {}: {}'.format(val['build_number'], val['created_on']))
                    result.append(val['build_number'])

        return None

    def stop_pipeline(self, number):
        resp = self._api_post('/pipelines/{number}/stopPipeline'.format(number=number))

        if resp.status_code != 204:
            raise Exception("Wasn't able to stop pipeline {}: {}: {}".format(number, r.status_code, r.content))

    def get_variable(self, key):
        page = 0
        result = None

        while True:
            page = page + 1
            resp = self._api_get('/pipelines_config/variables/?page={page}'.format(page=page)).json()

            if resp['pagelen'] == 0:
                print('No more results returned form API')
                return result

            for val in resp['values']:
                if (val['type'] == 'pipeline_variable' and
                        val['key'] == key):
                    result = val
                    print('Varible for name {key} found under uuid {uuid}'.format(key=key, uuid=val['uuid']))
                    return result

        return None

    def save_variable(self, key, value, secured=False):
        page = 0
        result = None

        existing_var = self.get_variable(key)
        if existing_var:
            existing_var['value'] = value
            resp = self._api_put('/pipelines_config/variables/{uuid}'.format(uuid=existing_var['uuid']), existing_var)
            if resp:
                result = resp.json()
        else:
            new_variable = {
                'uuid': '{{{uuid}}}'.format(uuid=uuid.uuid4().hex),
                'key': key,
                'value': value,
                'secured': secured,
            }
            resp = self._api_post('/pipelines_config/variables/', new_variable)
            if resp:
                result = resp.json()

        return result

    def get_cache(self, name):
        page = 0
        result = None

        while True:
            page = page + 1
            resp = self._internal_get('/pipelines_caches/?page={page}'.format(page=page)).json()

            if resp['pagelen'] == 0:
                print('No more results returned form API')
                return result

            for val in resp['values']:
                if (val['name'] == name):
                    result = val
                    print('Cache for name {name} found under uuid {uuid}'.format(name=name, uuid=val['uuid']))
                    return result

        return result

    def find_cache_by_prefix(self, *prefixes):
        page = 0
        result = list()

        while True:
            page = page + 1
            resp = self._internal_get('/pipelines_caches/?page={page}'.format(page=page)).json()

            if resp['pagelen'] == 0:
                print('No more results returned form API')
                return result

            for val in resp['values']:
                for prefix in prefixes:
                    if val['name'].startswith(prefix):
                        result.append(val)
                        print('Cache for prefix {prefix} found under uuid {uuid}'.format(prefix=prefix, uuid=val['uuid']))

        return result

    def delete_cache(self, name):
        cache = self.get_cache(name)
        self._internal_delete('/pipelines_caches/{uuid}'.format(uuid=cache['uuid']))
        print('Cache with name {name} and uuid {uuid} deleted'.format(name=name, uuid=val['uuid']))

    def _api_post(self, url, data=None):
        if not url.startswith('/'):
            url = '/' + url

        resp = requests.post('https://api.bitbucket.org/2.0/repositories/{team}/{repo_name}{url}'.format(
            team=os.environ.get('BITBUCKET_WORKSPACE'),
            repo_name=os.environ.get('BITBUCKET_REPO_SLUG'),
            url=url
        ),
            headers={'Content-Type': 'application/json'},
            auth=HTTPBasicAuth(os.environ.get('BITBUCKET_USERNAME'), os.environ.get('BITBUCKET_PASSWORD')),
            json=data
        )

        if resp.status_code >= 400:
            raise Exception('Response error: code={code}, message={message}'.format(code=resp.status_code, message=resp.content))

        return resp

    def _api_put(self, url, data=None):
        if not url.startswith('/'):
            url = '/' + url

        resp = requests.put('https://api.bitbucket.org/2.0/repositories/{team}/{repo_name}{url}'.format(
            team=os.environ.get('BITBUCKET_WORKSPACE'),
            repo_name=os.environ.get('BITBUCKET_REPO_SLUG'),
            url=url
        ),
            headers={'Content-Type': 'application/json'},
            auth=HTTPBasicAuth(os.environ.get('BITBUCKET_USERNAME'), os.environ.get('BITBUCKET_PASSWORD')),
            json=data
        )

        if resp.status_code >= 400:
            raise Exception('Response error: code={code}, message={message}'.format(code=resp.status_code, message=resp.content))

        return resp

    def _api_get(self, url):
        if not url.startswith('/'):
            url = '/' + url

        resp = requests.get('https://api.bitbucket.org/2.0/repositories/{team}/{repo_name}{url}'.format(
            team=os.environ.get('BITBUCKET_WORKSPACE'),
            repo_name=os.environ.get('BITBUCKET_REPO_SLUG'),
            url=url
        ),
            headers={'Content-Type': 'application/json'},
            auth=HTTPBasicAuth(os.environ.get('BITBUCKET_USERNAME'), os.environ.get('BITBUCKET_PASSWORD'))
        )

        if resp.status_code >= 400:
            raise Exception('Response error: code={code}, message={message}'.format(code=resp.status_code, message=resp.content))

        return resp

    def _internal_get(self, url):
        if not url.startswith('/'):
            url = '/' + url

        resp = requests.get('https://api.bitbucket.org/internal/repositories/{team}/{repo_name}{url}'.format(
            team=os.environ.get('BITBUCKET_WORKSPACE'),
            repo_name=os.environ.get('BITBUCKET_REPO_SLUG'),
            url=url
        ),
            headers={'Content-Type': 'application/json'},
            auth=HTTPBasicAuth(os.environ.get('BITBUCKET_USERNAME'), os.environ.get('BITBUCKET_PASSWORD'))
        )

        if resp.status_code >= 400:
            raise Exception('Response error: code={code}, message={message}'.format(code=resp.status_code, message=resp.content))

        return resp

    def _internal_delete(self, url):
        if not url.startswith('/'):
            url = '/' + url

        resp = requests.delete('https://api.bitbucket.org/internal/repositories/{team}/{repo_name}{url}'.format(
            team=os.environ.get('BITBUCKET_WORKSPACE'),
            repo_name=os.environ.get('BITBUCKET_REPO_SLUG'),
            url=url
        ),
            headers={'Content-Type': 'application/json'},
            auth=HTTPBasicAuth(os.environ.get('BITBUCKET_USERNAME'), os.environ.get('BITBUCKET_PASSWORD'))
        )

        if resp.status_code >= 400:
            raise Exception('Response error: code={code}, message={message}'.format(code=resp.status_code, message=resp.content))

        return resp
