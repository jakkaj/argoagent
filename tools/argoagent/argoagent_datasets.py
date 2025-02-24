import json

class AgentRunsDatasetEntry:
    def __init__(self, param, steps, input_data=None):
        self.param = param
        self.steps = steps
        self.input_data = input_data

    @classmethod
    def from_dict(cls, data):
        return cls(
            param=data.get("param"),
            steps=data.get("steps", []),
            input_data=data.get("input_data")
        )

    def __repr__(self):
        return (f"AgentRunsDatasetEntry(param={self.param!r}, "
                f"steps={self.steps!r}, input_data={self.input_data!r})")

class AgentRunsDataset:
    def __init__(self, entries):
        self.entries = entries

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        if isinstance(data, list):
            entries = [AgentRunsDatasetEntry.from_dict(item) for item in data]
        elif isinstance(data, dict):
            # If a single dictionary is provided, wrap it in a list.
            entries = [AgentRunsDatasetEntry.from_dict(data)]
        else:
            raise ValueError("Unsupported JSON format")
        return cls(entries)

    def __iter__(self):
        return iter(self.entries)

    def __repr__(self):
        return f"AgentRunsDataset(entries={self.entries!r})"


# Example usage:
json_data = '''
[
    {
        "input_data": "Find me information on Perth",
        "param": "Perth",
        "steps": [
            "wikistep"
        ]
    },
    {
        "input_data": "Find me information on Perth, summarise it.",
        "param": "Perth",
        "steps": [
            "wikistep",
            "summarystep"
        ]
    }
]
'''
