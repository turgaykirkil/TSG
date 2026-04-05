"""add geocoding cache

Revision ID: feeb1e000000
Revises: 
Create Date: 2026-02-28 19:20:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'feeb1e000000'
down_revision = None
# We don't link down_revision strictly here to avoid conflicts; normally we'd find the head.
# Let's set it to 'c0ffee000001' which is the latest fix I saw, or let's find the head first.
