from slackclient import SlackClient

class CommandHandler():

    currentTargetForDankness = "lemoneylimeslimes"
    memes = [
                    {"trigger" : "`rules`", 
                    "channel" : None, 
                    "responses": 
                        ["This place isn't quite dank enough to get into the rules..."]},
                    {"trigger" : "`rules`", 
                    "channel" : "dank_memers", 
                    "responses": 
                        ["Here are the rules... #1 Don't tell"]}]

    def handle_command(self, slackClient, command, channel):
        """
            Executes bot command if the command is known
        """

        # Finds and executes the given command, filling in response
        response = None
        
        for meme in self.memes:
            if command.startswith(meme["trigger"]):
                if meme["channel"] is None or meme["channel"] == channel:
                    response = meme["responses"][0]

        if response is None:
            return

        # Sends the response back to the channel
        slackClient.api_call(
            "chat.postMessage",
            channel=channel,
            text=response
        )
