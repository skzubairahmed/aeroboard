import datetime
class Logger():
    def __init__(self, file_path):
        self.file_path = file_path

    def logData(self, code, message):
        try:
            timestamp = datetime.datetime.now()
            timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            log = f"[{code}] [{timestamp_str}] --- {message}\n"
            with open(self.file_path, 'a', encoding="utf-8") as file:
                file.write(log)
            return None
        except Exception as e:
            return 

    def clearLogs(self):
        print("Clearing...")
            