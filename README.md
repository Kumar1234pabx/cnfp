# SPSMUN 3.0 — Delegate Portal

Two-page, zero-backend portal for SPSMUN 3.0 delegates.  
Delegates enter their phone number → instantly see their name, class, committee, and portfolio.

---

## Folder structure

```
spsmun/
├── index.html      ← Login page (also holds the delegate database)
├── profile.html    ← Delegate profile page
├── update_db.py    ← Run this whenever you update the Excel file
├── Kartik.xlsx     ← Your Excel data source (keep alongside the script)
└── README.md
```

---

## How to update the database

1. Edit **Kartik.xlsx** (add/change/remove rows as needed — do NOT rename columns).
2. In a terminal, `cd` into the `spsmun/` folder.
3. Run:
   ```bash
   python update_db.py
   ```
   This re-reads the Excel file and automatically rewrites the delegate data inside `index.html`.
4. Re-upload `index.html` to your host. That's it.

Dependencies (one-time install):
```bash
pip install pandas openpyxl
```

---

## Publishing options

### Option A — Netlify (recommended, free, 2 minutes)

1. Go to [netlify.com](https://netlify.com) → **Add new site → Deploy manually**.
2. Drag-and-drop the `spsmun/` folder onto the drop zone.
3. Netlify gives you a free URL like `https://spsmun-xyz.netlify.app`.
4. **Custom domain**: In Netlify → Domain settings → add `portal.satlujmun.com` (or any subdomain) and point your DNS CNAME there.
5. After every database update, repeat step 2 (just drag-drop again; Netlify keeps history).

### Option B — GitHub Pages (free, auto-deploy)

1. Create a GitHub repo (private or public).
2. Push the `spsmun/` folder contents to the `main` branch (files at root level, not inside a subfolder).
3. Go to repo **Settings → Pages → Source: main / root**.
4. Your site appears at `https://<username>.github.io/<repo>/`.
5. After updating the Excel and running `update_db.py`, commit & push `index.html` — GitHub Pages auto-redeploys in ~30 seconds.

### Option C — Any static host (cPanel, hosting panel)

1. Log in to your hosting panel → File Manager.
2. Upload `index.html` and `profile.html` to `public_html/portal/` (or any subfolder).
3. Access at `https://yourdomain.com/portal/`.
4. After a database update, just re-upload `index.html`.

---

## How login works (no backend required)

- All 170 delegate records are embedded as a JSON array in `index.html`.
- When a delegate enters their phone number, JavaScript looks it up client-side — no server call needed.
- On match, the delegate object is stored in `sessionStorage` and the user is redirected to `profile.html`.
- `profile.html` reads from `sessionStorage` and renders the profile. If the session is empty (direct URL access), it redirects back to login automatically.

---

## Excel column requirements

The script reads these exact column headers (case-sensitive):

| Column | Used for |
|--------|----------|
| Name | Delegate name |
| Class | e.g. 9th, 10th |
| Section | e.g. Shakespeare |
| Portfolio | Country or role |
| Committee | e.g. UNSC, WHO |
| Contact | 10-digit phone number (login key) |

Do not rename or delete these columns.

---

## Security note

This is a school event portal with no sensitive personal data. Phone numbers are used as a convenient lookup key, not as authentication. If you need stronger access control for a future edition, consider adding a Netlify serverless function or a Supabase backend — contact the site maintainer for guidance.

---

## Agenda updates

Committee agendas are defined in `profile.html` inside the `COMMITTEE_META` object. To update an agenda:

1. Open `profile.html` in any text editor.
2. Find the `COMMITTEE_META` object near the bottom of the `<script>` block.
3. Edit the `agenda` array for the relevant committee.
4. Save and re-upload `profile.html`.

For the full official agenda, delegates are directed to **satlujmun.com**.
