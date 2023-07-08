import nltk
from discord.ext.commands import Context, command, Cog

from Config.Configs import VConfigs
from Config.Embeds import VEmbeds
from Config.Helper import Helper
from Music.JimBoi import JimBoi
from Utils.Chatbot import Chatbot, hostile_or_personal, info

helper = Helper()


class OpenAICog(Cog):
    """
    Class to listen to OpenAI commands
    """

    def __init__(self, bot: JimBoi) -> None:
        self.__bot: JimBoi = bot
        self.__embeds = VEmbeds()

        # Ensure that nltk is downloaded
        try:
            hostile_or_personal('Thats pretty wack yo')
            info('NLTK Loaded', 'good')

        except Exception as e:
            try:
                info('Downloading NLTK packages ...')
                nltk.download('punkt', quiet=True, raise_on_error=True)
                nltk.download('averaged_perceptron_tagger', quiet=True, raise_on_error=True)
                nltk.download('maxent_ne_chunker', quiet=True, raise_on_error=True)
                nltk.download('vader_lexicon', quiet=True, raise_on_error=True)
                nltk.download('words', quiet=True, raise_on_error=True)
                info('NLTK Loaded', 'good')

            except Exception as e:
                info('Failed to download NLTK data', 'bad')
                info(f'Unexpected error while downloading NLTK data: {e}', 'bad')

        # configs = VConfigs()
        # if configs.SONG_PLAYBACK_IN_SEPARATE_PROCESS:
        #     configs.setPlayersManager(ProcessPlayerManager(bot))
        # else:
        #     configs.setPlayersManager(ThreadPlayerManager(bot))

    @command(name="chat", help=helper.HELP_OPENAI, description=helper.HELP_OPENAI_LONG)
    async def chat(self, ctx: Context, *args) -> None:
        try:

            if len(args) > 1:
                track = " ".join(args)
            else:
                track = args[0]

            chatbot = Chatbot(VConfigs().OPENAI_KEY)
            response = chatbot.get_AI_response(chatbot.say_to_chatbot(track, outloud=False))
            await ctx.channel.send(response)
        except Exception as e:
            print(f'[ERROR IN COG] -> {e}')


def setup(bot):
    bot.add_cog(OpenAICog(bot))
