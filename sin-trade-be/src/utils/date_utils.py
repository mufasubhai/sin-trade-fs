def parse_datetime(self, date_string):
    if date_string:
        try:
            return datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            return None
    return None