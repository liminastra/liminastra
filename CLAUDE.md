# CLAUDE.md


## What this project is

`liminastra` computes **limiting magnitudes** for both regimes over a shared sky model:

- **Visual head** — naked-eye and telescopic thresholds for a human observer (Crumey 2014 primary, Schaefer 1990/1993 as an alternative backend).
- **Digital head** — SNR-limited depth for CCD/CMOS detectors (Merline & Howell 1995, LSST `m5` parameterisation per LSE-40 / SMTN-002).

No existing package covers both. Professional ETCs ignore human vision and light pollution; amateur visual calculators run a 1990 model on a 1947 psychophysics formula that is known to be wrong in the scotopic regime.

Library-first, open-source (BSD-3), with three thin frontends: Typer CLI, NiceGUI web app, and the same NiceGUI app in native mode for Windows desktop.

## Hard rules

These are the ones that matter. Violating them produces plausible-looking wrong physics, which is the failure mode this project is most exposed to.

1. **Never invent a coefficient.** If a constant, exponent, or fit parameter is not in the cited source, stop and ask. Do not interpolate one from a nearby paper, and do not "reasonably estimate" one to make a test pass.
2. **Every physics function cites its source** in the docstring: author, year, and equation or table number. Format: `Crumey (2014), MNRAS 442, eq. 15`.
3. **Do not add `rubin_sim`, `lsst_*`, or any observatory stack as a dependency.** The `m5` parameterisation is ~12 lines; reimplement it and verify against the published table in SMTN-002.
4. **Benchmarks are the oracle.** Physics changes are validated against `benchmarks/`, not against intuition. If a benchmark's expected value changes, that requires a CHANGELOG entry explaining why.
5. **Respect the layering rule** (below). It is enforced in CI by import-linter; do not work around a failure by editing the linter config.

## Layering

```
CLI (Typer) │ Web (NiceGUI) │ Desktop (NiceGUI native)   ← adapters
─────────────────────────────────────────────────────────
              Core: visual head │ digital head            ← pure functions
              Sky model (ephemeris, extinction, moon,
                         twilight, skyglow)
─────────────────────────────────────────────────────────
              Data access layer (cache, download)         ← only layer that touches the network
```

- Core and sky-model modules must not import from any adapter, must not print, must not read or write files, and must not make network calls.
- Only the data access layer touches the network or the filesystem cache.
- Physics functions take dataclass inputs and return dataclass results. No dicts as informal structs.

## Units convention

Decided once; do not revisit.

- **Public API boundaries** use `astropy.units` quantities.
- **Internals** use plain floats with the unit in the name: `sky_mag_per_arcsec2`, `exposure_s`, `aperture_m`, `wavelength_nm`, `airmass` (dimensionless).
- Magnitudes are **V-band Johnson unless the parameter name says otherwise**. Sky brightness is always mag arcsec⁻².
- Angles are radians internally, degrees at the API boundary.

## Testing

```bash
pytest                          # full suite
pytest benchmarks/ -v           # published-value benchmarks only
pytest -k bowen                 # single benchmark
ruff check . && ruff format .   # lint + format
mypy src/                       # type check
import-linter                   # layering contract
```

- `tests/` — unit tests, fast, no network.
- `benchmarks/` — golden values from the literature, each with an explicit tolerance and a source comment. Current oracles: Bowen (1947) exit-pupil series; Krisciunas & Schaefer (1991) worked cases; Crumey (2014) worked examples (`F = 2` at µ = 21.83 → NELM 6.18; `m_cut = 5 log D + 8.45`); SMTN-002 `m5` table.
- Never loosen a benchmark tolerance to make a test pass. If the model genuinely can't hit it, say so and stop.
- No test may hit the network. ESO SkyCalc and atlas lookups are mocked with cached fixtures.

## Repo layout

```
src/liminastra/
  visual/       # Crumey, Schaefer backends; contrast threshold, field factor F
  digital/      # photon budget, Merline & Howell SNR, n_eff pixels, m5
  sky/          # ephemeris, airmass, extinction, moon, twilight, airglow, skyglow
  data/         # cache, downloads, offline fallbacks — the only networked layer
  cli/          # Typer app
  web/          # NiceGUI app
tests/
benchmarks/
docs/
```

## Conventions

- Python 3.11+, `src/` layout, `uv` for env and lockfile.
- Ruff for lint and format (line length 100). Mypy strict on `src/`, lenient on tests.
- Public functions get NumPy-style docstrings with a `References` section.
- Conventional commits. Tag releases `vX.Y.Z`.
- Sky-model backends are pluggable: `sky_model="closed_form" | "eso"`. The closed-form tier must always work fully offline.

## Scope discipline

v1.0 is **V-band, clear-sky, point sources**. Extended sources, multi-band, and cloud modelling are v2. If a request implies scope beyond that, flag it rather than quietly building it.

Known constraint: the Falchi et al. World Atlas light-pollution data may be non-commercial-licensed. Treat it as an optional user-supplied file, never bundled. Manual sky-brightness input is the always-available path.

## Working style

- Architectural decisions go in `DECISIONS.md` with a date and rationale. Before proposing a change to layering, units, model choice, or dependencies, read it — the reasoning is usually already there.
- Use plan mode for anything touching more than one module.
- Prefer failing-test-first: write the benchmark, then implement until green.
- When a paper is ambiguous, say so explicitly in the response and in a `# NOTE:` comment — do not pick an interpretation silently.
