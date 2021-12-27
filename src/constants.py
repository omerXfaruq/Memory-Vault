class Constants:
    HELP_MESSAGE = (
        f"\n\nThis bot will send you a random memory at every midday from your memory vault."
        f"\n- You can join my system by writing, *join* or */join*"
        f"\n- Leave my system by, *leave* or */leave*"
        f"\n- Get a random memory by, *send* or */send*"
        f"\n- Get your status information by, *status* or */status*"
        f"\n- List memories by, *list* or */list*"
        f"\n- Learn how to support me by, *support* or */support*"
        f"\n- Delete a memory with command, *delete id*. You can get the memory id with the command, *list*"
        f"\n*Example*:"
        f"\n*delete 2*"
        f"\n- Add memories to your memory vault with command,  *add Sentence*"
        f"\n*Example*:"
        f"\n*add Time does not come back*"
        f"\n- Give feedback about the bot with command,  *feedback Sentence*"
        f"\n\n- Set your timezone with command, *gmt timezone*. Default timezone is GMT0."
        f"\n*Examples*:"
        f"\nGMT+3: *gmt 3*"
        f"\nGMT0: *gmt 0*"
        f"\nGMT-5: *gmt -5*"
        f"\n\nYou can use me in groups as well, just can add me to the group and make me admin. Also you can have multiple memory vaults by using groups."
    )
    BROADCAST_CHAT_ID = -1001786782026
    FEEDBACK_FORWARD_CHAT_ID = -683998033

    @staticmethod
    def start_message(name: str = "") -> str:
        return (
            f"Welcome onboard {name} "
            f"\nThis bot stores your memories in the memory vault and sends a random memory every midday."
            f"\n\nKeeping note of beautiful & important stuff that we come across throughout the life and remembering those memories is quite challenging. "
            f"\nThis bot solves this problem with a very simple "
            f"approach, as complex methods makes it harder to keep it them in our life."
            f"\nSincerely thanks to my wife Seyyide for the beautiful idea."
            f"\n\n- You can join my system by writing, *join*. "
            f"\n- You can get more detailed information by writing, *help*."
        )
