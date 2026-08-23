# Decisions

One entry per architectural choice: what was decided, when, why, and what would make us revisit it.
Newest at the top. Keep entries to a paragraph — this file is for re-orienting after a gap, not for
essays.

Status values: **Settled** · **Tentative** (working assumption, low cost to change) · **Open**
(blocking or unresolved).

---

## D-012 — Package name: `liminastra`
**Date:** 2026-08-23 · **Status:** Settled

*Limen* (the psychophysics term for the threshold of perception) + *astra*. The name binds the
detection-threshold idea to the domain without privileging either the visual or the digital head.
Verified free on PyPI and with zero repositories on GitHub at the time of the decision.

Rejected: `limina` — free on PyPI but collides with an active Python project (`theam/limina`) and
the `limina` GitHub org name is taken. Also considered and clean: `maglim`, `faintward`,
`magdepth`, `noctilimen`, `limenastra`.

Known near-misses, none of them blocking: `Liminastra` is a fictional sky-realm in an amateur
Wattpad story; `Luminastra` (different word) is a character in the Toivoa homebrew campaign
setting; `LiminAstral` is a French artist's social handle. No trademarks, no commercial use, no
overlap in class. **Accepted cost:** English speakers may drift toward the more familiar *lumin-*
root when recalling the name, so documentation and metadata carry the searchable terms instead.

## D-011 — License
**Date:** TBD · **Status:** Settled

MIT or BSD-3. Leaning BSD-3 for the explicit non-endorsement clause, which matters slightly more
for a package that will be cited in papers. Decide before the first public commit.

## D-010 — Falchi et al. World Atlas treated as optional user-supplied data
**Date:** 2026-08-21 · **Status:** Tentative — pending license verification

The World Atlas light-pollution data may carry a non-commercial restriction, which would make
bundling it in an open-source package awkward. Design accordingly: the atlas is an optional file
the user supplies, never shipped with the package, and manual sky-brightness entry is the
always-available path. This degrades gracefully offline regardless of how the license question
resolves. **Revisit when:** license terms are actually confirmed.

## D-009 — v1.0 scope frozen at V-band, clear-sky, point sources, single site
**Date:** 2026-08-21 · **Status:** Settled

The literature review covers far more than v1.0 should implement. Extended sources, multi-band,
and cloud effects are v2. Written down while still unattached to it, specifically to make later
scope creep visible as a decision reversal rather than drift.

## D-008 — Benchmarks against published values are the project's oracle
**Date:** 2026-08-21 · **Status:** Settled

`benchmarks/` encodes numbers from the literature — Bowen (1947) exit-pupil series, Krisciunas &
Schaefer (1991) worked cases, Crumey (2014) examples, SMTN-002 `m5` table — each with an explicit
pinned tolerance. Changing a tolerance requires a CHANGELOG entry. Rationale: agentic development
produces plausible-looking wrong physics unless there is an objective target to iterate against,
and un-pinned tolerances get quietly "adjusted" until they test nothing.

## D-007 — Crumey (2014) is the primary visual model; Schaefer is a comparison backend only
**Date:** 2026-08-21 · **Status:** Settled

Hecht's 1947 point-source formula — the basis of Schaefer (1990) and essentially every online
amateur calculator — has accelerating curvature in the scotopic range where faint-star detection
happens, while the laboratory data are compressive. Against Bowen's 1947 series, Crumey gives
0.09 mag RMS versus Schaefer's 0.37. Schaefer stays implemented behind the same interface for
comparison, because users will expect to see it, but it is never the default.

## D-006 — No dependency on `rubin_sim` or the observatory stack
**Date:** 2026-08-21 · **Status:** Settled

`rubin_sim` is excellent but pulls gigabytes of data files and a heavy dependency tree, which is
disproportionate for a package whose selling point is that it runs offline on a laptop. The `m5`
parameterisation is roughly a dozen lines — reimplemented here, cited to LSE-40 and SMTN-002, and
verified against their published values.

## D-005 — Units: `astropy.units` at API boundaries, suffixed floats internally
**Date:** 2026-08-21 · **Status:** Settled

Quantities at public boundaries for safety and discoverability; plain floats internally for speed
and readability, with the unit in the parameter name (`sky_mag_per_arcsec2`, `exposure_s`,
`aperture_m`). Angles radians internally, degrees at the boundary. Decided once deliberately,
because a units convention re-litigated mid-project is a full-codebase refactor.

## D-004 — Layering rule enforced by import-linter in CI
**Date:** 2026-08-21 · **Status:** Settled

Core physics and sky-model modules may not import from CLI or web adapters; only the data layer
touches the network or disk. Enforced mechanically rather than by convention, because this is the
constraint that makes the project contributable and it erodes silently otherwise.

## D-003 — Digital head ships before visual head
**Date:** 2026-08-21 · **Status:** Settled

The digital path is deterministic and has the best published benchmarks, so it gives the fastest
signal on whether the architecture works. A CLI-only tool that correctly computes imaging depth is
already useful to people, which makes an early `v0.1.0` release meaningful rather than a
placeholder.

## D-002 — NiceGUI for web and desktop, one codebase
**Date:** 2026-08-21 · **Status:** Settled

Writing a Qt app and a web app separately is the main trap in "desktop + web + CLI." NiceGUI is
pure Python and its native mode runs the same app in a desktop window via pywebview. Streamlit was
rejected: it packages poorly as a desktop app and fights on layout. **Revisit when:** custom UI
needs outgrow the component model — the fallback is FastAPI + HTMX + Jinja, which is a frontend
rewrite, not a project rewrite, provided D-004 holds.

## D-001 — Library-first with three thin frontends
**Date:** 2026-08-21 · **Status:** Settled

The core library is pure functions with dataclass inputs and outputs, no printing, no I/O, and no
knowledge that UIs exist. CLI (Typer), web, and desktop are all thin adapters over it. This is what
makes the physics independently testable and the project open to contributors who care about one
model rather than the whole application.
