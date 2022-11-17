"""Internal diff representation."""


class DiffEntryType:
    pass


class DiffEntriesGenerator:
    def __init__(self, source, compared_to):
        self.source = source
        self.compared_to = compared_to
        self._diff_entries = []

    def _get_formatted_property(self, v, key):
        """Get formatted property."""
        value = v[key]
        formatted_value = self._format_value(value)
        formatted_propery = {"key": key, "value": formatted_value}
        return formatted_propery

    def _format_value(self, v):
        """Recursively format value."""
        if type(v) is dict:
            properties = []
            for key in v:
                property = self._get_formatted_property(v, key)
                properties.append(property)
            return properties
        return v

    @classmethod
    def _get_nested_entry(cls, key, source_value, compared_value):
        diff_generator = cls(source_value, compared_value)
        formatted_value = diff_generator.get_entries()
        return {"key": key, "value": formatted_value}

    def _get_added_entry(self, key, value):
        return {"type": "added", "key": key, "value": self._format_value(value)}

    def _get_unchanged_entry(self, key, value):
        formatted_value = self._format_value(value)
        return {"key": key, "value": formatted_value}

    def _get_updated_entry(self, key, old_value, new_value):
        formatted_old_value = self._format_value(old_value)
        formatted_new_value = self._format_value(new_value)
        return {
            "type": "updated",
            "key": key,
            "old_value": formatted_old_value,
            "new_value": formatted_new_value,
        }

    def _get_removed_entry(self, key, value):
        formatted_value = self._format_value(value)
        return {"type": "removed", "key": key, "value": formatted_value}

    def _process_new_keys(self):
        """Process keys that are contained only in self.compared_to"""
        source_keys = set(self.source.keys())
        compared_keys = set(self.compared_to.keys())
        for key in compared_keys - source_keys:
            value = self.compared_to[key]
            entry = self._get_added_entry(key, value)
            self._diff_entries.append(entry)

    def _process_commmon_key(self, source_key, source_value):
        if source_key in self.compared_to.keys():
            compared_value = self.compared_to[source_key]
            types_are_equal = type(source_value) == type(compared_value) == dict
            values_are_different = source_value != compared_value
            if types_are_equal and values_are_different:
                entry = self._get_nested_entry(
                    source_key, source_value, compared_value
                )
            elif source_value == compared_value:
                entry = self._get_unchanged_entry(source_key, source_value)
            else:
                entry = self._get_updated_entry(
                    source_key, source_value, compared_value
                )
        else:
            entry = self._get_removed_entry(source_key, source_value)
        self._diff_entries.append(entry)

    def get_entries(self):
        """Generate diff entries between source and compared_to dicts."""
        for source_key in self.source:
            source_value = self.source[source_key]
            self._process_commmon_key(source_key, source_value)
        self._process_new_keys()
        return self._diff_entries


def sort_by_key(entries):
    """Recursively sort entries by value."""
    for entry in entries:
        value = entry.get("value")
        if type(value) is list:
            sorted_value = sort_by_key(value)
            entry["value"] = sorted_value
    return sorted(entries, key=lambda x: x["key"])
