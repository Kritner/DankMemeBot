from slackclient import SlackClient

class CommandHandler():

    currentTargetForDankness = "lemoneylimeslimes"
    memes = [
                    {"trigger" : "rules", 
                    "channel" : None, 
                    "responses": 
                        ["This place isn't quite dank enough to get into the rules..."]},
                    {"trigger" : "rules", 
                    "channel" : "dank_memers", 
                    "responses": 
                        [("Here are the rules..." + 
                        "\nRule #1: Don’t tell {0}" + 
                        "\nRule #2: If {0} still finds out, invite him." +
                        "\nRule #3: If {0} is in this channel, he can select the next potential candidate.").format(currentTargetForDankness)]}]

    def handle_command(self, slackClient, command, channel):
        """
            Executes bot command if the command is known
        """

        # Finds and executes the given command, filling in response
        response = None
        
        channel_name = self.get_current_channel_name(slackClient, channel)

        for meme in self.memes:
            if command.startswith(meme["trigger"]):
                if meme["channel"] == channel_name:
                    response = meme["responses"][0]
                elif meme["channel"] is None:
                    response = meme["responses"][0]

        if response is None:
            return

        # Sends the response back to the channel
        slackClient.api_call(
            "chat.postMessage",
            channel=channel,
            text=response
        )

    def get_current_channel_name(self, slackClient, channel):
        channel_name = None
        for chan in self.get_channel_list(slackClient, True):
            if channel == chan["id"]:
                channel_name = chan["name"]

        return channel_name

    def get_channel_list(self, slackClient, includePrivate = True):
        channelList = []

        apiChannels = slackClient.api_call("channels.list")
        channels = apiChannels["channels"]
        for chan in channels:
            channelList.append({"id": chan["id"], "name": chan["name"]})

        if includePrivate:
            apiChannels = slackClient.api_call("groups.list")
            channels = apiChannels["groups"]
            for chan in channels:
                channelList.append({"id": chan["id"], "name": chan["name"]})

        return channelList

