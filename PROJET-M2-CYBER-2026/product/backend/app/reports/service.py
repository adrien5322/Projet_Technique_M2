"""Reports service for data export (CSV, JSON).

Handles data retrieval from all SOC modules and generates
export files in memory.
"""

import csv
import io
import json
from datetime import datetime, timezone
from typing import Any, Optional

from sqlalchemy import inspect
from sqlalchemy.orm import Session


def _model_exists(db: Session, tablename: str) -> bool:
    """Check if a table exists in the database."""
    try:
        return inspect(db.bind).has_table(tablename)
    except Exception:
        return False


def _serialize_row(row: Any) -> dict:
    """Convert a SQLAlchemy model instance to a plain dict."""
    result = {}
    for column in row.__table__.columns:
        value = getattr(row, column.name, None)
        # Convert datetime to ISO string for serialization
        if isinstance(value, datetime):
            value = value.isoformat()
        # Convert non-serializable types to string
        if value is not None and not isinstance(value, (str, int, float, bool, list, dict)):
            value = str(value)
        result[column.name] = value
    return result


def _parse_date(date_str: Optional[str]) -> Optional[datetime]:
    """Parse a date string into a datetime object.

    Supports ISO 8601 format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS).
    Returns None if parsing fails or input is None.
    """
    if date_str is None:
        return None

    # Try different common formats
    formats = [
        "%Y-%m-%d",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%d %H:%M:%S",
    ]

    for fmt in formats:
        try:
            naive_dt = datetime.strptime(date_str, fmt)
            # Return naive datetime for SQLite compatibility
            return naive_dt
        except ValueError:
            continue

    return None


def _get_date_field(model_class: Any, export_type: str) -> Any:
    """Get the appropriate date field for filtering based on export type."""
    date_field_mapping = {
        "alerts": "created_at",
        "events": "timestamp",
        "audit": "timestamp",
        "assets": "created_at",
    }

    field_name = date_field_mapping.get(export_type)
    if field_name and hasattr(model_class, field_name):
        return getattr(model_class, field_name)

    return None


def get_export_data(
    db: Session,
    export_type: str,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
) -> list[dict]:
    """Retrieve data to export based on type with optional date filtering.

    Args:
        db: Database session.
        export_type: One of "alerts", "events", "audit", "assets".
        from_date: Optional start date (ISO 8601 format: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS).
        to_date: Optional end date (ISO 8601 format: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS).

    Returns:
        List of dictionaries representing rows to export.
        Returns empty list if the table does not exist yet.
    """
    type_to_model = {
        "assets": ("assets", "Asset"),
        "alerts": ("alerts", "Alert"),
        "events": ("events", "Event"),
        "audit": ("audit_logs", "AuditLog"),
    }

    mapping = type_to_model.get(export_type)
    if mapping is None:
        return []

    tablename, model_name = mapping

    if not _model_exists(db, tablename):
        return []

    try:
        # Dynamically import the model class
        from app.models import Base  # noqa: F401

        # Try to get the model from the registry
        model_class = Base.registry._class_registry.get(model_name)
        if model_class is None:
            return []

        # Build query with optional date filtering
        query = db.query(model_class)

        # Parse date filters
        from_dt = _parse_date(from_date)
        to_dt = _parse_date(to_date)

        # Apply date filtering if dates are provided
        date_field = _get_date_field(model_class, export_type)
        if date_field is not None:
            if from_dt is not None:
                query = query.filter(date_field >= from_dt)
            if to_dt is not None:
                # Add 1 day to to_date to include the entire day
                import datetime as dt
                to_dt_inclusive = to_dt + dt.timedelta(days=1)
                query = query.filter(date_field < to_dt_inclusive)

        rows = query.all()
        return [_serialize_row(row) for row in rows]
    except Exception:
        # Graceful fallback: table or model not ready yet
        return []


def generate_csv(data: list[dict], filename: str) -> tuple[str, str]:
    """Generate a CSV file in memory from a list of dicts.

    Args:
        data: List of dictionaries to export.
        filename: Base filename (without timestamp).

    Returns:
        Tuple of (csv_content_string, full_filename_with_timestamp).
    """
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    full_filename = f"{filename}_{timestamp}.csv"

    if not data:
        # Return empty CSV with just headers hint
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["info", "No data available for export"])
        return output.getvalue(), full_filename

    # Collect all unique keys preserving order of first appearance
    fieldnames = []
    seen = set()
    for row in data:
        for key in row:
            if key not in seen:
                fieldnames.append(key)
                seen.add(key)

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(data)

    return output.getvalue(), full_filename


def generate_json(data: list[dict], filename: str) -> tuple[str, str]:
    """Generate a structured JSON export with metadata.

    Args:
        data: List of dictionaries to export.
        filename: Base filename (without timestamp).

    Returns:
        Tuple of (json_content_string, full_filename_with_timestamp).
    """
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    full_filename = f"{filename}_{timestamp}.json"

    export_payload = {
        "export_metadata": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "source": "DAR-Cyber",
            "record_count": len(data),
            "filename": full_filename,
        },
        "data": data,
    }

    content = json.dumps(export_payload, indent=2, ensure_ascii=False, default=str)
    return content, full_filename
