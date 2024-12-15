# Initialize Laurel and Overwatch
laurel = LaurelRecovery()
overwatch = OverwatchMonitor()

# Systems to recover
systems = ["Gentuo", "Valhalla"]

# Process Recovery
for system in systems:
    # Step 1: Scan for anomalies
    scan_results = laurel.scan_system(system)
    if scan_results["anomalies_found"]:
        # Step 2: Rollback unauthorized changes
        rollback_status = laurel.rollback_changes(system)

        # Step 3: Verify checksum
        checksum_status = laurel.verify_checksum(system, "known_checksum_value")
        if checksum_status:
            print(f"{system} successfully recovered and verified.")
        else:
            print(f"{system} recovery failed checksum verification.")
    else:
        print(f"No anomalies found in {system}.")

    # Step 4: Start live monitoring
    overwatch.start_monitoring(system)