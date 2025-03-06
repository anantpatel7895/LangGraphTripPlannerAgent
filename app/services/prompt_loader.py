class PromptLoader:

    def __init__(self, file_path):
        self.file_path = file_path
        self.prompt = self._load_prompt()

    def _load_prompt(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except FileNotFoundError:
            print(f"File not found: {self.file_path}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def format_prompt(self, **kwargs):
        if self.prompt:
            try:
                return self.prompt.format(**kwargs)
            except KeyError as e:
                print(f"Missing variable for prompt formatting: {e}")
                return None
        return None
    
    def get_prompt(self):
        return self.prompt