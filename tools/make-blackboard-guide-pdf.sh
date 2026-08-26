#!/usr/bin/env bash
# Regenerate BLACKBOARD_GUIDE.pdf from BLACKBOARD_GUIDE.md.
#
# The PDF is a distributable convenience copy for instructional designers who do not
# work in the repo. It is gitignored — the markdown is the source of truth.
#
# Requires: pandoc and a LaTeX install providing pdflatex (texlive-latex-recommended
# and texlive-latex-extra cover the packages used below).
set -euo pipefail
cd "$(dirname "$0")/.."

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

# Long URLs inside table cells overflow the page as \texttt{}; render them as
# breakable \url{} instead.
cat > "$tmp/urlbreak.lua" <<'LUA'
function Code(el)
  if el.text:match("^https?://") then
    return pandoc.RawInline("latex", "{\\small\\url{" .. el.text .. "}}")
  end
end
LUA

cat > "$tmp/header.tex" <<'TEX'
\usepackage[htt]{hyphenat}
\usepackage{ragged2e}
\usepackage{xurl}
\sloppy
\emergencystretch=3em
\let\oldtexttt\texttt
\renewcommand{\texttt}[1]{{\small\oldtexttt{#1}}}
\usepackage{etoolbox}
\AtBeginEnvironment{longtable}{\footnotesize\RaggedRight}
TEX

pandoc BLACKBOARD_GUIDE.md \
  -o BLACKBOARD_GUIDE.pdf \
  --pdf-engine=pdflatex \
  --toc --toc-depth=2 \
  -V geometry:margin=1in \
  -V colorlinks=true -V linkcolor=teal -V urlcolor=teal -V toccolor=black \
  -V fontsize=11pt \
  -L "$tmp/urlbreak.lua" \
  -H "$tmp/header.tex"

echo "Wrote BLACKBOARD_GUIDE.pdf"
