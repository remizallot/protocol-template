# Protocol template

A way to write a run protocol for any command-line tool so that the reader
sees every command in full, understands each option, can change it, and can
copy it without it breaking.

| file | what it is |
|---|---|
| `PROTOCOL_TEMPLATE.md` | the skeleton to fill in |
| `build_protocol.py` | turns the filled-in Markdown into `PROTOCOL.html` (Copy button on every command) and, with `--pdf`, `PROTOCOL.pdf`. Python standard library only |
| `README.md` | this file: how to ask for it, and the rules the protocol must follow |

## Install

Clone it anywhere. The examples below assume `~/code/protocol-template`; if
you put it somewhere else, use that path instead.

```bash
git clone https://github.com/remizallot/protocol-template ~/code/protocol-template
```

There is nothing to build or install after that:

- **Python 3** is all the builder needs (standard library only, no `pip`).
- **Chrome or Chromium** is needed only for the PDF. Without it the HTML page
  is still written and the script says the PDF was skipped.

To update later:

```bash
git -C ~/code/protocol-template pull
```

## How to ask for it

The template is written to be handed to an AI coding assistant, but a person
can follow it just as well. In a session opened on another repository, say:

> Write a run protocol for <what I want to run> following the template in
> `~/code/protocol-template/`. Read its README first and follow the rules.
> Put the result in <folder>.

## Building the pages

Run this in the folder that holds your filled-in `PROTOCOL.md`:

```bash
python3 ~/code/protocol-template/build_protocol.py PROTOCOL.md --pdf
```

This writes `PROTOCOL.html` and `PROTOCOL.pdf` beside `PROTOCOL.md`. Without
`--pdf` it writes the HTML only. The script refuses to write anything if a
command box in the page would differ from its Markdown source. The PDF needs
Chrome or Chromium installed; everything else needs only Python 3.

## Rules for whoever writes the protocol

### The commands

1. **Every command in full.** No wrapper script, no shell variables standing
   in for arguments, no "as above". If two commands differ in one option,
   both are written out. A helper script may be offered as an extra; the
   protocol must not depend on it.
2. **One command per box.** A check that follows a step is its own box. The
   only exception is a list of commands that are each one short line.
3. **One option per line**, each line but the last ending in ` \`, options
   aligned under the first one. A long comma-separated value stays on one
   line: the browser page scrolls sideways, and the Copy button takes it
   whole.
4. **Runnable as pasted.** Absolute or `$HOME`-based paths, quoted when they
   contain spaces. No placeholders left in a command the reader is meant to
   run; where a value must be the reader's own, say so in the sentence above
   the box.
5. **Checked against the tool, not written from memory.** Before a command
   goes in, confirm each option exists and means what the table says, from
   the tool's `--help` or its source. Say in the hand-over what was run and
   what was only checked by reading.

### The explanations

6. **Explain the shared part once**, in "How every command is built": the
   launcher, any mount or environment, and how paths inside the command map
   to folders on disk.
7. **An options table under every command**, three columns: the option as
   written, what it does, what you might change. The third column gives a
   concrete alternative value, or "leave" when changing it would break a
   later step, with the reason if it is not obvious.
8. **Include the useful options that were left at their default**, as rows
   starting `not set:`. These are the ones the reader will reach for when
   adjusting: thresholds, filters, thread counts, output selection.
9. **After each command, say what to expect**: roughly how long, which
   warnings are harmless (quoted as they appear), which files appear, and
   what to do if it stops.
10. **Give the reason for any choice made on the reader's behalf** (dataset,
    scope, reference, threshold) and name the alternative in one line.
11. **Say how to adjust the inputs by hand**: which files can be edited,
    added or removed, and which other file must change with them.

### The document

12. **One complete document**, start to finish, delivered at once. Not one
    step per message.
13. **Three forms, one source.** `PROTOCOL.md` is the source. `PROTOCOL.html`
    is where commands are copied from. `PROTOCOL.pdf` is for reading and
    printing only: copying multi-line commands out of a PDF breaks them, and
    the opening paragraph says so.
14. **Stay within the Markdown the builder understands**: headings, plain
    paragraphs, fenced code blocks, tables, bullet and numbered lists,
    `code`, bold, italic, links. No nested lists, no images, no HTML. A
    literal pipe inside a table cell is written `\|`.
15. **Keep study material where it belongs.** A protocol that names
    unpublished genes, organisms or results lives in the study folder, not in
    a code repository.

## Changing the look

Fonts, widths and colours are the `CSS_...` blocks near the middle of
`build_protocol.py`. `PRINT_WIDTH` at the top is the number of monospace
characters that fit across the PDF page at the print font size; change the
two together.
