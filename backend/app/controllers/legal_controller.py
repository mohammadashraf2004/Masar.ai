"""
app/controllers/legal_controller.py

The Terms of Service and Privacy Policy, served from the same package that
holds their version numbers, so what the site shows and what an account is
recorded as accepting cannot drift apart.

    GET /legal/versions            the versions in force
    GET /legal/{terms|privacy}     one document, ?lang=en|ar

Public: a person has to be able to read the terms before creating an account.
"""
from typing import Dict, List, Literal

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.content import legal_documents as docs

router = APIRouter(prefix="/legal", tags=["Legal"])


class LegalVersions(BaseModel):
    terms_version: str
    privacy_version: str


class LegalSection(BaseModel):
    heading: str
    body: List[str]


class LegalDocument(BaseModel):
    kind: Literal["terms", "privacy", "refund"]
    version: str
    language: Literal["en", "ar"]
    title: str
    intro: str
    sections: List[LegalSection]


@router.get("/versions", response_model=LegalVersions)
def get_versions() -> Dict[str, str]:
    v = docs.versions()
    return {"terms_version": v["terms"], "privacy_version": v["privacy"]}


@router.get("/{kind}", response_model=LegalDocument)
def get_document(kind: str, lang: Literal["en", "ar"] = Query("en")):
    document = docs.get_document(kind, lang)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"kind": kind, "version": docs.versions()[kind], "language": lang, **document}
