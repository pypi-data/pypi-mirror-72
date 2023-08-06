from dataclasses import dataclass
from django.contrib.auth.models import User
from faker import Faker
from pprint import pformat
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from safetydance import step, step_data

# from safetydance_django.steps import *
from safetydance_django.test import *
from safetydance_test import scripted_test, Given, When, Then, And, TestStepPrefix
from scoped_rbac.models import Role
import logging
import pytest


role_url = step_data(str)


@step
def create_editor_role(context_url):
    # Create a role
    When.http.post(
        reverse("role-list"),
        {
            "definition": {
                "http.POST": [Role.resource_type.iri],
                "http.GET": [Role.resource_type.iri, Role.resource_type.list_iri],
                "http.PUT": [Role.resource_type.iri],
                "http.DELETE": [Role.resource_type.iri],
            },
            # TODO add these fields
            # "name": role_name,
            # "description": role_description,
            "rbac_context": context_url,
        },
        format="json",
    )
    logging.info(http_response)
    logging.info(http_response.data)
    Then.http.status_code_is(201)
    role_url = http_response["location"]


@step
def get_role_list():
    When.http.get(reverse("role-list"))
    Then.http.status_code_is(200)


@step
def role_list_contains(*role_urls):
    list_json = http_response.json()
    urls = [x["url"] for x in list_json["results"]]
    for role_url in role_urls:
        assert role_url in urls, f"No matching role for {role_url} in {urls}"


@step
def role_list_does_not_contain(*role_urls):
    list_json = http_response.json()
    urls = [x["url"] for x in list_json["results"]]
    for role_url in role_urls:
        assert role_url not in urls, f"Found a matching role for {role_url} in {urls}"


@step
def assign_role(role_url, user, context_url):
    When.http.post(
        reverse("roleassignment-list"),
        {
            "user": reverse("user-detail", [user.instance.pk]),
            "role": role_url,
            "rbac_context": context_url,
        },
        format="json",
    )
    Then.http.status_code_is(201)


@step
def get_user_rbac_policy():
    When.http.get(reverse("user-rbac-policy"), format="json")
