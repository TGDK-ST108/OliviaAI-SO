class OliviaAI:
    def __init__(self):
        self.modules = {}
        self.api_base_url = "http://localhost:8000"  # Update with deployment URL
        self.logs = []

    def add_module(self, module_name, module_instance):
        self.modules[module_name] = module_instance
        self.log(f"Module '{module_name}' successfully integrated.")

    def call_api(self, endpoint, data):
        """
        Call OliviaAIHiggsAPI endpoints.
        """
        import requests
        try:
            response = requests.post(f"{self.api_base_url}{endpoint}", json=data)
            if response.status_code == 200:
                return response.json()
            else:
                self.log_error(f"API call failed: {response.status_code}, {response.text}")
                return None
        except Exception as e:
            self.log_error(f"Error calling API: {str(e)}")
            return None

    def log(self, message):
        self.logs.append(message)
        print(message)

    def log_error(self, error_message):
        self.logs.append(f"Error: {error_message}")
        print(f"Error: {error_message}")