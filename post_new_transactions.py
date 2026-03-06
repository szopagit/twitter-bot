import requests
from dotenv import load_dotenv
from requests_oauthlib import OAuth1
import os
import libsql
load_dotenv()

def post_new_transaction():
    content = "🔔 Nowe tranzakcje:\n"
    url = os.getenv("TURSO_DATABASE_URL")
    auth_token = os.getenv("TURSO_AUTH_TOKEN")

    conn = libsql.connect("walletdb.db", sync_url=url, auth_token=auth_token)
    conn.sync()
    cur = conn.cursor()

    cur.execute("SELECT * FROM new_transactions")
    rows = cur.fetchall()

    if not rows:
        print("Brak nowych")
        return

    new_transactions = {}
    type = ""
    for row in rows:
        if row[4] == "Stock purchase":
            type = "🟢 Zakup"
        if row[4] == "Stock sale":
            type == "🔴 Sprzedaż"
        if row[1] not in new_transactions.keys():
            new_transactions.update({row[1]: {"volume": float(row[2]), "price": row[3], "type": type}})
        else:
            new_transactions[row[1]]["volume"] += float(row[2])

    for ticker, info in new_transactions.items():
        content += f"{info["type"]} | {ticker} | Ilość: {info["volume"]} szt. | Po cenie: {info["price"]} zł/szt. | Wartość: {round(float(info["volume"])*float(info["price"]), 2)}zł\n"


    print(new_transactions)
    print(content)


    url = "https://api.twitter.com/2/tweets"
    API_KEY = os.getenv("API_KEY")
    API_SECRET = os.getenv("API_SECRET")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
    auth = OAuth1(
        API_KEY,
        API_SECRET,
        ACCESS_TOKEN,
        ACCESS_TOKEN_SECRET
    )

    response = requests.post(
        url,
        json={"text": content},
        auth=auth
    )

    response.raise_for_status()

    cur.execute("DELETE FROM new_transactions")
    conn.commit()

if __name__ == "__main__":
    post_new_transaction()