"""
Terms of Service and Privacy Policy acceptance.

What is pinned here:

  * an account cannot be created without accepting both documents - checked on
    the server, whatever the browser did;
  * the acceptance is recorded with the *version* and the time, in the same
    transaction as the account;
  * the client can not choose the version it is recorded as accepting;
  * an account that predates the feature, or that accepted an older version, is
    asked again - and is never silently marked as having accepted;
  * the documents themselves are public and carry their version.
"""
import logging
import uuid
from datetime import datetime, timezone

import pytest

from app.core import legal
from app.models.user import User

STRONG_PASSWORD = "correcthorsebatterystaple"
REGISTER = "/api/v1/auth/register"


def _payload(**extra):
    return {
        "email": f"legal-{uuid.uuid4().hex[:12]}@example.com",
        "full_name": "Legal Tester",
        "password": STRONG_PASSWORD,
        **extra,
    }


def _headers(body):
    return {"Authorization": f"Bearer {body['access_token']}"}


# ─── Registration ───────────────────────────────────────────────────────────

@pytest.mark.parametrize("acceptance", [
    {},                                                              # nothing sent
    {"accept_terms": True},                                          # only one of the two
    {"accept_privacy": True},
    {"accept_terms": False, "accept_privacy": False},
    {"accept_terms": True, "accept_privacy": False},
    {"accept_terms": False, "accept_privacy": True},
])
def test_registration_fails_without_accepting_both(client, db, acceptance):
    payload = _payload(**acceptance)
    resp = client.post(REGISTER, json=payload)
    assert resp.status_code == 422
    assert resp.json()["detail"]["error"] == "legal_acceptance_required"
    assert db.query(User).filter(User.email == payload["email"]).first() is None   # no half-created account


def test_registration_succeeds_with_acceptance_and_records_versions_and_time(client, db):
    before = datetime.now(timezone.utc)
    payload = _payload(accept_terms=True, accept_privacy=True)
    resp = client.post(REGISTER, json=payload)
    assert resp.status_code == 201, resp.text

    user = db.query(User).filter(User.email == payload["email"]).one()
    assert user.terms_version == legal.TERMS_VERSION == "2026-09-01"
    assert user.privacy_version == legal.PRIVACY_VERSION == "2026-09-01"
    assert user.terms_accepted_at is not None and user.privacy_accepted_at is not None
    assert before <= user.terms_accepted_at <= datetime.now(timezone.utc)
    assert user.privacy_accepted_at == user.terms_accepted_at
    assert user.requires_legal_acceptance is False


def test_the_client_cannot_choose_the_version_it_is_recorded_as_accepting(client, db):
    payload = _payload(accept_terms=True, accept_privacy=True,
                       terms_version="1999-01-01", privacy_version="1999-01-01",
                       terms_accepted_at="1999-01-01T00:00:00Z", legal_accepted_at="1999-01-01T00:00:00Z")
    resp = client.post(REGISTER, json=payload)
    assert resp.status_code == 201, resp.text
    user = db.query(User).filter(User.email == payload["email"]).one()
    assert user.terms_version == legal.TERMS_VERSION
    assert user.privacy_version == legal.PRIVACY_VERSION
    assert user.terms_accepted_at.year >= 2026                         # the server's clock, not the request's


def test_acceptance_must_be_the_boolean_true(client):
    for value in ("true", 1, "yes", None):
        resp = client.post(REGISTER, json=_payload(accept_terms=value, accept_privacy=True))
        assert resp.status_code == 422, value


def test_the_account_response_says_acceptance_is_current(client):
    body = client.post(REGISTER, json=_payload(accept_terms=True, accept_privacy=True)).json()
    assert body["user"]["requires_legal_acceptance"] is False
    assert body["user"]["terms_version"] == legal.TERMS_VERSION
    me = client.get("/api/v1/auth/me", headers=_headers(body)).json()
    assert me["requires_legal_acceptance"] is False


def test_acceptance_is_logged_per_document_without_personal_data(client, caplog, logs_enabled_security):
    with caplog.at_level(logging.INFO, logger="security"):
        payload = _payload(accept_terms=True, accept_privacy=True)
        client.post(REGISTER, json=payload)
    text = " ".join(r.getMessage() for r in caplog.records)
    assert "event=legal_terms_accepted" in text and "event=privacy_policy_accepted" in text
    assert f"version={legal.TERMS_VERSION}" in text
    assert payload["email"] not in text and payload["password"] not in text


@pytest.fixture()
def logs_enabled_security():
    """`alembic/env.py` disables existing loggers for the whole test session; turn the
    security logger back on for the test that asserts on it."""
    security = logging.getLogger("security")
    was = security.disabled
    security.disabled = False
    yield
    security.disabled = was


# ─── Existing accounts and new versions ─────────────────────────────────────

