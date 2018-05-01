import random
from slackclient import SlackClient

class CommandHandler():

    _memeMode = "sequential"
    _memeModeToggleString = "memeMode"
    _currentTargetForDankness = "michael"
    _helpCommandString = "wat do"
    _memes = [
        {"trigger" : "rules",
        "channel" : None, 
        "index" : 0,
        "responses": 
            ["This place isn't quite dank enough to get into the rules..."]},
        {"trigger" : "rules", 
        "channel" : "dank_memers", 
        "index" : 0,
        "responses": 
            [("Here are the rules..." + 
            "\nRule #1: Don’t tell {0}" + 
            "\nRule #2: If {0} still finds out, invite him." +
            "\nRule #3: If {0} is in this channel, he can select the next potential candidate.").format(_currentTargetForDankness)]},
        {"trigger" : "flavortown", 
        "channel" : None, 
        "index" : 0,
        "responses": [
            "http://i0.kym-cdn.com/photos/images/newsfeed/001/355/960/bf2.jpg",
            "http://i0.kym-cdn.com/photos/images/newsfeed/001/053/453/f5f.jpg",
            "http://i0.kym-cdn.com/photos/images/newsfeed/000/972/194/cd9.jpg",
            "https://i.chzbgr.com/full/9101308416/h26CA5A46/"
        ]},
        {"trigger" : "it is wednesday my dudes", 
        "channel" : None, 
        "index" : 0,
        "responses": [
            "https://www.youtube.com/watch?v=du-TY1GUFGk",
            "https://www.youtube.com/watch?v=YSDAAh6Lps4",
            "https://www.youtube.com/watch?v=m2Z0CyuyfMI",
            "https://youtu.be/Oct2xKMGOno?list=RDRT0soCWpH3Q",
            "https://www.youtube.com/watch?v=OzQ-KvxLVT0",
            "https://youtu.be/VaPMUACYWww",
            "https://www.youtube.com/watch?v=csqJK8wwaHw",
            "https://www.youtube.com/watch?v=JHO61_wDC30",
            "https://youtu.be/RT0soCWpH3Q",
            "https://youtu.be/0W51GIxnwKc",
            "https://youtu.be/VfaNCw2bF48",
            "https://youtu.be/RT0soCWpH3Q"
        ]},
        {"trigger" : "doge", 
        "channel" : None, 
        "index" : 0,
        "responses": [
            "https://mtgcardsmith.com/view/complete/full/2017/8/21/1503338850980696.png",
            "http://i0.kym-cdn.com/photos/images/newsfeed/000/581/723/a8b.jpg",
            "http://i0.kym-cdn.com/photos/images/newsfeed/000/581/168/9f1.jpg",
            "http://i0.kym-cdn.com/photos/images/newsfeed/000/581/567/bab.jpg",
            "http://i0.kym-cdn.com/photos/images/newsfeed/000/661/142/c03.jpg"
        ]}]

    def handle_command(self, slackClient, command, channel):
        """
            Executes bot command if the command is known
        """

        # Finds and executes the given command, filling in response
        response = None
        
        if command.startswith(self._helpCommandString):
            response = self._get_help()
        elif command.startswith(self._memeModeToggleString):
            response = "changing current 'memeMode' of {0} ".format(self._memeMode)
            
            if self._memeMode == "sequential":
                self._memeMode = "random"
            else:
                self._memeMode = "sequential"

            response = response + "to {0}.".format(self._memeMode)
        else:
            response = self._get_memes(slackClient, command, channel)

        if response is None:
            response = "Hmm... I'm not sure what you mean.  Try '{0}' for commands".format(self._helpCommandString)

        # Sends the response back to the channel
        slackClient.api_call(
            "chat.postMessage",
            channel=channel,
            text=response
        )

    def _get_current_channel_name(self, slackClient, channel):
        channel_name = None
        for chan in self._get_channel_list(slackClient, True):
            if channel == chan["id"]:
                channel_name = chan["name"]

        return channel_name

    def _get_channel_list(self, slackClient, includePrivate = True):
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

    def _get_help(self):
        response = ("DankMemeBot is currently operating in {0} meme mode, " +
            "and capable of acting on the following trigger words:").format(self._memeMode)
        response = response + "\n----------\n"

        for item in self._memes:
            if item["trigger"] not in response:
                response = response + "\n" + item["trigger"]
        
        response = response + "\n----------\n"
        response = response + ("\nUse command '{0}' " +
            "to toggle the current meme mode (random or sequential)").format(self._memeModeToggleString)

        return response

    def _get_memes(self, slackClient, command, channel):
        response = None
        channel_name = self._get_current_channel_name(slackClient, channel)
        for meme in self._memes:
            if command.lower().startswith(meme["trigger"].lower()):
                if meme["channel"] == channel_name:
                    response = self._get_meme(meme)
                elif meme["channel"] is None:
                    response = self._get_meme(meme)

        return response

    def _get_meme(self, meme):
        if len(meme["responses"]) == 1:
            return meme["responses"][0]

        if self._memeMode == "random":
            return meme["responses"][random.randrange(0, len(meme["responses"]) - 1)]

        if meme["index"] == len(meme["responses"]):
            meme["index"] = 0

        response = meme["responses"][meme["index"]]
        meme["index"] += 1
        return response


