# liminastra

**Limiting magnitudes for visual observers and digital detectors.**

`liminastra` computes how faint an object has to be before it disappears — for the dark-adapted
human eye at a telescope, and for a CCD or CMOS sensor at a given exposure. Both calculations run
over the same physical sky model, so a visual estimate and an imaging estimate for the same night
share the same assumptions about airglow, moonlight, extinction, and light pollution.

```{note}
Status: pre-release. Version 0.1.x reserves the name and nothing more — there is no working API
yet. These docs will grow alongside it.
```

## Scope

Version 1.0 is deliberately narrow: V-band, clear sky, point sources.

- Naked-eye and telescopic limiting magnitude for a given observer, site, and instrument
- SNR-limited depth for a given sensor, optic, and exposure
- Sky brightness from natural components (airglow, zodiacal light, moonlight, twilight) plus
  user-supplied or atlas-derived light pollution

## References

- Crumey, A. (2014). *Human contrast threshold and astronomical visibility.* MNRAS 442, 2600.
- Schaefer, B. E. (1990). *Telescopic limiting magnitudes.* PASP 102, 212.
- Merline, W. J. & Howell, S. B. (1995). *A realistic model for point-sources imaged on array
  detectors.* Experimental Astronomy 6, 163.
- Krisciunas, K. & Schaefer, B. E. (1991). *A model of the brightness of moonlight.* PASP 103, 1033.

Source is on [GitHub](https://github.com/liminastra/liminastra).
