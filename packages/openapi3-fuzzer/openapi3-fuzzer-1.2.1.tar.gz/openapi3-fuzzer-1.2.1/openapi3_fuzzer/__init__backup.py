from flask_testing import TestCase
import json
import os
import re
from time import sleep
from typing import List, Dict
from prance import ResolvingParser


def do_post_req(mytestcase, ep, headers, payload):
    """
    Perform an actual POST request
    returns the response object r
    """
    self = mytestcase
    try:
        # print("--- Starting POST request to {}".format(ep))
        sleep(0.05)
        r = self.client.open(
            ep,
            method='POST',
            data=json.dumps(payload),
            headers=headers)
    except Exception as e:
        print("Exception connecting to {} with {}".format(ep, str(e)))
        return {"status_code": -1, "content": ""}
    else:
        return r


def do_get_req(mytestcase, ep, headers):
    """
    Perform an actual GET request
    returns the response object r
    """
    self = mytestcase
    try:
        # print("--- Starting GET request to {}".format(ep))
        sleep(0.05)
        r = self.client.open(
            ep,
            method='GET',
            headers=headers)
    except Exception as e:
        print("    Exception connecting to {} with {}".format(ep, str(e)))
        return {"status_code": -1, "content": ""}
    else:
        return r

def do_put_req(mytestcase, ep, headers, payload):
    """
    Perform an actual POST request
    returns the response object r
    """
    self = mytestcase
    try:
        # print("--- Starting POST request to {}".format(ep))
        sleep(0.05)
        r = self.client.open(
            ep,
            method='PUT',
            data=json.dumps(payload),
            headers=headers)
    except Exception as e:
        print("Exception connecting to {} with {}".format(ep, str(e)))
        return {"status_code": -1, "content": ""}
    else:
        return r


def do_request(method, my_testcase, entry_point, headers, payload=None):
    """
    Perform an actual HTTP equest
    returns the response object r
    """
    test_case = my_testcase
    try:
        # print("--- Starting POST request to {}".format(ep))
        sleep(0.05)
        r = test_case.client.open(
            entry_point,
            method=method.upper(),
            data=json.dumps(payload),
            headers=headers)
    except Exception as e:
        print("Exception connecting to {} with {}".format(entry_point, str(e)))
        return {"status_code": -1, "content": ""}
    else:
        return r


def get_happyday_pattern(datatype):
    fuzzdbfile = "{}/fuzz/fuzz-{}.txt".format(os.path.dirname(os.path.realpath(__file__)),
                                              re.sub(r'[^a-zA-Z]', '', datatype))
    fuzzdbfallbackfile = "{}/fuzz/fuzz-fallback.txt".format(os.path.dirname(os.path.realpath(__file__)))
    happydaystring = ""
    if os.path.exists(fuzzdbfile):
        with open(fuzzdbfile) as f:
            happydaystring = f.readlines()[0].rstrip()
    elif os.path.exists(fuzzdbfallbackfile):
        with open(fuzzdbfallbackfile) as f:
            happydaystring = f.readlines()[0].rstrip()
    else:
        happydaystring = "AAAAAAAAAstaticfallbackoffallbackstring"
        raise FileNotFoundError
    return happydaystring


def get_fuzz_patterns(datatype):
    fuzzdbfile = "{}/fuzz/fuzz-{}.txt".format(os.path.dirname(os.path.realpath(__file__)),
                                              re.sub(r'[^a-zA-Z]', '', datatype))
    fuzzdbfallbackfile = "{}/fuzz/fuzz-fallback.txt".format(os.path.dirname(os.path.realpath(__file__)))
    lines = []
    if os.path.exists(fuzzdbfile):
        with open(fuzzdbfile) as f:
            lines = f.readlines()
    elif os.path.exists(fuzzdbfallbackfile):
        with open(fuzzdbfallbackfile) as f:
            lines = f.readlines()
    else:
        lines = "AAAAAAAAAstaticfallbackoffallbackstring"
        raise FileNotFoundError
    return lines


def generate_happy_day_url_from_pathvars(baseurl, path, pathvars):
    """
    From a given OAS3 endpoint with path parameters,
    generate 1 URL while substituting all params with happy day strings
    """
    url = "{}{}".format(baseurl, path)
    if pathvars is not None:
        for pathvar in pathvars:
            datatype = pathvar.get("schema", {}).get("type", "fallback")
            happydaystring = get_happyday_pattern(datatype)
            url = url.replace("{{{}}}".format(
                pathvar.get("name")), happydaystring.rstrip())
    return url


