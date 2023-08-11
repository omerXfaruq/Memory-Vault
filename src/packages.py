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

    @staticmethod
    async def get_yahoo_tr_stocks() -> str:
        import yfinance as yf

        key_list = {
            "USDTRY": "TRY=X",
            "EURTRY": "EURTRY=X",
            "ASELS": "ASELS.IS",
            "PGSUS": "PGSUS.IS",
            "EREGL": "EREGL.IS",
            "FROTO": "FROTO.IS",
            "KCHOL": "KCHOL.IS",
            "SAHOL": "SAHOL.IS",
            "SASA": "SASA.IS",
            "BIMAS": "BIMAS.IS",
            "TUR": "TUR",
        }
        words = []
        for key, value in key_list.items():
            info = yf.Ticker(value).info
            ask = info["ask"]
            previous = info["previousClose"]
            change = (ask - previous) / previous * 100
            words.append(f"{key}: {ask} --- %{round(change, 2)}")
        return "\n".join(words)

    functions = [get_tr_stocks, get_yahoo_tr_stocks]
    titles = ["TR Stocks & Currency", "Yahoo TR Stocks & Currency"]