def _legacy_user(client, db):
    """An account that predates the feature: acceptance columns NULL."""
    body = client.post(REGISTER, json=_payload(accept_terms=True, accept_privacy=True)).json()
    user = db.query(User).filter(User.id == body["user"]["id"]).one()
    user.terms_version = user.privacy_version = None
    user.terms_accepted_at = user.privacy_accepted_at = None
    db.commit()
    return body, user


def test_an_account_that_never_accepted_is_asked_to(client, db):
    body, user = _legacy_user(client, db)
    me = client.get("/api/v1/auth/me", headers=_headers(body)).json()
    assert me["requires_legal_acceptance"] is True
    assert me["terms_version"] is None and me["privacy_version"] is None     # not silently filled in


def test_a_legacy_account_can_accept_and_the_current_versions_are_recorded(client, db):
    body, user = _legacy_user(client, db)
    resp = client.post("/api/v1/auth/accept-legal", headers=_headers(body),
                       json={"accept_terms": True, "accept_privacy": True, "terms_version": "1999-01-01"})
    assert resp.status_code == 200, resp.text
    assert resp.json()["requires_legal_acceptance"] is False
    db.refresh(user)
    assert user.terms_version == legal.TERMS_VERSION and user.privacy_version == legal.PRIVACY_VERSION
    assert user.terms_accepted_at is not None and user.privacy_accepted_at is not None


def test_re_acceptance_also_requires_both_boxes(client, db):
    body, user = _legacy_user(client, db)
    for partial in ({}, {"accept_terms": True}, {"accept_terms": True, "accept_privacy": False}):
        resp = client.post("/api/v1/auth/accept-legal", headers=_headers(body), json=partial)
        assert resp.status_code == 422 and resp.json()["detail"]["error"] == "legal_acceptance_required"
    db.refresh(user)
    assert user.terms_accepted_at is None                                    # nothing recorded


def test_accepting_requires_being_signed_in(client):
    resp = client.post("/api/v1/auth/accept-legal", json={"accept_terms": True, "accept_privacy": True})
    assert resp.status_code == 401


def test_a_new_document_version_asks_existing_users_again(client, db, monkeypatch):
    body = client.post(REGISTER, json=_payload(accept_terms=True, accept_privacy=True)).json()
    headers = _headers(body)
    assert client.get("/api/v1/auth/me", headers=headers).json()["requires_legal_acceptance"] is False

    monkeypatch.setattr(legal, "TERMS_VERSION", "2027-03-01")               # the terms materially changed
    me = client.get("/api/v1/auth/me", headers=headers).json()
    assert me["requires_legal_acceptance"] is True
    assert me["terms_version"] == "2026-09-01"                              # what they accepted is not rewritten

    client.post("/api/v1/auth/accept-legal", headers=headers, json={"accept_terms": True, "accept_privacy": True})
    me = client.get("/api/v1/auth/me", headers=headers).json()
    assert me["requires_legal_acceptance"] is False and me["terms_version"] == "2027-03-01"


def test_a_changed_privacy_version_alone_also_asks_again(client, monkeypatch):
    body = client.post(REGISTER, json=_payload(accept_terms=True, accept_privacy=True)).json()
    monkeypatch.setattr(legal, "PRIVACY_VERSION", "2027-03-01")
    assert client.get("/api/v1/auth/me", headers=_headers(body)).json()["requires_legal_acceptance"] is True


def test_a_timestamp_without_a_version_or_the_reverse_is_not_acceptance():
    now = datetime.now(timezone.utc)
    assert legal.acceptance_is_current(legal.TERMS_VERSION, now, legal.PRIVACY_VERSION, now) is True
    assert legal.acceptance_is_current(legal.TERMS_VERSION, None, legal.PRIVACY_VERSION, now) is False
    assert legal.acceptance_is_current(None, now, legal.PRIVACY_VERSION, now) is False
    assert legal.acceptance_is_current(legal.TERMS_VERSION, now, "old", now) is False


# ─── The documents ──────────────────────────────────────────────────────────

def test_versions_are_published(client):
    assert client.get("/api/v1/legal/versions").json() == {
        "terms_version": legal.TERMS_VERSION, "privacy_version": legal.PRIVACY_VERSION,
    }


@pytest.mark.parametrize("kind", ["terms", "privacy"])
def test_documents_are_public_versioned_and_bilingual(client, kind):
    en = client.get(f"/api/v1/legal/{kind}").json()
    ar = client.get(f"/api/v1/legal/{kind}", params={"lang": "ar"}).json()
    assert en["version"] == ar["version"] == "2026-09-01"
    assert en["language"] == "en" and ar["language"] == "ar"
    assert en["title"] != ar["title"] and en["sections"] and len(en["sections"]) == len(ar["sections"])
    assert all(s["heading"] and s["body"] for s in en["sections"] + ar["sections"])


