from dataclasses import dataclass
from django.contrib.auth.models import User
from faker import Faker
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from safetydance import step_data
from safetydance_django.test import *
from safetydance_test import scripted_test, Given, When, Then, And
from scoped_rbac.models import Role
from scoped_rbac.rbac_contexts import SOME_CONTEXT
from .step_extensions import *
import logging
import pytest


@dataclass
class TestUser:
    username: str
    email: str
    password: str
    instance: object


def create_user(is_super=False):
    fake = Faker()
    name = fake.pystr(min_chars=10, max_chars=20)
    email = f"{name}@example.com"
    passwd = fake.pystr(min_chars=12, max_chars=20)
    if is_super:
        user = User.objects.create_superuser(name, email, passwd)
    else:
        user = User.objects.create(
            username=name, email=email, password=passwd, is_active=True
        )
    user.save()
    return TestUser(name, email, passwd, user)


@pytest.fixture()
def superuser(transactional_db):
    # fake = Faker()
    # name = fake.pystr(min_chars=10, max_chars=20)
    # email = f"{name}@example.com"
    # passwd = fake.pystr(min_chars=12, max_chars=20)
    # superuser = User.objects.create_superuser(name, email, passwd,)
    # superuser.save()
    # return TestUser(name, email, passwd, superuser)
    return create_user(is_super=True)


@pytest.fixture()
def editor_user(transactional_db):
    return create_user()


@pytest.fixture()
def not_authorized_user(transactional_db):
    return create_user()


@pytest.mark.django_db
@scripted_test
def test_create_access_controlled_resource(superuser):
    Given.http.force_authenticate(user=superuser.instance)
    When.http.get(reverse("exampleaccesscontrolledmodel-list"))
    Then.http.status_code_is(200)
    And.http.response_json_is(
        {"count": 0, "next": None, "previous": None, "results": []}
    )

    When.http.post(
        reverse("exampleaccesscontrolledmodel-list"),
        {"name": "foo", "rbac_context": ""},
        format="json",
    )
    Then.http.status_code_is(201)
    When.http.get_created()
    Then.http.status_code_is(200)
    And.http.response_json_is({"name": "foo"})

    # FIXME delete after testing, add envelope testing
    # When.http.get(reverse("exampleaccesscontrolledmodel-list"))
    # print(http_response.json())
    # print(http_response._headers)
    # raise Exception("just want the trace")


fake = step_data(Faker, initializer=Faker)


@pytest.mark.django_db
@scripted_test
def test_simple_role_assignment(superuser, editor_user, not_authorized_user):
    context_name = fake.pystr(min_chars=10, max_chars=20)

    Given.http.force_authenticate(user=superuser.instance)
    When.http.post(
        reverse("exampleaccesscontrolledmodel-list"),
        {"name": context_name},
        format="json",
    )
    Then.http.status_code_is(201)
    context_url = http_response["location"]

    # Create a role
    Given.create_editor_role(context_url)

    # Assign the role to editor_user
    And.assign_role(role_url, editor_user, context_url)

    # Switch to the editor_user
    And.http.force_authenticate(user=editor_user.instance)

    # Create a protected resource as editor_user
    protected_resource_content = {"definition": {}, "rbac_context": context_url}
    When.http.post(reverse("role-list"), protected_resource_content, format="json")
    Then.http.status_code_is(201)
    protected_resource_url = http_response["location"]

    # Get the resource
    When.http.get(protected_resource_url)
    Then.http.status_code_is(200)
    And.http.response_json_is(protected_resource_content)

    # Update the resource
    updated_content = {"definition": {"GET": True}, "rbac_context": context_url}
    When.http.put(protected_resource_url, updated_content, format="json")
    Then.http.status_code_is(200)
    When.http.get(protected_resource_url)
    Then.http.status_code_is(200)
    And.http.response_json_is(updated_content)

    # Get the resource list as the editor_user
    When.http.get(reverse("role-list"))
    Then.http.status_code_is(200)

    # Try creating a resource in an unauthorized context
    When.http.post(
        reverse("role-list"),
        {"definition": {}, "rbac_context": fake.pystr(min_chars=10, max_chars=20)},
        format="json",
    )
    Then.http.status_code_is(403)

    # Switch to the not_authorized_user
    Given.http.force_authenticate(user=not_authorized_user.instance)

    # Get the resource list as the not_authorized_user
    # check that it failed
    When.http.get(reverse("role-list"))
    Then.http.status_code_is(403)

    # Get the resource as the not_authorized_user
    # check that it failed
    When.http.get(protected_resource_url)
    Then.http.status_code_is(403)

    # Update the resource
    # check that it failed
    When.http.put(protected_resource_url, {})
    Then.http.status_code_is(403)

    # Delete the resource
    # check that it failed
    When.http.delete(protected_resource_url)
    Then.http.status_code_is(403)

    # Create a resource
    # check that it failed
    When.http.post(reverse("role-list"), {}, format="json")
    Then.http.status_code_is(403)

    # Switch to the editor_user
    # delete the resource
    Given.http.force_authenticate(user=editor_user.instance)
    And.http.get(protected_resource_content)
    And.http.delete(protected_resource_url)
    Then.http.status_code_is_one_of(200, 204)

    # double check it's gone
    When.http.get(protected_resource_url)
    Then.http.status_code_is(404)


@pytest.mark.django_db
@scripted_test
def test_list_filtering(superuser, editor_user):
    context1_name = fake.pystr(min_chars=10, max_chars=20)
    context2_name = fake.pystr(min_chars=10, max_chars=20)

    Given.http.force_authenticate(user=superuser.instance)
    And.create_editor_role(context1_name)
    role_in_context1_url = role_url
    And.create_editor_role(context2_name)
    role_in_context2_url = role_url

    # validate superuser sees both roles in listing
    When.get_role_list()
    Then.role_list_contains(role_in_context1_url, role_in_context2_url)

    # validate editor_user sees only role in context1 in listing
    When.assign_role(role_in_context1_url, editor_user, context1_name)
    And.http.force_authenticate(user=editor_user.instance)
    And.get_role_list()
    Then.role_list_contains(role_in_context1_url)
    And.role_list_does_not_contain(role_in_context2_url)


@pytest.mark.django_db
@scripted_test
def test_get_user_rbac_policy(superuser, editor_user):
    Given.http.force_authenticate(user=superuser.instance)
    When.get_user_rbac_policy()
    Then.http.status_code_is(200)
    And.http.response_json_is(True)

    # TODO more comprehensive testing
    context1_name = fake.pystr(min_chars=10, max_chars=20)
    context2_name = fake.pystr(min_chars=10, max_chars=20)

    Given.http.force_authenticate(user=superuser.instance)
    And.create_editor_role(context1_name)
    role_in_context1_url = role_url
    And.create_editor_role(context2_name)
    role_in_context2_url = role_url

    # validate editor_user sees only role in context1 in listing
    Given.assign_role(role_in_context1_url, editor_user, context1_name)
    And.assign_role(role_in_context2_url, editor_user, context2_name)
    And.http.get(role_in_context1_url)
    role_in_context1_json = http_response.json()
    And.http.get(role_in_context2_url)
    role_in_context2_json = http_response.json()
    When.http.force_authenticate(user=editor_user.instance)
    And.get_user_rbac_policy()
    Then.http.response_json_is(
        {
            context1_name: role_in_context1_json["definition"],
            context2_name: role_in_context2_json["definition"],
            SOME_CONTEXT: role_in_context1_json["definition"],
        }
    )
