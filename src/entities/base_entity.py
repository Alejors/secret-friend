from datetime import datetime
from dataclasses import asdict

from src.utils import format_date


class BaseEntity:
  def to_dict(self):
    return asdict(self)

  def serialize(self, include_deleted = False):
    _dict = self.to_dict()
    if not include_deleted:
      _dict.pop("deleted_at")
    _dict = self._check_datetimes(_dict)
    return _dict
  
  def _check_datetimes(self, _dict: dict) -> dict:
    for key in _dict.keys():
      if isinstance(_dict[key], dict):
        _dict[key] = self._check_datetimes(_dict[key])
      if isinstance(_dict[key], datetime):
        _dict[key] = format_date(_dict[key])
    
    return _dict