def test_an_unknown_document_or_language_is_refused(client):
    assert client.get("/api/v1/legal/cookies").status_code == 404
    assert client.get("/api/v1/legal/terms", params={"lang": "fr"}).status_code == 422


def test_the_documents_reflect_the_live_version(client, monkeypatch):
    monkeypatch.setattr(legal, "TERMS_VERSION", "2027-03-01")
    assert client.get("/api/v1/legal/terms").json()["version"] == "2027-03-01"


def test_the_documents_say_declared_skills_are_self_reported(client):
    text = " ".join(
        p for s in client.get("/api/v1/legal/terms").json()["sections"] for p in s["body"]
    ).lower()
    assert "self-reported" in text and "not a verified qualification" in text


# ─── Hardening: a version is never the client's to name ────────────────────

@pytest.mark.parametrize("spoof", [
    {"legal_version": "9999-99-99"},
    {"legal_version": "9999-99-99", "terms_version": "9999-99-99", "privacy_version": "9999-99-99"},
    {"terms_accepted_at": "1999-01-01T00:00:00Z", "privacy_accepted_at": "1999-01-01T00:00:00Z"},
])
def test_no_client_supplied_version_or_time_reaches_the_stored_record(client, db, spoof):
    payload = _payload(accept_terms=True, accept_privacy=True, **spoof)
    assert client.post(REGISTER, json=payload).status_code == 201
    user = db.query(User).filter(User.email == payload["email"]).one()
    assert (user.terms_version, user.privacy_version) == ("2026-09-01", "2026-09-01")
    assert user.terms_accepted_at.year >= 2026 and user.privacy_accepted_at.year >= 2026

    body, legacy = _legacy_user(client, db)
    resp = client.post("/api/v1/auth/accept-legal", headers=_headers(body),
                       json={"accept_terms": True, "accept_privacy": True, **spoof})
    assert resp.status_code == 200
    db.refresh(legacy)
    assert (legacy.terms_version, legacy.privacy_version) == ("2026-09-01", "2026-09-01")
    assert legacy.terms_accepted_at.year >= 2026


def test_the_record_belongs_to_the_account_that_accepted(client, db):
    a = client.post(REGISTER, json=_payload(accept_terms=True, accept_privacy=True)).json()
    b, legacy = _legacy_user(client, db)
    other = db.query(User).filter(User.id == a["user"]["id"]).one()
    other_before = other.terms_accepted_at
    client.post("/api/v1/auth/accept-legal", headers=_headers(b), json={"accept_terms": True, "accept_privacy": True})
    db.expire_all()
    assert legacy.terms_accepted_at is not None                               # the caller's own row was written
    assert other.terms_accepted_at == other_before                            # nobody else's was touched


def test_accepting_twice_keeps_the_original_acceptance_time(client, db):
    body, user = _legacy_user(client, db)
    ok = {"accept_terms": True, "accept_privacy": True}
    client.post("/api/v1/auth/accept-legal", headers=_headers(body), json=ok)
    db.refresh(user)
    first = user.terms_accepted_at
    again = client.post("/api/v1/auth/accept-legal", headers=_headers(body), json=ok)
    assert again.status_code == 200 and again.json()["requires_legal_acceptance"] is False
    db.refresh(user)
    assert user.terms_accepted_at == first and user.privacy_accepted_at == first   # not rewritten


def test_a_profile_update_cannot_write_the_acceptance_record(client, db):
    body, user = _legacy_user(client, db)
    resp = client.patch("/api/v1/auth/me", headers=_headers(body), json={
        "full_name": "Still Legacy", "terms_version": legal.TERMS_VERSION,
        "terms_accepted_at": "2026-09-01T00:00:00Z", "privacy_version": legal.PRIVACY_VERSION,
        "privacy_accepted_at": "2026-09-01T00:00:00Z",
    })
    assert resp.status_code == 200
    db.refresh(user)
    assert user.terms_accepted_at is None and user.privacy_accepted_at is None
    assert client.get("/api/v1/auth/me", headers=_headers(body)).json()["requires_legal_acceptance"] is True


def test_a_rejected_registration_leaves_no_account_even_when_acceptance_was_ticked(client, db):
    payload = _payload(accept_terms=True, accept_privacy=True, password="short")
    assert client.post(REGISTER, json=payload).status_code == 422
    assert db.query(User).filter(User.email == payload["email"]).first() is None


def test_registering_an_existing_email_does_not_touch_that_accounts_record(client, db):
    payload = _payload(accept_terms=True, accept_privacy=True)
    assert client.post(REGISTER, json=payload).status_code == 201
    user = db.query(User).filter(User.email == payload["email"]).one()
    before = user.terms_accepted_at
    dup = client.post(REGISTER, json={**payload, "full_name": "Somebody Else"})
    assert dup.status_code == 400
    db.refresh(user)
    assert user.terms_accepted_at == before and user.full_name == "Legal Tester"
