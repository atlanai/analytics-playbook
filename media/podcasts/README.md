# Podcast audio

The three episodes are the listening alternative to the guide's reading tracks. Small Listen links on the cover and reading paths open one dismissible player. It keeps playing as visitors navigate chapters in the main guide. The compact episode list lives at `#listen`, with a transcript link for each episode.

Regenerated on 27 October 2026 from source revision `b0d905c13c1a5299cf3a433a2b93c14842eb952d`.

| File | Track | Duration | Transcript |
|---|---|---|---|
| [01-sponsoring-it.mp3](01-sponsoring-it.mp3) | Sponsoring it | 9:34 | [Read transcript](01-sponsoring-it.transcript.txt) |
| [02-building-it.mp3](02-building-it.mp3) | Building it | 19:35 | [Read transcript](02-building-it.transcript.txt) |
| [03-running-it.mp3](03-running-it.mp3) | Running it | 15:18 | [Read transcript](03-running-it.transcript.txt) |

These are full-length NotebookLM conversations encoded as mono MP3 at 96 kbps, about 32 MB combined. The shared player uses `preload="none"` and has no audio source until a visitor clicks Listen. Native audio controls remain available when JavaScript is disabled. The site build copies the audio, transcripts and editorial notes beside the generated pages.

The transcripts come from NotebookLM's transcription of the new recordings. Obvious spelling of names and technical terms has been corrected. The episodes are AI-generated; read [episode clarifications](editorial-notes.txt) for what the hosts got wrong or overstated.

`podcasts.json` records the source revision, source chapters, durations, file hashes and transcript paths. To replace an episode, update its MP3, transcript and provenance record, then its title and duration labels in `chapters/podcasts.md`, `chapters/00-start.md` and `README.md`. Run `python3 build.py --check --site _site` and verify playback and transcript links.

The standalone `playbook.html` uses relative media paths. Keep `media/podcasts/` beside it when sharing an offline copy with audio.
