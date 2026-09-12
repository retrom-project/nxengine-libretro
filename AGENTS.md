# NXEngine Retrom fork

Read `retrom-fork.json` and `retrom/README.md` before changes. `master` is an upstream fast-forward mirror only. Retrom changes belong to the default `retrom/<baseline>` branch, with feature work on `feat/*`, `fix/*`, or `build/*`. Never move existing tags. Releases require explicit authorization and passing the actual Retrom product case; a candidate build is not release evidence.

Keep core source/build/ABI changes here, host-independent browser lifecycle in retrom-runtime, and import/approval/storage in Retrom. Do not add game assets or proprietary executables. Preserve upstream copyright and include GPL, bundled SDL LGPL and source notices in every candidate/release.

Run `python3 .github/rpg-runtime/verify-source.py`, `bash retrom/check.sh`, `python3 -m unittest discover -s retrom/tests`, then the fixed-toolchain candidate build. Test native save restore through a different Retrom Launch. This core declares GAME_SAVE, not instant serialization.
