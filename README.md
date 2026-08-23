# liminastra

**Limiting magnitudes for visual observers and digital detectors.**

`liminastra` computes how faint an object has to be before it disappears — for the dark-adapted
human eye at a telescope, and for a CCD or CMOS sensor at a given exposure. Both calculations run
over the same physical sky model, so a visual estimate and an imaging estimate for the same night
share the same assumptions about airglow, moonlight, extinction, and light pollution.

> **Status: pre-release.** Version 0.1.x reserves the name and nothing more. There is no working
> API yet. Watch the repository if you want to know when there is.

## Why this exists

Tools for this problem are split cleanly in two, and neither half talks to the other.

Professional exposure time calculators — ESO SkyCalc, the observatory ETCs, `rubin_sim` — model
detectors and sky backgrounds carefully, but have no concept of a human observer and generally
assume a dark professional site rather than a suburban backyard.

Amateur visual calculators do model the eye, but nearly all of them descend from Schaefer (1990),
which rests on Hecht's 1947 point-source threshold formula. That formula has the wrong curvature in
the scotopic regime where faint-star detection actually happens: it accelerates where the
laboratory data compress. Against Bowen's 1947 exit-pupil series, Crumey (2014) gives roughly
0.09 mag RMS where Schaefer gives 0.37.

`liminastra` uses Crumey (2014) as its primary visual model, implements the digital case from the
standard Merline & Howell (1995) SNR formalism, and runs both against a shared sky model — offline,
on a laptop, without a multi-gigabyte data download.

## Planned scope

Version 1.0 is deliberately narrow: **V-band, clear sky, point sources.**

- Naked-eye and telescopic limiting magnitude for a given observer, site, and instrument
- SNR-limited depth for a given sensor, optic, and exposure
- Sky brightness from natural components (airglow, zodiacal light, moonlight, twilight) plus
  user-supplied or atlas-derived light pollution
- A Python API, a command-line interface, and a browser and desktop application over the same
  library

Extended sources, multi-band work, and cloud modelling are explicitly out of scope for 1.0.

## Primary references

- Crumey, A. (2014). *Human contrast threshold and astronomical visibility.* MNRAS 442, 2600.
- Schaefer, B. E. (1990). *Telescopic limiting magnitudes.* PASP 102, 212.
- Merline, W. J. & Howell, S. B. (1995). *A realistic model for point-sources imaged on array
  detectors.* Experimental Astronomy 6, 163.
- Krisciunas, K. & Schaefer, B. E. (1991). *A model of the brightness of moonlight.* PASP 103, 1033.
- Leinert, C. et al. (1998). *The 1997 reference of diffuse night sky brightness.* A&AS 127, 1.

Every physics function in the codebase cites its source and equation number. Results are validated
against published values from these papers rather than against expectation.

## Contributing

Not yet — there is nothing to contribute to. Once the core library exists, the architecture is
designed so that a contributor can work on one model (the visual head, the moonlight component,
a detector noise term) without touching anything else. Issues and discussion are open in the
meantime if you have relevant expertise or a use case you want represented.

## License

BSD-3-Clause.
