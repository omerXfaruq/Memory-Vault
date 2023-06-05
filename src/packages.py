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
            USDTRY = round(USDTRY, 2)
            USD_DEGISIM = float(js["USD"]["degisim"])
            USD_DEGISIM = round(USD_DEGISIM, 2)
            XU100 = (float(js["XU100"]["satis"]) + float(js["XU100"]["alis"])) / 2
            XU100 = round(XU100, 2)
            XU100_DEGISIM = float(js["XU100"]["degisim"])
            XU100_DEGISIM = round(XU100_DEGISIM, 2)
            GA = (float(js["GA"]["satis"]) + float(js["GA"]["alis"])) / 2
            GA = round(GA, 2)
            GA_DEGISIM = float(js["GA"]["degisim"])
            GA_DEGISIM = round(GA_DEGISIM, 2)
            try:
                XU100USD = round(XU100 / USDTRY, 2)
            except:
                XU100USD = 0
            try:
                XU100USD_DEGISIM = round(XU100_DEGISIM / USD_DEGISIM, 2)
            except:
                XU100USD_DEGISIM = 0

            try:
                XAUUSD = round(GA / USDTRY * 31.1, 2)
            except:
                XAUUSD = 0

            try:
                XAUUSD_DEGISIM = round(GA_DEGISIM / USD_DEGISIM, 2)
            except:
                XAUUSD_DEGISIM = 0

            message = (
                f"*USD*: {USDTRY} -- % {USD_DEGISIM} \n"
                f"*XU100*: {XU100} -- % {XU100_DEGISIM} \n"
                f"*XU100/USD*: {XU100USD} -- % {XU100USD_DEGISIM} \n"
                f"*GA*: {GA} -- % {GA_DEGISIM} \n"
                f"*XAUUSD*: {XAUUSD} -- % {XAUUSD_DEGISIM} \n"
            )
            return message

    functions = [get_tr_stocks]
    titles = ["TR Stocks & Currency"]
