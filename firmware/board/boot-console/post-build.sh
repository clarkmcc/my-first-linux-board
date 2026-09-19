#!/bin/sh
set -eu

target_dir=$1
metrics=$target_dir/www/cgi-bin/metrics

# Buildroot overlays add and replace files but do not remove files left by an
# earlier build. Keep the generated web root faithful to the one-endpoint
# contract even when an existing output directory is reused.
if [ -d "$target_dir/www" ]; then
	find "$target_dir/www" -type f ! -path "$metrics" -delete
fi

test -x "$metrics"
