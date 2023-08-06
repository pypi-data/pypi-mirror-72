import os, json
from cavalry import errors


class Secrets:
    def __init__(self, file, *, create=False):
        if os.path.exists(file):
            self.file = file
        elif not os.path.exists(file) and create:
            self.file = file
            with open(file, "w") as f:
                f.write(json.dumps({}))
        else:
            errors.missing_secrets_file(file)

        with open(self.file, "r") as f:
            self.data = json.loads(f.read())

    def commit(self):
        with open(self.file, "w") as f:
            f.write(json.dumps(self.data))

    def store(self, project, key, value):
        if project in self.data:
            self.data[project][key] = value
        else:
            self.data[project] = {key: value}

    def load(self, project, *keys):
        vars = {}
        if not project in self.data:
            errors.missing_project(project)

        if len(keys) > 0:
            for k in keys:
                if not k in self.data[project]:
                    errors.missing_key(project, k)

                vars[k] = self.data[project][k]
        else:
            for k, v in self.data[project].items():
                vars[k] = v

        return vars

    def delete(self, project, *keys):
        if not project in self.data:
            errors.missing_project(project)

        if len(keys) > 0:
            for k in keys:
                if not k in self.data[project]:
                    errors.missing_key(project, k)

                self.data[project].pop(k)
        else:
            self.data.pop(project)
