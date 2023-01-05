from httpx import AsyncClient


class Packages:
    """
    Custom packages for users.
    """

    @staticmethod
    async def get_tr_stocks() -> str:
        URL = "https://api.genelpara.com/embed/borsa.json"

        async with AsyncClient() as client:
            request = await client.get(URL)
            js = request.json()
            USDTRY = (float(js["USD"]["satis"]) + float(js["USD"]["alis"])) / 2
            USD_DEGISIM = float(js["USD"]["degisim"])
            XU100 = (float(js["XU100"]["satis"]) + float(js["XU100"]["alis"])) / 2
            XU100_DEGISIM = float(js["XU100"]["degisim"])
            GA = (float(js["GA"]["satis"]) + float(js["GA"]["alis"])) / 2
            GA_DEGISIM = float(js["GA"]["degisim"])

            message = (
                f"*USD*: {USDTRY} -- % {USD_DEGISIM} \n"
                f"*XU100*: {XU100} -- % {XU100_DEGISIM} \n"
                f"*XU100/USD*: {XU100 / USDTRY} -- % {XU100_DEGISIM / USD_DEGISIM} \n"
                f"*GA*: {GA} -- % {GA_DEGISIM} \n"
            )
            return message

    functions = [get_tr_stocks]
    titles = ["TR Stocks & Currency"]
