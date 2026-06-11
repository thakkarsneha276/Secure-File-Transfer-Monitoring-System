class RuleEngine:

    def __init__(self):
        self.sensitive_keywords = [
            "salary",
            "confidential",
            "password",
            "secret",
            "bank",
            "otp"
        ]

        self.external_paths = [
            "E:\\",
            "F:\\",
            "G:\\",
            "USB",
            "Removable",
            "/media"
        ]

    def is_sensitive(self, file_path: str):
        path = file_path.lower()
        return any(word in path for word in self.sensitive_keywords)

    def is_external(self, file_path: str):
        path = file_path.lower()
        return any(ext.lower() in path for ext in self.external_paths)

    def analyze(self, src, dest=None):

        result = {
            "sensitive": self.is_sensitive(src),
            "external": self.is_external(dest or "")
        }

        return result