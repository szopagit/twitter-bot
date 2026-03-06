# Twitter-bot
[**Link to the bot**](https://x.com/IdiotaZGPW)

---

### What does the bot do?
Every weekday at 5:00 PM the bot posts on X the current state of my investment portfolio with Polish stocks. It fetches data from a cloud database (Turso), which gets its data from an XLSX file exported from XTB. Details on how the data is saved to the database can be found in the [**Investment Portfolio**](https://github.com/szopagit/Portfel-Inwestycyjny) repository.

---

### Tech stack
- Python
- GitHub Actions (schedule Mon-Fri 5:00 PM)
- Turso (SQLite cloud database)
- X API v2
