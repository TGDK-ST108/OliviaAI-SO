def generate_integration_report(preparation_logs, integration_logs, synchronization_logs):
    print("Generating integration report...")
    report = {
        "Preparation Logs": preparation_logs,
        "Integration Logs": integration_logs,
        "Synchronization Logs": synchronization_logs,
    }
    return report

# Generate Report
integration_report = generate_integration_report(
    preparator.preparation_logs, integrator.integration_logs, synchronizer.synchronization_logs
)

# Output Report
print("\nIntegration Report:")
for category, logs in integration_report.items():
    print(f"{category}:")
    for log in logs:
        print(log)