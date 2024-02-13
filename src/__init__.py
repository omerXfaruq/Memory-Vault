import sys
import os

from pyngrok import ngrok
import uvicorn
import asyncio

from .events import Events
from .constants import Constants

__all__ = []

if __name__ == "__main__":
    if Events.TOKEN is None:
        sys.exit("No TELEGRAM_TOKEN found in the environment, exiting now.")

    PORT = Events.PORT
    loop = asyncio.get_event_loop()

    # Run with ngrok if the parameter is given
    running_option = None
    if len(sys.argv) == 2:
        running_option = sys.argv[1]

    if running_option == "ngrok":
        ngrok_token = str(os.environ.get("NGROK_TOKEN"))
        if ngrok_token == "None":
            print(
                "NGROK auth token is not found in the environment. Ngrok will timeout after a few hours."
            )
        else:
            print(f"NGROK TOKEN: {ngrok_token}")
            ngrok.set_auth_token(ngrok_token)
        http_tunnel = ngrok.connect(PORT, bind_tls=True)
        ssh_tunnel = ngrok.connect(22, "tcp")
        public_url = http_tunnel.public_url
        ssh_url = ssh_tunnel.public_url
        Events.HOST_URL = public_url
        _ = loop.run_until_complete(
            Events.send_a_message_to_user(
                Constants.BROADCAST_CHAT_ID, f"ssh: {ssh_url}, http:{public_url}"
            )
        )
    else:
        public_url = loop.run_until_complete(Events.get_public_ip())
        Events.HOST_URL = f"https://{public_url}"
        if running_option == "self_signed":
            Events.SELF_SIGNED = True

    print(Events.HOST_URL)
    success = loop.run_until_complete(Events.set_telegram_webhook_url())

    if success:
        uvicorn.run(
            "src.listener:app",
            host="0.0.0.0",
            port=PORT,
            reload=False,
        )
    else:
        print("Fail, closing the app.")
