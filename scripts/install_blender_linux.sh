#!/usr/bin/env bash
# Install a matching, checksum-verified portable Blender without root access.
set -euo pipefail
version="${1:-5.2.1}"
series="${version%.*}"
install_root="${BLENDER_INSTALL_ROOT:-$HOME/.local/opt}"
download_dir="$install_root/blender-downloads"
archive="blender-$version-linux-x64.tar.xz"
mkdir -p "$download_dir"
cd "$download_dir"
curl --fail --location --retry 3 --output "$archive" "https://mirror.blender.org/release/Blender$series/$archive"
curl --fail --location --retry 3 --output "blender-$version.sha256" "https://mirror.blender.org/release/Blender$series/blender-$version.sha256"
awk -v archive="$archive" '$2 == archive { print }' "blender-$version.sha256" | sha256sum --check --strict -
tar -xf "$archive" -C "$install_root"
"$install_root/blender-$version-linux-x64/blender" --version
