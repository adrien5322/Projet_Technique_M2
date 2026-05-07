"""Schemas for discovery module."""

from pydantic import BaseModel, Field, field_validator
import re


class IPRangeScanRequest(BaseModel):
    """Request schema for IP range scanning."""

    ip_range: str = Field(
        ...,
        min_length=7,
        max_length=20,
        examples=["192.168.1.0/24"],
        description="CIDR notation (e.g. 192.168.1.0/24) or single IP address",
    )

    @field_validator('ip_range')
    @classmethod
    def validate_ip_range(cls, v: str) -> str:
        """
        Validate IP range format.

        Accepts:
        - CIDR notation like 192.168.1.0/24
        - Single IP like 192.168.1.1
        """
        pattern = r'^(\d{1,3}\.){3}\d{1,3}(/\d{1,2})?$'
        if not re.match(pattern, v):
            raise ValueError(
                'Invalid IP range format. Use CIDR notation like 192.168.1.0/24'
            )

        # Additional validation: check each octet is <= 255
        ip_part = v.split('/')[0]
        octets = ip_part.split('.')
        for octet in octets:
            if int(octet) > 255:
                raise ValueError(f'Invalid IP address: octet {octet} exceeds 255')

        # Validate CIDR prefix if present
        if '/' in v:
            prefix = int(v.split('/')[1])
            if prefix > 32:
                raise ValueError(f'Invalid CIDR prefix: /{prefix} exceeds /32')

        return v
