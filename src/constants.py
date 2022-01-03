from .db import default_schedule


class Constants:
    smile = "😊"
    hello = "👋🏻"

    HELP_MESSAGE = (
        f"\n\nThis bot will send you random memories every day from your memory vault."
        f"\n- You can activate daily memory sending by writing, *join* or */join*"
        f"\n- Deactivate daily sending by, *leave* or */leave*"
        f"\n- Get a random memory by, *send* or */send*"
        f"\n- Get multiple random memories by, *send number*"
        f"\n- Get your status information by, *status* or */status*"
        f"\n- List memories by, *list* or */list*"
        f"\n- Learn how to support me by, *support* or */support*"
        f"\n- Delete a memory with command, *delete id*, you can get the memory id with the command, *list* or */list*"
        f"\nExample:"
        f"\n*delete 2*"
        f"\n- Add memories to your memory vault with command,  *add Sentence*"
        f"\nExample:"
        f"\n*add Time does not come back*"
        f"\n- Give feedback about the bot with command,  *feedback Sentence*"
        f"\n\n- Set your timezone with command, *gmt timezone*. Default timezone is GMT0."
        f"\nExamples:"
        f"\nGMT+3: *gmt 3*"
        f"\nGMT0: *gmt 0*"
        f"\nGMT-5: *gmt -5*"
        f"\n\n*Schedule related commands:*"
        f"\nThe default scheduled hours are *{default_schedule}*. You can add an hour multiple times to receive multiple memories"
        f"\n-Show your current schedule by, *schedule* or */schedule*"
        f"\n-Reset your schedule to the default schedule by, *schedule reset*"
        f"\n-Adds hours to your schedule by, *schedule add hour1 hour2 hour3*"
        f"\nExample:"
        f"\n*schedule add 1 3 9 11*"
        f"\n-Removes hour from your schedule by *schedule remove hour*"
        f"\nExample:"
        f"\n*schedule remove 8*"

        f"\n\nYou can use me in groups as well, just can add me to the group and make me admin."
        f"\nAlso you can have multiple memory vaults by using groups."
        f"\nFor example I would serve you well in a language learning group, where you add words to your memory vault."
    )

    BROADCAST_CHAT_ID = -1001786782026
    FEEDBACK_FORWARD_CHAT_ID = -683998033

    @staticmethod
    def start_message(name: str = "") -> str:
        return (
            f"Welcome onboard {name} {Constants.hello}"
            f"\nThis bot stores your memories in the memory vault and sends random memories every day."
            f"\n\nKeeping note of beautiful & important stuff that we come across throughout the life and remembering those memories is quite challenging. "
            f"\nThis bot solves this problem with a very simple approach, as complex methods makes it harder to keep them in our life."
            f"\nSincerely thanks to my wife Seyyide for the beautiful idea."
            f"\n\n-You can activate daily sending by writing, *join* or /join. "
            f"\n-You can get more detailed information by writing, *help* or /help."
        )
