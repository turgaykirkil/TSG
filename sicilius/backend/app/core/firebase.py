from __future__ import annotations

from pathlib import Path
from typing import Optional

import firebase_admin
from firebase_admin import credentials, firestore

from .config import settings


def _init_firebase_app() -> firebase_admin.App:
    """
    Initialize and return a singleton Firebase App using service account JSON path
    and project ID from settings. Storage bucket is optional and disabled by default.
    """
    try:
        return firebase_admin.get_app()
    except ValueError:
        pass  # not initialized yet

    sa_path = settings.firebase_service_account_path
    project_id = settings.firebase_project_id

    if not sa_path or not project_id:
        raise RuntimeError(
            "Firebase service account path or project id is not configured. "
            "Set tsg_firebase_service_account_path and tsg_firebase_project_id in .env"
        )

    p = Path(sa_path)
    if not p.exists():
        raise FileNotFoundError(f"Firebase service account file not found: {p}")

    cred = credentials.Certificate(str(p))

    options: dict = {"projectId": project_id}

    # Storage is optional; enabled only when explicitly set in config
    if settings.firebase_enable_storage and settings.firebase_storage_bucket:
        options["storageBucket"] = settings.firebase_storage_bucket

    app = firebase_admin.initialize_app(cred, options)
    return app


def get_firestore_client() -> firestore.Client:
    """Get a Firestore client bound to the initialized Firebase App."""
    _init_firebase_app()
    return firestore.client()
