# Markdown Rules (markdownlint-compliant)

These rules apply to **every** `.md` file generated in this project.
They are derived from the [openHAB markdownlint configuration](https://github.com/openhab/openhab-docs/blob/main/.github/.markdownlint.yaml)
and must be followed without exception.

---

## MD004 — Unordered list style: dash

Always use `-` for unordered list items. Never use `*` or `+`.

**Wrong:**

```markdown
* item one
+ item two
```

**Correct:**

```markdown
- item one
- item two
```

---

## MD013 — Line length: disabled

No line length limit. Long lines are allowed.

---

## MD022 — Blank lines around headings

Every heading (`#`, `##`, `###`, etc.) must be preceded **and** followed by exactly one blank line.

**Wrong:**

```markdown
Some text.
### My Heading
- item one
```

**Correct:**

```markdown
Some text.

### My Heading

- item one
```

---

## MD024 — Duplicate headings: siblings only

Duplicate heading text is allowed only between headings at different nesting levels (siblings).
Two headings with identical text at the same nesting level within the same parent section are not allowed.

---

## MD025 — Multiple top-level headings: allowed

A document may have more than one `# H1` heading.

---

## MD026 — Trailing punctuation in headings: allowed

Headings may end with punctuation (e.g., a colon or question mark).

---

## MD029 — Ordered list item prefix (Style: one)

All items in a numbered list must use `1.` as the prefix. Never use `2.`, `3.`, etc.
The renderer increments numbers automatically.

**Wrong:**

```markdown
1. First
2. Second
3. Third
```

**Correct:**

```markdown
1. First
1. Second
1. Third
```

---

## MD032 — Blank lines around lists

Every list (bullet or numbered) must be preceded **and** followed by exactly one blank line.

**Wrong:**

```markdown
Some text.
- item one
- item two
More text.
```

**Correct:**

```markdown
Some text.

- item one
- item two

More text.
```

---

## MD033 — Inline HTML: allowed

Inline HTML elements are permitted where needed.

---

## MD040 — Fenced code blocks must declare a language

Every fenced code block must specify a language identifier immediately after the opening fence.
Use `text` if no specific language applies. Never leave it blank.

**Wrong:**

````markdown
```
some code here
```
````

**Correct:**

````markdown
```java
public class Foo {}
```
````

Common identifiers: `java`, `xml`, `json`, `yaml`, `shell`, `text`, `markdown`, `properties`.

---

## MD046 — Code block style: fenced

Always use fenced code blocks (` ``` `). Never use indented code blocks (4-space indent).

**Wrong:**

```markdown
    public class Foo {}
```

**Correct:**

````markdown
```java
public class Foo {}
```
````

---

## MD049 — Emphasis style: underscore

Use `_text_` for italic/emphasis. Never use `*text*`.

**Wrong:**

```markdown
This is *important*.
```

**Correct:**

```markdown
This is _important_.
```

---

## MD050 — Strong style: asterisk

Use `**text**` for bold/strong. Never use `__text__`.

**Wrong:**

```markdown
This is __critical__.
```

**Correct:**

```markdown
This is **critical**.
```

---

## MD060 — Disabled

No restriction from this rule.

---

## Summary Checklist

Before finalizing any `.md` file, verify:

- [ ] Unordered lists use `-` (not `*` or `+`)
- [ ] Every heading has a blank line above and below it
- [ ] Every list has a blank line above and below it
- [ ] All numbered lists use `1.` for every item
- [ ] Every fenced code block has a language identifier
- [ ] Code blocks use fenced style, not 4-space indent
- [ ] Emphasis uses `_underscores_`
- [ ] Bold uses `**asterisks**`
