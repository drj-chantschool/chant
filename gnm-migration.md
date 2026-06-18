# GNM → lit_part_assignment Migration

## What was done

A previous session read all `.tex` files in `GNM/OT/`, `GNM/TQ/`, `GNM/TP/`, and `GNM/Feasts/`, extracted every `\gregorioscore{...}` reference for introits, offertories, and communions, resolved each chant's `chant_group_id` (by checking `local_chants` for English versions and disambiguating by office-part), and inserted `lit_part_assignment` records.

### Inserted: 194 assignments total

- **Ordinary Time**: Weeks 1–5, 11–12, 14–19, 21–34 (all from `GNM/OT/`)
- **Lent**: Ash Wed week (Thu only), weeks 1–5 (Thu/Fri only, matching what the tex files covered) (from `GNM/TQ/`)
- **Feasts**: St. Agatha (Feb 5), St. Joseph (Mar 19), St. Barnabas (Jun 11), St. Thomas (Jul 3), St. Ignatius (Jul 31), St. Maximilian Kolbe (Aug 14), Assumption (Aug 15), St. Pius X (Aug 21), St. Augustine (Aug 28), Archangels (Sep 29), Guardian Angels (Oct 2)
- All inserted with `needs_review = 1` and `assignment_authority_code = 'GRADUALE'`, except:
  - `majorem-caritatem` as communion for Aug 14 → `MISSAL` (offertory chant used as communion per Missal text match)
  - `in-conspectu-angelorum` as communion for Oct 2 → `MISSAL` (antiphon used as communion per Missal)

### Not inserted (already existed)

Easter weeks 2–4 and the octave Thursday (`PASC-AD_ASC-02` through `04`, `PASC-OCT-01-5`) — these already had 80 assignments from a prior migration.

### Supporting data created

- **9 `proper_of_saints` entries**: st-agatha, st-barnabas, st-thomas-apostle, st-ignatius-loyola, st-maximilian-kolbe, st-pius-x, st-augustine, archangels, guardian-angels
- **9 `lit_epoch` entries** (kind=`saint`): same slugs as above

### Notes on specific chants

- `laetatur-cor` (OT-30 introit folder slug) was mapped to cg 864 (`laetetur-cor`, in. mode 2) — likely a spelling variant in the folder name.
- `quinque-prudentes-virgines` (OT-21 Fri communion) was mapped to cg 3388 (`quinque-prudentes`, co. mode 5) — same chant.
- `de-ventre-matris-meae` (OT-27 Tue Yr II, ad libitum) mapped to cg 659 — no English chant uploaded yet.
- `Beatam me dicent` appearing in Aug 14's PDF was NOT assigned — it was an ad libitum after-communion meditation, not part of that day's liturgy.

## What remains

**Seasons not yet processed** — the GNM folder only covered OT, partial Lent, partial Easter, and select feasts. Assignments still needed for:

- **Advent** — tex files are elsewhere (not in GNM/). Ad te levavi (cg 132) for Advent I Sunday is one example; it has an English chant uploaded and ready.
- **Christmas / Epiphany**
- **OT weeks 6–10, 13, 20** — no GNM tex files exist for these weeks
- **Remaining Lent days** — the GNM tex files only covered Thursdays (and one Friday/Sunday); full-week coverage is still needed
- **Remaining Easter days** — Easter weeks 5–6 have assignments but weeks 1 (octave Mon–Wed, Fri–Sat) and some individual days within 2–4 may be incomplete
- **Additional feasts/solemnities** not in GNM (e.g., Corpus Christi, Sacred Heart, Christ the King, Immaculate Conception, etc.)
- **MISSAL authority rows** — the current batch is all GRADUALE. Where `lit_part_texts` has matching text for a given day, a duplicate row with `assignment_authority_code = 'MISSAL'` should be added.

## Technical reference

### How to insert an assignment

```python
import keyring
from sqlalchemy import create_engine, text

pw = keyring.get_password('liturgio-mysql', 'jcost')
engine = create_engine(f'mysql+mysqlconnector://jcost:{pw}@localhost:3306/liturgio')

with engine.begin() as conn:
    conn.execute(text('''
        INSERT INTO lit_part_assignment
        (jurisdiction, part_id, lit_epoch_slug, cycle_sun, cycle_wk,
         chant_group_id, assignment_authority_code, notes, needs_review)
        VALUES (:jurisdiction, :part_id, :lit_epoch_slug, :cycle_sun, :cycle_wk,
                :chant_group_id, :assignment_authority_code, :notes, 1)
    '''), {
        'jurisdiction': 'UNIVERSAL',
        'part_id': 1,           # 1=in, 8=of, 9=co
        'lit_epoch_slug': 'ADV-I-01',  # week-level or day-level
        'cycle_sun': None,      # A=1, B=2, C=0, NULL=all
        'cycle_wk': None,       # mod 2, NULL=all
        'chant_group_id': 132,
        'assignment_authority_code': 'GRADUALE',
        'notes': None,
    })
```

### lit_epoch_slug format

The slug references `lit_epoch.slug` (FK). Format: `{season}-{subseason}-{wknum:02d}` for a week, `{season}-{subseason}-{wknum:02d}-{seq}` for a specific day. Saints use `proper_of_saints.slug` directly.

Examples:
- `OT-OT-01` = all of OT week 1
- `OT-OT-01-1` = OT week 1 Sunday
- `TQ-LENT-00-5` = Thursday after Ash Wednesday
- `TQ-LENT-01-1` = 1st Sunday of Lent
- `PASC-AD_ASC-03` = all of Easter week 3
- `PASC-OCT-01-5` = Thursday of Easter Octave
- `ADV-I-01-1` = 1st Sunday of Advent
- `assumption` = Assumption (saint slug)
- `st-joseph` = St. Joseph (saint slug)

### Resolving chant_group_id

1. Check `local_chants` for an English version with matching incipit — if exactly one `chant_group_id` has a `version LIKE 'english%'` row, use that.
2. If ambiguous, filter by office-part from `chant_group.canonical_name` (contains `(in. mode X)`, `(of. mode X)`, `(co. mode X)`).
3. If no `local_chants` match, use `chant_group.canonical_name` filtered by office-part.

### Authority code rules

- **GRADUALE**: Default for GR-assigned chants.
- **MISSAL**: When the chant's text matches what `lit_part_texts` has for that day. Both GRADUALE and MISSAL can apply to the same chant (two rows).
- **MISSAL only**: When the liturgical position doesn't match the chant type (e.g., an offertory chant or plain antiphon used at communion).
- Ignore OCM for now.

### Scripts

- `GNM/insert_assignments.py` — the script that performed this batch insert (194 rows)
- `GNM/gen_csv.py` — generated an intermediate CSV for review (now superseded)
