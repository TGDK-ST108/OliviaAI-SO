import re
import datetime

class Strip:
    @staticmethod
    def strip_datetime_data(data):
        if isinstance(data, (list, tuple)):
            cleaned = []
            for item in data:
                cleaned_item = Strip.strip_datetime_data(item)
                if cleaned_item is not None:
                    cleaned.append(cleaned_item)
            return cleaned if cleaned else None
        elif isinstance(data, dict):
            cleaned = {}
            for key, value in data.items():
                cleaned_value = Strip.strip_datetime_data(value)
                if cleaned_value is not None:
                    cleaned[key] = cleaned_value
            return cleaned if cleaned else None
        elif isinstance(data, (datetime.datetime, datetime.date)):
            # Remove datetime objects
            return None
        elif isinstance(data, str):
            # Check if the string represents a date/time
            if Strip.is_datetime_string(data):
                return None
            else:
                return data
        else:
            # Retain other data types
            return data

    @staticmethod
    def is_datetime_string(s):
        # Implement the function as per your previous code
        date_patterns = [
            r'\b\d{4}-\d{1,2}-\d{1,2}\b',               # YYYY-MM-DD
            r'\b\d{1,2}/\d{1,2}/\d{4}\b',               # MM/DD/YYYY or DD/MM/YYYY
            r'\b\d{1,2}-[A-Za-z]{3}-\d{4}\b',           # DD-MMM-YYYY
            r'\b[A-Za-z]{3,9} \d{1,2}, \d{4}\b',        # Month DD, YYYY
            r'\b\d{1,2} [A-Za-z]{3,9} \d{4}\b',         # DD Month YYYY
            r'\b\d{4}/\d{1,2}/\d{1,2}\b',               # YYYY/MM/DD
            r'\b\d{1,2}:\d{2}(:\d{2})?\b',              # HH:MM or HH:MM:SS
        ]
        datetime_patterns = [
            r'\b\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{2}(:\d{2})?\b',  # YYYY-MM-DD HH:MM[:SS]
            r'\b\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{2}(:\d{2})?\b',  # MM/DD/YYYY HH:MM[:SS]
        ]
        all_patterns = date_patterns + datetime_patterns

        for pattern in all_patterns:
            if re.search(pattern, s):
                return True
        return False