def generate_urls_from_pathvars(baseurl, path, pathvars):
    """
    From a given OAS3 endpoint with path parameters,
    generate all the possible URLs to fuzz
    while only substituting 1 param with all fuzzing entries
    and using happy day strings for the other parameters
    """
    urls = set()
    for pathvar in pathvars:
        if pathvar.get('in', None) == 'path' and 'name' in pathvar.keys():
            datatype = pathvar.get("schema", {}).get("type", "fallback")
            lines = get_fuzz_patterns(datatype)
            for line in lines:
                url = "{}{}".format(baseurl, path)
                url = url.replace("{{{}}}".format(
                    pathvar.get("name")), line.rstrip())
                for otherpathvar in pathvars:
                    datatype = otherpathvar.get(
                        "schema", {}).get("type", "fallback")
                    happydaystring = get_happyday_pattern(datatype)
                    url = url.replace("{{{}}}".format(
                        otherpathvar.get("name")), happydaystring.rstrip())
                urls.add(url)
    return urls


def generate_payloads_from_request_vars(request_vars) -> List[Dict[str, str]]:
    """
    From a given OAS3 dict of requestBody variables
    generate a list of payload dicts
    """
    payloads = []
    payload = {}

    for jsontype in ["int", "str", "arr", "none"]:
        for fuzzparam in request_vars.keys():
            datatype = request_vars.get(fuzzparam, {}).get("type", "fallback")
            lines = get_fuzz_patterns(datatype)
            for line in lines:
                payload = {}
                for param in request_vars.keys():
                    datatype = request_vars.get(param, {}).get("type", "")
                    happydaystring = get_happyday_pattern(datatype)
                    if param == fuzzparam:
                        if jsontype == "int" or datatype == "int" or \
                                datatype == "number":
                            try:
                                payload[param] = int(line.rstrip())
                            except ValueError:
                                payload[param] = line.rstrip()
                        elif jsontype == "str":
                            payload[param] = line.rstrip()
                    else:
                        if datatype == "int" or datatype == "number":
                            try:
                                payload[param] = int(happydaystring)
                            except ValueError:
                                payload[param] = happydaystring
                        else:
                            payload[param] = happydaystring
                payloads.append(payload)
    payloads_uniq = []
    for payload in payloads:
        if payload not in payloads_uniq:
            payloads_uniq.append(payload)
    return payloads_uniq


def do_post_fuzzing(*args, **kwargs):
    baseurl = kwargs.get('baseurl', "")
    headers = kwargs.get('headers', {})
    path = kwargs.get('path', None)
    pathvars = kwargs.get('pathvars', {})
    postvars = kwargs.get('postvars', {})
    responses = kwargs.get('responses', [])
    test_case = kwargs.get('mytestcase', None)

    newresponses = []
    for response in responses:
        try:
            newresponses.append(int(response))
        except ValueError:
            newresponses.append(response)
    responses = newresponses

    # Generate url once
    url = generate_happy_day_url_from_pathvars(baseurl, path, pathvars)
    payloads = generate_payloads_from_request_vars(postvars)

    # And send multiple payloads
    for payload in payloads:
        with test_case.subTest(method="POST", url=url, payload=payload,
                               headers=headers):
            result = do_post_req(test_case, url, headers, payload)
            test_case.assertLess(result.status_code, 500)
            test_case.assertIn(result.status_code, responses)
    return True


def do_get_fuzzing(*args, **kwargs):
    """
    Perform fuzzing on a GET endpoint
    """
    baseurl = kwargs.get('baseurl', "")
    headers = kwargs.get('headers', {})
    path = kwargs.get('path', None)
    pathvars = kwargs.get('pathvars', {})
    responses = kwargs.get('responses', [])
    test_case = kwargs.get('mytestcase', None)

    newresponses = []
    for response in responses:
        try:
            newresponses.append(int(response))
        except ValueError:
            newresponses.append(response)
    responses = newresponses

    urls = generate_urls_from_pathvars(baseurl, path, pathvars)

    for url in urls:
        with test_case.subTest(method="GET", url=url, headers=headers):
            result = do_get_req(test_case, url, headers)
            test_case.assertLess(result.status_code, 500)
            test_case.assertIn(result.status_code, responses)
    return True


