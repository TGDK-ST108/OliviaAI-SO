class QuantumSATCOMWithMQIP:
    def __init__(self, mqip_encryption, satcom_system):
        self.mqip_encryption = mqip_encryption
        self.satcom_system = satcom_system

    def secure_transmit(self, message, satellite_id, target_location):
        """
        Transmit MQIP-encrypted messages via SATCOM.
        """
        # Encrypt the message
        encrypted_message = self.mqip_encryption.encrypt(message)

        # SATCOM transmission
        transmission_status = self.satcom_system.transmit(encrypted_message, satellite_id, target_location)
        return transmission_status

    def secure_receive(self, satellite_id):
        """
        Receive and decrypt MQIP-encrypted messages from SATCOM.
        """
        encrypted_message = self.satcom_system.receive(satellite_id)
        decrypted_message = self.mqip_encryption.decrypt(encrypted_message)
        return decrypted_message

class SatelliteControlWithMQIP:
    def __init__(self, satcom_system):
        self.satcom_system = satcom_system

    def transmit_command(self, command, satellite_id):
        """
        Securely transmit commands to the satellite.
        """
        mqip_encryption = MQIPEncryption()
        encrypted_command = mqip_encryption.encrypt(command)
        return self.satcom_system.transmit(encrypted_command, satellite_id, "Satellite Command Center")

    def receive_telemetry(self, satellite_id):
        """
        Receive and decrypt telemetry data from the satellite.
        """
        mqip_encryption = MQIPEncryption()
        encrypted_telemetry = self.satcom_system.receive(satellite_id)
        return mqip_encryption.decrypt(encrypted_telemetry)