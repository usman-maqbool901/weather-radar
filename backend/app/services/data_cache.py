from datetime import datetime
from typing import Optional, Dict, Any

class DataCache:
    def __init__(self):
        self.data: Optional[Dict[str, Any]] = None
        self.last_updated: Optional[datetime] = None
        self.data_timestamp: Optional[datetime] = None
    
    def set(self, data: Dict[str, Any], data_timestamp: Optional[datetime] = None):
        self.data = data
        self.last_updated = datetime.now()
        self.data_timestamp = data_timestamp or datetime.now()
    
    def get(self) -> Optional[Dict[str, Any]]:
        if not self.is_valid():
            return None
        return {
            "data": self.data,
            "lastUpdated": self.last_updated.isoformat(),
            "dataTimestamp": self.data_timestamp.isoformat() if self.data_timestamp else None,
        }
    
    def is_valid(self) -> bool:
        return self.data is not None and self.last_updated is not None
    
    def clear(self):
        self.data = None
        self.last_updated = None
        self.data_timestamp = None

cache = DataCache()