def do_put_fuzzing(*args, **kwargs):
    """
    Perform fuzzing on a PUT endpoint
    """
    baseurl = kwargs.get('baseurl', "")
    headers = kwargs.get('headers', {})
    path = kwargs.get('path', None)
    pathvars = kwargs.get('pathvars', {})
    putvars = kwargs.get('putvars', {})
    responses = kwargs.get('responses', [])
    test_case = kwargs.get('mytestcase', None)

    newresponses = []
    for response in responses:
        try:
            newresponses.append(int(response))
        except ValueError:
            newresponses.append(response)
    responses = newresponses

    url = generate_happy_day_url_from_pathvars(baseurl, path, pathvars)

    payloads = generate_payloads_from_request_vars(putvars)
    for payload in payloads:
        with test_case.subTest(method="PUT", url=url, payload=payload,
                               headers=headers):
            result = do_put_req(test_case, url, headers, payload)
            test_case.assertLess(result.status_code, 500)
            test_case.assertIn(result.status_code, responses)
    return True


def do_delete_fuzzing(*args, **kwargs):
    pass


def do_options_fuzzing(*args, **kwargs):
    pass


def do_head_fuzzing(*args, **kwargs):
    pass


def do_patch_fuzzing(*args, **kwargs):
    pass


def do_trace_fuzzing(*args, **kwargs):
    pass


def do_fuzzing(my_testcase: TestCase, headers: Dict[str, str], spec_r: str):
    self = my_testcase
    baseurl = ""

    parser = ResolvingParser(spec_r)
    spec = parser.specification  # contains fully resolved specs as a dict
    for path, pathvalues in spec.get("paths", {}).items():
        for method, methodvalues in pathvalues.items():
            pathvars = {}
            if method == 'get':
                if 'parameters' in methodvalues.keys():
                    pathvars = methodvalues.get("parameters", {})
                    responses = list(methodvalues.get("responses", {}).keys())
                    do_get_fuzzing(mytestcase=self, baseurl=baseurl,
                                   headers=headers, path=path,
                                   pathvars=pathvars, responses=responses)
            if method == 'post':
                responses = list(methodvalues.get("responses", {}).keys())
                if 'requestBody' in methodvalues.keys() and \
                        'parameters' in methodvalues.keys():
                    pathvars = methodvalues.get("parameters")
                    postvars = methodvalues.get("requestBody", {}).get(
                        "content", {}).get("application/json", {}).get(
                        "schema", {}).get("properties", {})
                    do_post_fuzzing(mytestcase=self, baseurl=baseurl,
                                    headers=headers, path=path,
                                    pathvars=pathvars, postvars=postvars,
                                    responses=responses)
                elif 'requestBody' in methodvalues.keys():
                    postvars = methodvalues.get("requestBody", {}).get(
                        "content", {}).get("application/json", {}).get(
                        "schema", {}).get("properties", {})
                    do_post_fuzzing(mytestcase=self, baseurl=baseurl,
                                    headers=headers, path=path,
                                    postvars=postvars, responses=responses)
            if method == 'put':
                responses = list(methodvalues.get("responses", {}).keys())
                if all(key in methodvalues.keys() for key in ['requestBody', 'parameters']):
                    pathvars = methodvalues.get("parameters")
                    putvars = methodvalues.get("requestBody", {}).get(
                        "content", {}).get("application/json", {}).get(
                        "schema", {}).get("properties", {})
                    do_put_fuzzing(mytestcase=self, baseurl=baseurl,
                                   headers=headers, path=path,
                                   pathvars=pathvars, putvars=putvars,
                                   responses=responses)
                elif 'requestBody' in methodvalues.keys():
                    putvars = methodvalues.get("requestBody", {}).get(
                        "content", {}).get("application/json", {}).get(
                        "schema", {}).get("properties", {})
                    do_put_fuzzing(mytestcase=self, baseurl=baseurl,
                                   headers=headers, path=path,
                                   putvars=putvars, responses=responses)


class FuzzIt:
    def __init__(self, spec_r: str, token: str, test_app: TestCase, header_addition: Dict[str, str] = None):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        if header_addition is not None and isinstance(header_addition, dict):
            for key, value in header_addition.items():
                headers[key] = value
        do_fuzzing(test_app, headers, spec_r)
