# Copyright 2025 Emcie Co Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Common utilities for application modules, including pagination cursor handling."""

import base64
import json
from typing import Optional

from parlant.core.persistence.common import Cursor, ObjectId


def encode_cursor(cursor: Cursor) -> str:
    """Encode a Cursor object into a base64 string for API transport.

    Args:
        cursor: The Cursor object to encode.

    Returns:
        A base64-encoded string representation of the cursor.
    """
    cursor_data = {
        "creation_utc": cursor.creation_utc,
        "id": str(cursor.id),
    }
    json_str = json.dumps(cursor_data, separators=(",", ":"))
    return base64.urlsafe_b64encode(json_str.encode("utf-8")).decode("utf-8")


def decode_cursor(cursor_str: str) -> Optional[Cursor]:
    """Decode a base64 cursor string back into a Cursor object.

    Args:
        cursor_str: The base64-encoded cursor string.

    Returns:
        The decoded Cursor object, or None if decoding fails.
    """
    try:
        json_str = base64.urlsafe_b64decode(cursor_str.encode("utf-8")).decode("utf-8")
        cursor_data = json.loads(json_str)
        return Cursor(
            creation_utc=cursor_data["creation_utc"],
            id=ObjectId(cursor_data["id"]),
        )
    except (ValueError, KeyError, json.JSONDecodeError):
        return None
