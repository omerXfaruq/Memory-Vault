import sys

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

    PORT = 8000
    loop = asyncio.get_event_loop()
    if is_by_ngrok == "ngrok":
        http_tunnel = ngrok.connect(PORT, bind_tls=True)
        public_url = http_tunnel.public_url
        Events.HOST_URL = public_url
    else:
        public_url = loop.run_until_complete(Events.get_public_ip())
        Events.HOST_URL = public_url

    success = loop.run_until_complete(Events.set_telegram_webhook_url())
    if success:
        uvicorn.run(
            "src.listener:app",
            host="127.0.0.1",
            port=PORT,
            reload=True,
            log_level="info",
        )
    else:
        print("Fail, closing the app.")
