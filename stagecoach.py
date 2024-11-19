# stagecoach.py

import logging
from datetime import datetime

class Stagecoach:
    def __init__(self, report_format="text", save_path="reports/"):
        self.report_format = report_format
        self.save_path = save_path
        logging.info(f"Stagecoach initialized with report format '{self.report_format}' and save path '{self.save_path}'.")

    def generate_report(self, data):
        """
        Generate a report based on the given data.

        Parameters:
        - data: The data to include in the report.

        Returns:
        - report_content: The content of the report as a formatted string.
        """
        logging.info("Generating report.")
        
        if self.report_format == "text":
            report_content = self._generate_text_report(data)
        elif self.report_format == "json":
            report_content = self._generate_json_report(data)
        else:
            raise ValueError("Unsupported report format.")
        
        self._save_report(report_content)
        return report_content

    def _generate_text_report(self, data):
        """
        Create a human-readable text report from data.

        Parameters:
        - data: The data to include in the report.

        Returns:
        - report_content: The content of the report as a text string.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report_content = f"Report generated on: {timestamp}\n\n"
        
        for key, value in data.items():
            report_content += f"{key}: {value}\n"
        
        logging.debug("Text report generated.")
        return report_content

    def _generate_json_report(self, data):
        """
        Create a JSON-formatted report from data.

        Parameters:
        - data: The data to include in the report.

        Returns:
        - report_content: The content of the report as a JSON string.
        """
        import json
        timestamp = datetime.now().isoformat()
        data_with_timestamp = {"timestamp": timestamp, "data": data}
        
        report_content = json.dumps(data_with_timestamp, indent=4)
        logging.debug("JSON report generated.")
        return report_content

    def _save_report(self, report_content):
        """
        Save the generated report to a file.

        Parameters:
        - report_content: The content of the report to save.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_extension = "txt" if self.report_format == "text" else "json"
        file_name = f"{self.save_path}report_{timestamp}.{file_extension}"

        try:
            with open(file_name, "w") as report_file:
                report_file.write(report_content)
            logging.info(f"Report saved to {file_name}.")
        except Exception as e:
            logging.error(f"Failed to save report: {e}")

    def transmit_report(self, report_content, destination):
        """
        Transmit the report to a specified destination (e.g., email or API).

        Parameters:
        - report_content: The content of the report to transmit.
        - destination: The endpoint or address to send the report to.
        """
        logging.info(f"Transmitting report to {destination}.")
        # Here, implement the logic for transmitting the report
        # For example, send via email, HTTP POST request, etc.
        # Placeholder for future implementation.
        logging.warning("Report transmission not yet implemented.")
