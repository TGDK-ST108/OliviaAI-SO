# Systems to recover
systems = ["Gentuo", "Valhalla"]

# Initialize Laurel
laurel = LaurelRecovery()

# Rollback for Each System
for system in systems:
    print(f"Starting rollback for {system}...")
    rollback_results = laurel.rollback_changes(system)
    if rollback_results["status"] == "success":
        print(f"Rollback successful for {system}.")
    else:
        print(f"Rollback failed for {system}. Reason: {rollback_results.get('reason')}")