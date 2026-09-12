#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
mkdir -p .retrom-build
gcc -Wall -Wextra -Werror -fsanitize=address,undefined -I nxengine/libretro/libretro-common/include \
  retrom/test_bridge.c -o .retrom-build/test-bridge
.retrom-build/test-bridge
