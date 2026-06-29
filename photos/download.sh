#!/bin/bash
# Usage: ./download.sh <photo_filename> [output_path]
PHOTO="$1"
OUT="${2:-/root/.openclaw-instagram/workspace/photos/$1}"
curl -s -u admin:seamless_nc_2026 \
  "http://localhost:8080/remote.php/dav/files/admin/%D1%84%D0%BE%D1%82%D0%BE_%D1%81_%D1%81%D0%B8%D0%BC%D0%BB%D0%B5%D1%81%D1%81/Selected/$PHOTO" \
  -o "$OUT" && echo "Downloaded: $OUT"
