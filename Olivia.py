import random
import matplotlib.pyplot as plt
import numpy as np

class Sequencer:
    def __init__(self):
        self.context = {}
        self.command_log = []

    def submit_statement(self, user_input):
        response = self.process_input(user_input)
        self.command_log.append((user_input, response))
        return response

    def process_input(self, input_text):
        command, context_info = self.extract_command(input_text)
        response = self.execute_command(command, context_info)
        return response

    def extract_command(self, input_text):
        if "::" in input_text:
            command, context_info = input_text.split("::")
            return command.strip(), context_info.strip()
        else:
            return input_text.strip(), None

    def execute_command(self, command, context_info):
        if command.lower() == "set context":
            return self.set_context(context_info)
        elif command.lower() == "get context":
            return self.get_context(context_info)
        elif command.lower() == "reset context":
            return self.reset_context()
        elif command.lower() == "submit":
            return self.handle_submit(context_info)
        elif command.lower() == "receive":
            return self.handle_receive(context_info)
        else:
            return "Command not recognized."

    def set_context(self, context_info):
        if context_info:
            key, value = context_info.split("=")
            self.context[key.strip()] = value.strip()
            return f"Context set: {key.strip()} = {value.strip()}"
        return "Invalid context format. Use key=value."

    def get_context(self, key):
        if key and key in self.context:
            return f"Context: {key} = {self.context[key]}"
        return "Context key not found."

    def reset_context(self):
        self.context.clear()
        return "Context reset."

    def handle_submit(self, submission):
        return f"Submission received: {submission}"

    def handle_receive(self, request):
        return f"Request processed for: {request}"

    def log_history(self):
        return self.command_log

# -------------------- ZenGarden and VHFVGRF --------------------

class ZenGarden:
    def __init__(self, frequency):
        self.frequency = frequency

    def adjust_variable_grade(self, data):
        adjusted_data = [d * (1 + self.frequency) for d in data]
        return adjusted_data

    def create_waveform_display(self, data):
        t = np.linspace(0, 1, len(data))
        signal = np.sin(2 * np.pi * self.frequency * t) * np.array(data)
        plt.plot(t, signal)
        plt.title("Holographic Waveform Display")
        plt.xlabel("Time")
        plt.ylabel("Amplitude")
        plt.show()
        return signal


class VHFVGRF:
    def __init__(self, n_trees, zen_garden):
        self.n_trees = n_trees
        self.zen_garden = zen_garden
        self.forest = []

    def create_tree(self, data):
        tree = {"decision": random.choice(data)}
        return tree

    def train(self, data):
        adjusted_data = self.zen_garden.adjust_variable_grade(data)
        self.forest = [self.create_tree(adjusted_data) for _ in range(self.n_trees)]

    def predict(self, data):
        predictions = [tree["decision"] for tree in self.forest]
        return max(set(predictions), key=predictions.count)

# -------------------- Lancaster and Olivia --------------------

class Lancaster:
    def __init__(self, sequencer):
        self.sequencer = sequencer
        self.olivia = Olivia(self.sequencer)

    def communicate_with_olivia(self, task, data):
        print(f"Lancaster forwarding task '{task}' to Olivia.")
        response = self.olivia.process_call(task, data)
        return response

    def receive_processing_status(self):
        status = self.olivia.report_processing_status()
        print(f"Lancaster received Olivia's status: {status}")
        return status


class Olivia:
    def __init__(self, sequencer):
        self.sequencer = sequencer
        self.calls_log = []
        self.processing_status = "Idle"
        self.pressure_points = []

    def process_call(self, task, data):
        print(f"Processing task '{task}' with data: {data}")
        self.calls_log.append((task, data))
        self.update_processing_status(f"Processing task '{task}'")
        self.track_pressure_points(data)
        self.sequencer.submit_statement(f"Submit:: Task '{task}' processed")
        return f"Task '{task}' processed successfully"

    def track_pressure_points(self, data):
        self.pressure_points = [random.uniform(0, 1) for _ in data]
        self.processing_status = "Analyzing Pressure Points"
        print(f"Pressure points: {self.pressure_points}")

    def update_processing_status(self, status):
        self.processing_status = status

    def report_processing_status(self):
        return self.processing_status

    def chat_with_user(self, user_message):
        response = self.sequencer.submit_statement(f"Submit:: User Message: {user_message}")
        print(f"Olivia response: {response}")
        return response


# -------------------- Firmworks Class --------------------

class Firmworks:
    def __init__(self, n_trees, frequency):
        self.sequencer = Sequencer()
        self.lancaster = Lancaster(self.sequencer)
        self.zen_garden = ZenGarden(frequency)
        self.vhfvgrf = VHFVGRF(n_trees, self.zen_garden)

    # In Firmworks class
    def distribute_task(self, task, data):
        print(f"Distributing task: {task}")
    # Train the VHFVGRF with data
        self.vhfvgrf.train(data)
        prediction = self.vhfvgrf.predict(data)
    # Generate the holographic waveform display
        self.zen_garden.create_waveform_display(data)
    # Wrap prediction in a list to ensure it's iterable
        response = self.lancaster.communicate_with_olivia(task, [prediction])
        return response


    def monitor_progress(self, task_id):
        print(f"Monitoring progress for task: {task_id}")
        processing_status = self.lancaster.receive_processing_status()
        self.zen_garden.create_waveform_display([task_id])
        return processing_status

    def chat_with_olivia(self, user_message):
        response = self.lancaster.olivia.chat_with_user(user_message)
        return response


# -------------------- Example Usage --------------------

if __name__ == "__main__":
    firmworks = Firmworks(n_trees=5, frequency=0.1)

    # Example Task Distribution
    task = "Analyze User Behavior"
    data = [1, 2, 3, 4, 5]
    
    response = firmworks.distribute_task(task, data)
    print(f"Response: {response}")

    # Monitor Progress with holographic waveform display
    firmworks.monitor_progress(task_id=1)

    # Chat with Olivia
    firmworks.chat_with_olivia("Hello Olivia, how's the task going?")
