# Greek Wordle Discord Bot

Ένα διαδραστικό Discord bot που μεταφέρει την εμπειρία του Wordle στα Ελληνικά! Οι χρήστες μπορούν να δοκιμάζουν καθημερινά μία πεντάγραμμη ελληνική λέξη, να διατηρούν streaks και να συναγωνίζονται σε ένα ζωντανό leaderboard.

## Χαρακτηριστικά:

- `Καθημερινή πρόκληση`: Κάθε χρήστης έχει μία προσπάθεια την ημέρα να βρει τη λέξη των 5 γραμμάτων.
- `Streaks`: Παρακολούθηση συνεχόμενων επιτυχιών.
- `Leaderboard`: Κατάταξη παικτών βάσει των νικών και των streaks τους.
- `Υπενθυμίσεις`: Ειδοποιήσεις για χρήστες που έχουν αδρανήσει πάνω από 24 ώρες.
- `Υποστήριξη Ελληνικής γλώσσας`: Όλες οι λέξεις, απαντήσεις και μηνύματα είναι στα Ελληνικά.
  
---

##  Εκτέλεση Bot

  Δημιούργησε ένα αρχείο `.env` στο ίδιο directory με το εξής περιεχόμενο:

```ini
DISCORD_TOKEN= το_token_του_bot
GUILD_ID= το_guild_id
```

> - Το DISCORD_TOKEN είναι το token του bot σου από το Discord Developer Portal.
> - Το GUILD_ID είναι το ID του Discord server (guild) όπου θες να λειτουργεί το bot.

---

## Python Libraries

```bash
pip install discord.py python-dotenv
```

---

## Χρήση εντολών

Μόλις μπει το bot στον server σου, μπορείς να χρησιμοποιήσεις τις παρακάτω Slash Commands:

- `/wordlegr`
Ξεκινάς το ημερήσιο Wordle (αν δεν έχεις ήδη παίξει).

- `/guess (λέξη)`
Κάνεις μία μαντεψιά 5-γράμματης ελληνικής λέξης. Εμφανίζει τα αντίστοιχα emoji αποτελέσματα:

🟩 σωστό γράμμα στη σωστή θέση

🟨 σωστό γράμμα σε λάθος θέση

⬛ γράμμα που δεν υπάρχει στη λέξη

- `/leaderboard`
Εμφανίζει τους top παίκτες με βάση τις νίκες και τα streaks.

---

## Εικόνες

- ###  Εντολές
<p align="center">
  <img src="https://github.com/user-attachments/assets/0d5e4e72-3e2a-4d9f-bb1b-a4ca1bc012d3" alt="Wordle" width="1000"/><br><br>
  <img src="https://github.com/user-attachments/assets/cdcde35c-1b7e-49cf-bf2c-387a9c93d301" alt="Wordle" width="800"/>
</p>


- ### Ροή παιχνιδιού

<table>
  <tr>
    <td align="left">
      <img src="https://github.com/user-attachments/assets/9511f37d-6180-4e07-a780-256db691877e" alt="Wordle" width="500"/>
    </td>
    <td align="right">
      <img src="https://github.com/user-attachments/assets/712f3e50-a47d-4475-90c7-1adf65692e45" alt="Wordle" width="500"/>
    </td>
  </tr>
</table>

