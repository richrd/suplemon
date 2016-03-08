#!/usr/bin/env bash
# Exit on first error
set -e

# Parse our CLI arguments
version="$1"
if test "$version" = ""; then
  echo "Expected a version to be provided to \`release.sh\` but none was provided." 1>&2
  echo "Usage: $0 [version] # (e.g. $0 1.0.0)" 1>&2
  exit 1
fi

# Bump the version via regexp
sed -E "s/^(__version__ = \")[0-9]+\.[0-9]+\.[0-9]+(\")$/\1$version\2/" suplemon/main.py --in-place

# Verify our version made it into the file
if ! grep "$version" suplemon/main.py &> /dev/null; then
  echo "Expected \`__version__\` to update via \`sed\` but it didn't" 1>&2
  exit 1
fi

# Commit the change
git add suplemon/main.py
git commit -a -m "Release $version"

# Tag the release
git tag "$version"

# Publish the release to GitHub
git push
git push --tags

# Publish the release to PyPI
python setup.py sdist --formats=gztar,zip upload
