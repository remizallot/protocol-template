# <What is being run>: run protocol

Prepared <date>. <One line on status or confidentiality, if any.>

Every command is written out in full, with what each option does and what
you may want to change. Run them in order, from <the folder>, in one terminal
window, and wait for each to finish before starting the next.

**Copy the commands from `PROTOCOL.html`** (open it in a browser: each box
has a Copy button) or from `PROTOCOL.md`. Copying from the PDF breaks the
long commands, so the PDF is for reading and printing.

## How every command is built

```bash
<the part every command shares> <command> <options>
```

| part | meaning |
|---|---|
| `<shared part 1>` | <what it does, and why it is there> |
| `<shared part 2>` | <for a mount or a working directory: how paths in the options relate to folders on disk> |
| `<command>` | <the list of sub-commands this protocol uses> |
| `\` at the end of a line | the command continues on the next line |
| `2>&1 \| tee file.log` | show the output on screen and keep a copy in `file.log` |

Any command's full option list: `<the help command>`.

## What is in this folder

| item | what it is |
|---|---|
| `<input folder or file>` | <what it holds, and which step reads it> |
| `<another>` | <...> |

<One short paragraph on how to adjust the inputs by hand: add, remove, rename.>

## <The main choice made for the user, and why>

<The decision this protocol takes on the reader's behalf (which dataset, which
scope, which reference), the reason, and the alternative in one line.>

## 0. Go to the folder

```bash
cd "<absolute path, quoted if it has spaces>"
```

## 1. <First step, as an action>

```bash
<full command, one option per line, each line but the last ending in \>
```

| option | what it does | what you might change |
|---|---|---|
| `<option as written above>` | <what it does, in the reader's terms> | <a concrete alternative value, or "leave"> |
| not set: `<useful option left at its default>` | <what the default is> | <when to set it, with an example value> |

<What to expect: how long, what is printed, what files appear.>

<A quick check that the step worked, as its own short command:>

```bash
<check command>
```

- <A warning that is expected and harmless, quoted as it appears.>
- <What to do if the step stops: rerun, or which option to add.>

## 2. <Next step>

```bash
<full command>
```

| option | what it does | what you might change |
|---|---|---|
| `<option>` | <...> | <...> |

<What to read in the output before going on.>

## Where the results are

| file | what to read it for |
|---|---|
| `<output file>` | <the question it answers> |

## Reading the result: things to keep in mind

1. <A known limit or trap in interpreting the output.>
2. <Another.>
