# Chant Project — Claude Context

## Purpose
This project produces liturgical music (Gregorian chant) for Catholic Mass and the Liturgy of the Hours. Work includes:
- Sourcing and adapting chants (Latin and English) for specific liturgical days
- Composing English GABC adaptations of Gregorian chants
- Compiling Mass propers into LaTeX/PDF handouts

## Python environment
All Python scripts use: `~/liturgio/.venv/Scripts/python`

## Database
Local MySQL on localhost:3306, database `liturgio`.
- Read user: `liturgio_ro` — keyring service `liturgio-mysql`, key `liturgio_ro`
- Write user: `jcost` — keyring service `liturgio-mysql`, key `jcost`
- Use the `get_ro_engine`/`get_rw_engine` pattern from
  [`liturgio-tools`](https://github.com/drj-chantschool/liturgio-tools)
  (`liturgio_tools/cli.py`) for connections.

Key tables:
- `proper_of_seasons` — date + jurisdiction → `lit_day_id`
- `liturgical_day` — `lit_day_id` → title, season, subseason, wknum, seq, lit_rank (also: slug, lit_day_order)
- `lit_part_assignment` — (jurisdiction, part_id, season, subseason, wknum) + day selector → `chant_group_id` + `assignment_authority_code`
  - `wkday` NULL=all days, 1=Sun…7=Sat (use for typical weekly assignments)
  - `seq` — use instead of wkday for days where liturgical sequence ≠ calendar weekday (Christmas octave, Dec 17–24, Ascension US)
  - `cycle_sun` — Sunday lectionary year: A=1, B=2, C=0 (liturgical_year mod 3); NULL=all years
  - `cycle_wk` — Weekday lectionary year: mod 2; NULL=all years. At most one of cycle_sun/cycle_wk is non-null.
- `chant_group` — groups Latin + English chant versions under a canonical name
- `gregobase_chants` — Latin GABC (id, incipit, gabc, office-part, mode, version, transcriber, commentary)
- `gregobase_chant_sources` — chant_id + source_id + page (GR page numbers; source 2 = 1961 GR, source 4 = 1974 GR)
- `gregobase_sources` — source registry (id, title, year); key sources: 1=GR 1908, 2=GR 1961, 3=Liber Usualis 1961, 4=GR 1974, 16=Gregorian Missal 1990
- `gregobase_chant_group_map` — gregobase_id → chant_group_id
- `gregobase_chants_texts` — extracted plain text of chants (id=gregobase_id, `text`=Latin with accents preserved, `text_decode`=ASCII-normalized lowercase). Use `text` for Latin provenance; note initial capital may be split/uppercased from GABC encoding.
- `local_chants` — English GABC adaptations. PK: `local_chant_id` (char(36) UUID). Key columns: `chant_group_id`, `version` (default 'english'), `incipit`, `office-part`, `mode`, `mode_var`, `transcriber` (default 'Doctor J'), `commentary`, `notation` (default 'gabc'), `gabc` (longtext), `translation_source_code`, `source_citation`, `is_text_exact`, `derived_from_uid`, `status` (default 'draft'), `notes`, `created_at`, `updated_at`
- `lit_part_texts` — antiphon texts keyed by season/subseason/wknum/wkday/cycle_sun with both Latin (`original_text`) and English (`vernacular_text`). Key columns: `translation_source_code` (translation authority), `page_num` (page in that source), `text_src` (scriptural citation, e.g. "Cf. Ps 66(65):1-2"), `assignment_authority_code`. Check here first before fetching from liturgies.net.
- `service_part` — in=Introit, gr=Gradual, al=Alleluia, of=Offertory, co=Communion
- `p_assignment_authority` — GRADUALE, MISSAL, OCM (Ordo Cantus Missae), OCO (Ordo Cantus Officii), CUSTOM
- `p_translation_source` — reference table of translation source codes (`translation_source_code`, `display_name`, `sort_order`, `is_active`); query this table for the current list rather than hardcoding source codes

## GABC format
Chant files use the GABC notation:
```
name:Incipit text;
office-part:Introit;
mode:8;
book:Graduale Romanum, 1961, p. 123;
transcriber:Name;
%%
(c3) Syl(gh)la(h)ble(f.) by(h) syl(hi)la(h)ble(f.)
```
Header fields followed by `%%`, then body with `syllable(neumes)` pairs.
Clefs: `(c3)`, `(f3)`, etc. Barlines: `(:)` `(;)` `(,)` `(.)` in parens.

## File structure
- `Antiphona/`, `Communio/`, `Introitus/`, `Gradual/`, `Offertorium/`, `Alleluia/` — chant folders by type
- Each chant has its own subdirectory (kebab-case incipit), with one or more `.gabc` files
- `!References/` — reference PDFs (Graduale Romanum, Liber Usualis, LotH, etc.)
- `loth.cls` — LaTeX class for LotH documents

## Latin text verification
Always use `gregobase_chants_texts.text` (or the GABC body) as the authoritative Latin — do not assume Vulgate. The GR chant text may differ from the Vulgate.

## Translation sourcing priority (composer's-assistant workflow only)
When sourcing a NEW English translation for a chant (composer's-assistant Step 2d), the most-used sources are checked in roughly this order: ROMAN_MISSAL_2010_ICEL → GREGORIAN_MISSAL → ABBEY_PSALMS_CANTICLES → NEW_AMERICAN_BIBLE, then adapt. **This is a priority order for the common case, not the full set of valid `translation_source_code` values** — `p_translation_source` also includes SAINT_JOSEPH_MISSAL_1961, LFM, LOTH_1975_ICEL, LITURGIA_HORARUM_1985, and possibly others added later. Always query `p_translation_source` for the authoritative list (e.g. when populating a dropdown or validating a code) rather than relying on this list.

## CLI tool: liturgio-tools
Used by the composer's assistant. Lives in the
[`liturgio-tools`](https://github.com/drj-chantschool/liturgio-tools) repo
(`liturgio_tools/cli.py`), installed into `~/liturgio/.venv`. Invoke as
`~/liturgio/.venv/Scripts/liturgio-tools <command>` (or
`~/liturgio/.venv/Scripts/python -m liturgio_tools.cli <command>`). See that
repo's README for the full command reference. The interactive
`fix_missing_scores.py` and `upload_english_chants.py` tools, and the
`translations/` scraping pipeline, also now live there
(`liturgio_tools/fix_missing_scores.py`,
`liturgio_tools/upload_english_chants.py`,
`liturgio_tools/translations/`).
