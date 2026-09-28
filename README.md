# Homnick Planner

Family schedule + to-do planner at **https://jhomnick.github.io/planner**.

- **Views:** To-do list · Day planner (hour by hour) · Priorities · Next 7 days · Next few weeks
- **Print:** the Print button makes a one-page summary (today's schedule, top priorities, next 3 days, deadlines for 4 weeks, notes box). Choose "Save as PDF" in the print dialog for a PDF.
- **Interactive:** add items, check them off, change priority, skip one occurrence, hide or delete.
- **Repeats:** every N hours (between two times), daily / every N days (2 = every other day), weekly on chosen days / every N weeks, monthly, yearly, each with an optional end date.

## Privacy
GitHub Pages is public, so nothing readable is published:
- `feed.enc.json` (calendar + email digest) is AES-256-GCM encrypted with the family passphrase (PBKDF2-SHA256, 250k rounds). The page decrypts it in the browser.
- Items the family adds or checks off are encrypted with the same key before they go to Firebase.
- `feed.json` (plaintext) is git-ignored and must never be committed.

## How updates work
A Claude scheduled task runs several times a day. It reads Google Calendar (personal, The Homnicks, Family), the Outlook work calendar and Gmail, writes `feed.json`, runs
`PLANNER_PASS='…' python3 encrypt_feed.py`, and commits only `feed.enc.json`. Open pages pick up the new feed within 15 minutes, or immediately with the ↻ button.

## Turning on family sync (one-time, ~5 minutes)
Without this, check-offs and new items stay on the device where they were made.

1. Go to https://console.firebase.google.com — reuse the Movie Nights project or create a new one.
2. Build → Firestore Database → Create database (production mode).
3. Firestore → Rules, paste and Publish:
   ```
   rules_version = '2';
   service cloud.firestore {
     match /databases/{db}/documents {
       match /planner/{space}/docs/{doc} {
         allow read, write: if true;   // contents are encrypted with the family passphrase
       }
     }
   }
   ```
4. Project settings → Your apps → Web app (</>) → copy the `firebaseConfig = { … }` block.
5. Paste it into `FIREBASE_CONFIG` near the top of the script in `index.html` (so every device gets it), or into the planner's ⚙︎ Settings on each device.

## Passphrase
Stored only in the scheduled task and on devices where "Remember on this device" was ticked. To change it, update the scheduled task's prompt; everyone re-enters the new one (⚙︎ → Lock this device).
