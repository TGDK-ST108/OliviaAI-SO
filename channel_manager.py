class ChannelManager:
    def __init__(self):
        self.channels = {}

    def add_channel(self, channel_name):
        self.channels[channel_name] = CurrogationChannel(channel_name)

    def route_to_channel(self, channel_name, data):
        """Routes data to a specific channel."""
        channel = self.channels.get(channel_name)
        if channel:
            channel.add_data(data)
