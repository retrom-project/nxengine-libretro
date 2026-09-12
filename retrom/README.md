# Retrom browser integration

Source: [libretro/nxengine-libretro](https://github.com/libretro/nxengine-libretro), fixed at `fd1c0686f8b4c0aea9b5addbc077e3ad7da23bb7`. The fork/default branch and immutable release naming are in `retrom-fork.json`.

The Emscripten build uses the bundled software SDL implementation and libretro callbacks. `nxengine-host-v1` exposes RGBA frames, stereo signed 16-bit 22050 Hz PCM, single-step execution, and joypad masks. Each module is one independent machine. `/game/Doukutsu.exe` and the complete `data/` directory are caller supplied. `/save` is separate and holds native `profile.dat` through `profile5.dat`; game resources do not seed saved progress. No instant serialization is advertised.

Build an absolute empty output directory with `bash .github/rpg-runtime/build-candidate.sh <output>`. The pinned Emscripten Docker image runs as the invoking user and writes build/cache state under `.retrom-build`. Run source verification, `bash retrom/check.sh`, and the Python tests before building. `retrom/licenses.py` includes unchanged source notices plus engine GPL and bundled SDL LGPL text (LGPL 2.1 text from the system common-licenses distribution).

Candidate output contains a truthful dirty/source digest descriptor and must only be used in a named Retrom PFB. Formal release preparation rejects dirty sources, wrong repository, tag and commit. The release workflow requires an annotated tag contained in the maintenance branch. It is not run as part of local integration.

The host product acceptance case is `ACC-NXENGINE-001`, using separately supplied original freeware Cave Story data. Original Windows resources are consumed as data; the PE executable is never launched as a Windows program. Cave Story+, alternate engines and arbitrary mods are not implied compatible. Before any release, verify ordinary import, review preview, input, native saving, stored-byte transfer and loading in a different Launch.
