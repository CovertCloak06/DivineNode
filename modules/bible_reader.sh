#!/data/data/com.termux/files/usr/bin/bash
# Divine Node Module: Bible Reader (Verse of the Day with Audio + Parakleon Voice)

# Dependencies check
for cmd in curl jq termux-tts-speak termux-media-player termux-toast; do
    command -v $cmd >/dev/null 2>&1 || {
        echo "Missing required command: $cmd"
        termux-tts-speak "Bible Reader cannot run. Missing $cmd."
        exit 1
    }
done

# Intro voice (Parakleon)
termux-tts-speak "This is Parakleon. Let the Word of God guide your path today."

# Fetch verse
verse_json=$(curl -s "https://beta.ourmanna.com/api/v1/get/?format=json&order=daily")
verse_ref=$(echo "$verse_json" | jq -r '.verse.details.reference')
verse_text=$(echo "$verse_json" | jq -r '.verse.details.text')

# Format for audio link
normalized_ref=$(echo "$verse_ref" | sed 's/ /_/g' | sed 's/:/_/g')

# Setup file
AUDIO_DIR="$HOME/DivineNode/assets"
mkdir -p "$AUDIO_DIR"
AUDIO_FILE="$AUDIO_DIR/audio_verse.mp3"
AUDIO_URL="https://audio.bible/download/kjv/${normalized_ref}.mp3"

# Notify + download
termux-toast "Verse of the Day: $verse_ref"
curl -s --fail "$AUDIO_URL" -o "$AUDIO_FILE"

# Play audio or fallback to spoken text
if [ -s "$AUDIO_FILE" ]; then
    termux-media-player play "$AUDIO_FILE"
else
    termux-tts-speak "Audio not found for $verse_ref. Instead, here is the verse: $verse_text"
fi
