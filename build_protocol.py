#!/usr/bin/env python3
"""Turn a protocol written in Markdown into a browser page with Copy buttons.

    python3 build_protocol.py PROTOCOL.md          writes PROTOCOL.html beside it
    python3 build_protocol.py PROTOCOL.md --pdf    also writes PROTOCOL.pdf (needs Chrome)

Standard library only. The Markdown it understands is deliberately small:
headings (#, ##, ###), paragraphs, fenced code blocks, tables, bullet and
numbered lists, `code`, **bold**, *italic*, [text](url). Inside a table cell
write a literal pipe as \\| .

The HTML is the copy source: the text of every command box is exactly the
text of the fenced block in the Markdown. The PDF is for reading: lines too
long for the page are broken at a comma with a trailing backslash.
"""
import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

PRINT_WIDTH = 92          # characters of monospace that fit an A4 page
PIPE = "\x00"
CHROME = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "google-chrome", "chromium", "chromium-browser",
]


def inline(text):
    t = html.escape(text, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<![\w*])\*([^*]+)\*(?![\w*])", r"<i>\1</i>", t)
    return t.replace(PIPE, "|")


def wrap_for_print(line):
    out = []
    while len(line) > PRINT_WIDTH:
        cut = line.rfind(",", 0, PRINT_WIDTH - 1)
        if cut <= 0:
            break
        out.append(line[:cut + 1] + "\\")
        line = line[cut + 1:]
    out.append(line)
    return out


BLOCK_START = re.compile(r"^(#|```|\||- |\d+\. )")
LIST_ITEM = re.compile(r"^(- |\d+\. )")


def convert(markdown, mode):
    """Return (title, body_html). mode is 'screen' or 'print'."""
    lines = markdown.splitlines()
    body, title, i, n = [], "Protocol", 0, len(lines)
    while i < n:
        line = lines[i]
        if line.startswith("```"):
            i += 1
            code = []
            while i < n and not lines[i].startswith("```"):
                code.extend(wrap_for_print(lines[i]) if mode == "print" else [lines[i]])
                i += 1
            i += 1
            button = "<button class='copy'>Copy</button>" if mode == "screen" else ""
            body.append("<div class='cmd'>" + button + "<pre>"
                        + html.escape("\n".join(code), quote=False) + "</pre></div>")
        elif line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            text = line[level:].strip()
            if level == 1 and title == "Protocol":
                title = re.sub(r"[`*]", "", text)
            body.append(f"<h{level}>{inline(text)}</h{level}>")
            i += 1
        elif line.startswith("|"):
            rows = []
            while i < n and lines[i].startswith("|"):
                cells = lines[i].replace("\\|", PIPE).strip().strip("|").split("|")
                rows.append([c.strip() for c in cells])
                i += 1
            head = "".join(f"<th>{inline(c)}</th>" for c in rows[0])
            rest = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>"
                           for r in rows[2:])
            body.append(f"<table><thead><tr>{head}</tr></thead><tbody>{rest}</tbody></table>")
        elif LIST_ITEM.match(line):
            tag = "ul" if line.startswith("- ") else "ol"
            items = []
            while i < n and (LIST_ITEM.match(lines[i]) or lines[i].startswith("  ")):
                if LIST_ITEM.match(lines[i]):
                    items.append(LIST_ITEM.sub("", lines[i], count=1))
                else:
                    items[-1] += " " + lines[i].strip()
                i += 1
            body.append(f"<{tag}>" + "".join(f"<li>{inline(x)}</li>" for x in items)
                        + f"</{tag}>")
        elif not line.strip():
            i += 1
        else:
            para = []
            while i < n and lines[i].strip() and not BLOCK_START.match(lines[i]):
                para.append(lines[i].strip())
                i += 1
            body.append("<p>" + inline(" ".join(para)) + "</p>")
    return title, "\n".join(body)


