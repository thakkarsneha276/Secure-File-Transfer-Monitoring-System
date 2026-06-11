import hashlib


class HashUtil:

    def generate_hash(self, file_path):
        try:
            sha = hashlib.sha256()

            with open(file_path, "rb") as f:
                while chunk := f.read(4096):
                    sha.update(chunk)

            return sha.hexdigest()

        except Exception as e:
            return f"error:{e}"