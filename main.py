from dotenv import load_dotenv
import os

load_dotenv()

from RocketBot import RocketBot
from RocketBot import Info
from RocketBot import AssignTask
from RocketBot import testing
bot = RocketBot()

if __name__ == '__main__':
    bot.add_cog(testing(bot))
    bot.add_cog(AssignTask(bot))
    bot.add_cog(Info(bot))
    bot.run(os.getenv("TOKEN"))