CSS_COMMON = """
body { font: 10.5pt/1.45 "Helvetica Neue", Helvetica, Arial, sans-serif; color: #111; }
h1 { font-size: 20pt; margin: 0 0 4pt; }
h2 { font-size: 13.5pt; margin: 18pt 0 5pt; padding-top: 6pt; border-top: 0.6pt solid #999;
     break-after: avoid; }
h3 { font-size: 11.5pt; margin: 12pt 0 4pt; break-after: avoid; }
p { margin: 5pt 0; }
ul, ol { margin: 4pt 0 6pt; padding-left: 16pt; }
li { margin: 2pt 0; }
a { color: #1e50a0; }
code { font: 0.86em Menlo, Monaco, Consolas, monospace; background: #f1f1f1; padding: 0 2pt; }
.cmd { position: relative; margin: 6pt 0 9pt; break-inside: avoid; }
pre { background: #f4f4f4; border: 0.5pt solid #bbb; border-left: 2.5pt solid #555;
      padding: 7pt 8pt; margin: 0; white-space: pre; }
table { border-collapse: collapse; width: 100%; margin: 6pt 0 9pt; font-size: 0.9em; }
tr { break-inside: avoid; }
th, td { border: 0.5pt solid #aaa; padding: 3pt 5pt; text-align: left; vertical-align: top; }
th { background: #eee; }
td:first-child { width: 30%; }
"""
CSS_PRINT = """
@page { size: A4; margin: 18mm 15mm 18mm 15mm; }
pre { font: 7.7pt/1.4 Menlo, Monaco, Consolas, monospace; overflow: hidden; }
"""
CSS_SCREEN = """
body { max-width: 980px; margin: 28px auto; padding: 0 22px; font-size: 15px; }
pre { font: 13px/1.5 Menlo, Monaco, Consolas, monospace; overflow-x: auto; padding-right: 70px; }
button.copy { position: absolute; top: 6px; right: 6px; font: 12px Helvetica, Arial, sans-serif;
              padding: 3px 10px; border: 1px solid #777; border-radius: 4px; background: #fff;
              color: #111; cursor: pointer; }
button.copy:hover { background: #e6e6e6; }
button.copy.done { background: #2e7d32; color: #fff; border-color: #2e7d32; }
@media print { button.copy { display: none; } }
"""
SCRIPT = """
<script>
document.querySelectorAll('button.copy').forEach(function (b) {
  b.addEventListener('click', function () {
    var text = b.parentNode.querySelector('pre').textContent;
    function ok() { b.textContent = 'Copied'; b.classList.add('done');
      setTimeout(function () { b.textContent = 'Copy'; b.classList.remove('done'); }, 1500); }
    function fallback() {
      var t = document.createElement('textarea'); t.value = text;
      t.style.position = 'fixed'; t.style.opacity = '0';
      document.body.appendChild(t); t.select(); document.execCommand('copy');
      document.body.removeChild(t); ok(); }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(ok, fallback);
    } else { fallback(); }
  });
});
</script>
"""


def page(markdown, mode):
    title, body = convert(markdown, mode)
    css = CSS_COMMON + (CSS_PRINT if mode == "print" else CSS_SCREEN)
    return ("<!doctype html><html lang='en'><head><meta charset='utf-8'>"
            f"<title>{html.escape(title)}</title><style>{css}</style></head><body>\n"
            + body + (SCRIPT if mode == "screen" else "") + "\n</body></html>\n")


def check_roundtrip(markdown, screen_html):
    """The commands in the page must be exactly the commands in the Markdown."""
    blocks, lines, i = [], markdown.splitlines(), 0
    while i < len(lines):
        if lines[i].startswith("```"):
            j = i + 1
            while j < len(lines) and not lines[j].startswith("```"):
                j += 1
            blocks.append("\n".join(lines[i + 1:j]))
            i = j
        i += 1
    shown = [html.unescape(x) for x in re.findall(r"<pre>(.*?)</pre>", screen_html, re.S)]
    if blocks != shown:
        sys.exit("ERROR: a command box differs from its Markdown source; nothing written.")
    return len(blocks)


def write_pdf(markdown, pdf_path):
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "print.html"
        src.write_text(page(markdown, "print"), encoding="utf-8")
        for chrome in CHROME:
            try:
                subprocess.run(
                    [chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                     f"--user-data-dir={tmp}/profile", f"--print-to-pdf={pdf_path}",
                     src.as_uri()],
                    check=True, capture_output=True, timeout=120)
                return True
            except (FileNotFoundError, subprocess.SubprocessError):
                continue
    return False


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        sys.exit(__doc__)
    source = Path(args[0])
    markdown = source.read_text(encoding="utf-8")
    screen = page(markdown, "screen")
    count = check_roundtrip(markdown, screen)
    out = source.with_suffix(".html")
    out.write_text(screen, encoding="utf-8")
    print(f"{out}: {count} command boxes, each identical to its Markdown source")
    if "--pdf" in sys.argv:
        pdf = source.with_suffix(".pdf")
        if write_pdf(markdown, pdf):
            print(f"{pdf}: written (for reading; copy commands from the HTML)")
        else:
            print("PDF not written: no Chrome or Chromium found, or it could not start.")


if __name__ == "__main__":
    main()
