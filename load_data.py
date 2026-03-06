import os
import time
from dotenv import load_dotenv
import libsql
from datetime import datetime
load_dotenv()


from get_yfinance_data import get_current_price


def positive_or_negative_percent(percent):
    if percent > 0:
        return f"+{percent}%"
    return f"{percent}%"

def emoji(value):
    if value > 0:
        return "📈"
    return "📉"

def replace_ticker(ticker):
    return ticker.replace(".WA", "")


def positive_or_negative_value(value):
    if value > 0:
        return f"+{value}"
    return f"{value}"



def load_data_for_post():
    url = os.getenv("TURSO_DATABASE_URL")
    auth_token = os.getenv("TURSO_AUTH_TOKEN")

    conn = libsql.connect("walletdb.db", sync_url=url, auth_token=auth_token)
    conn.sync()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM portfel")
        rows = cur.fetchall()
    except:
        print("Najpierw wczytaj dane z XTB!")
        time.sleep(3)
        return
    print("Pobieranie aktualnych cen rynkowych...")


    tickers = [ticker[1] for ticker in rows] # Wszystkie tickery
    current_prices = get_current_price(tickers)  # AKTUALNE CENY

    info = {}
    wallet_value = 0
    for row in rows:
        ticker = row[1]
        volume = row[2]
        avg_price = float(row[3])

        current_price = float(current_prices[ticker]["price"])
        daily_ptc_change = current_prices[ticker]["change_percent"]

        starting_value = volume * avg_price
        new_value = volume * current_price
        total_return = new_value - starting_value
        return_percentage = ((current_price / avg_price) - 1) * 100

        info[ticker] = {
            "volume": volume,
            "avg_price": avg_price,
            "return_percentage": round(return_percentage, 2),
            "starting_value": round(starting_value, 2),
            "new_value": round(new_value, 2),
            "total_return": round(total_return, 2),
            "daily_change": daily_ptc_change
        }
        wallet_value += new_value

    # info = {
    #     ticker: {
    #         "volume": volume,
    #         "avg_price": avg_price,
    #         "return_percentage": % of return,
    #         "starting_value": value of position (volume * avg_price)
    #         "new_value": new_value of position in pln,
    #         "total_return": total return of position in pln
    #     }
    # }
    # Nowa cena / srednia cena - 1 * 100 = o ile procent wzroslo

    date = datetime.now().strftime("%d.%m.%Y")
    data_to_post = f"📊 Portfel [{date}] 🇵🇱\n\n"

    old_value = 0

    for ticker in tickers:

        old_value += info[ticker]["starting_value"]
        data_to_post += f"{emoji(info[ticker]["return_percentage"])} ${replace_ticker(ticker)} | {info[ticker]["volume"]}szt. | {round(info[ticker]["volume"]*current_prices[ticker]["price"], 2)}zł | {positive_or_negative_percent(info[ticker]["return_percentage"])}\n"




    total_return_ptc_sum = round(((wallet_value / old_value) - 1) * 100, 2)
    total_return_sum = 0
    for ticker in info.keys():
        total_return_sum += info[ticker]["total_return"]

    data_to_post += f"\n💼 Suma: {round(wallet_value, 2)}zł | {positive_or_negative_value(round(total_return_sum, 2))}zł | {positive_or_negative_percent(total_return_ptc_sum)} {emoji(total_return_ptc_sum)}"









    with open("xd.txt", "w", encoding="UTF8",) as f:
        f.write(data_to_post)

    conn.close()
    return data_to_post



