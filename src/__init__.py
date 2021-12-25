import sys
import os

from pyngrok import ngrok
import uvicorn
import asyncio

from .events import Events

__all__ = []

if __name__ == "__main__":
    if Events.TOKEN is None:
        sys.exit("No TELEGRAM_TOKEN found in the environment, exiting now.")

    # Run with ngrok if the parameter is given
    is_by_ngrok = None
    if len(sys.argv) == 2:
        is_by_ngrok = sys.argv[1]

    PORT = 8443
    loop = asyncio.get_event_loop()
    if is_by_ngrok == "ngrok":
        ngrok_token = str(os.environ.get("NGROK_AUTH_TOKEN"))
        if ngrok_token is None:
            print("NGROK auth token is not found in the environment. Ngrok will timeout after a few hours.")
        else:
            ngrok.set_auth_token(ngrok_token)
        http_tunnel = ngrok.connect(PORT, bind_tls=True)
        public_url = http_tunnel.public_url
        Events.HOST_URL = public_url
    else:
        public_url = loop.run_until_complete(Events.get_public_ip())
        Events.HOST_URL = f"https://{public_url}:{PORT}"

    print(Events.HOST_URL)
    success = loop.run_until_complete(Events.set_telegram_webhook_url())
    if success:
        uvicorn.run(
            "src.listener:app",
            host="0.0.0.0",
            port=PORT,
            reload=True,
            log_level="info",
        )
    else:
        print("Fail, closing the app.")
