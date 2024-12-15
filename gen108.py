# Generate Recovery Report
def generate_recovery_report(laurel, overwatch):
    print("Generating recovery report...")
    report = {
        "laurel_logs": laurel.recovery_logs,
        "overwatch_logs": overwatch.activity_logs,
    }
    return report

recovery_report = generate_recovery_report(laurel, overwatch)
print("Recovery Report:", recovery_report)