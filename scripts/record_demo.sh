#!/bin/sh
set -eu
BASE=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
cd "$BASE"
mkdir -p .artifacts
DISPLAY_ID=:195
OUT="${1:-$BASE/.artifacts/handoff-check-demo.mp4}"
Xvfb "$DISPLAY_ID" -screen 0 1280x720x24 -nolisten tcp >.artifacts/xvfb.log 2>&1 &
XPID=$!
DPID=
cleanup() {
  [ -z "$DPID" ] || kill "$DPID" 2>/dev/null || true
  kill "$XPID" 2>/dev/null || true
  wait "$XPID" 2>/dev/null || true
}
trap cleanup EXIT INT TERM
sleep 2
DISPLAY="$DISPLAY_ID" python3 scripts/demo_screen.py &
DPID=$!
ffmpeg -nostdin -y -hide_banner -loglevel error -f x11grab -framerate 15 -video_size 1280x720 \
-i "$DISPLAY_ID" -t 98 -c:v libx264 -preset veryfast -crf 24 -pix_fmt yuv420p -movflags +faststart "$OUT"
wait "$DPID" || true
printf 'Local video: %s\n' "$OUT"
ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1 "$OUT"
