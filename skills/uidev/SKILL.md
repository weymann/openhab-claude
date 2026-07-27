---
name: UIDev
description: >
  Expert authoring of openHAB Main UI widget YAML files (.yaml) for the Framework7/Vue 3
  based UI. Use this skill whenever the user wants to create, edit, debug, or extend an
  openHAB UI widget — including donut rings, SVG graphics, power overlays, oh-repeater
  with JSONPath, dynamic innerHTML, or any component that uses JEXL expressions. Also
  trigger when the user asks about why a widget expression fails, how to render a chart
  or arc in openHAB, or how to display item states in the Main UI.
---

# openHAB UI Widget YAML Designer

You are an expert openHAB F7 UI widget author. Your output is valid `.yaml` that can be
pasted directly into the openHAB Main UI widget editor without errors.

The most important thing to understand: the widget editor evaluates every value that
starts with `=` as a **JEXL expression** — a restricted expression language, not
JavaScript. Many patterns that look natural (ternary operators, `new Date()`, variables)
are either parse errors or silently wrong. Every constraint below was learned from real
failures.

---

## Widget File Skeleton

```yaml
uid: MyWidgetId            # PascalCase, no spaces
tags: []
props:
  parameters:
    - name: myProp
      label: Human Label
      description: "Double-quoted single-line string — never block scalars"
      type: TEXT            # TEXT | INTEGER | DECIMAL | BOOLEAN
      required: false
      context: item         # omit for non-item props
      default: someValue
  parameterGroups: []
component: f7-card
config:
  stylesheet: |
    .my-widget { ... }
  style:
    --f7-card-bg-color: "transparent"
  class: my-widget
slots:
  default:
    - component: f7-row
      ...
```

---

## JEXL Expression Rules — the Sharp Edges

### Forbidden constructs

These cause parse errors in the widget editor. Never use them.

| Forbidden | Failure reason | Safe replacement |
|-----------|---------------|-----------------|
| `new Date()` | `new` is an unknown node type | `dayjs()` |
| `new Date().getHours()` | same | `dayjs().hour()` |
| `var x = ...` | `var` forbidden | inline all arithmetic |
| `let x = ...` | `let` forbidden | inline all arithmetic |
| `function(){ ... }` | `function` forbidden | inline all arithmetic |
| `{ key: value }` object literal | forbidden | not possible in JEXL |
| `now.hour` | `now` exists only in openHAB Rules, not UI widgets | `dayjs().hour()` |
| Multi-line `=` expressions via `>-` block scalar | YAML parses as plain string, strips leading `=` | keep `=` expressions single-line |

### The ternary / YAML trap

**Never write a ternary as a bare YAML compact mapping value.** YAML treats `?` as a
mapping key character, which silently breaks the entire widget.

```yaml
# ❌ BREAKS — YAML interprets ? as a mapping key
style:
  display: =props.x ? "flex" : "none"

# ✅ SAFE — ternary inside an innerHTML string is fine because the whole
#           value is one quoted scalar; the ? is inside JS string context
innerHTML: ='<g opacity="' + (x > 0 ? "1" : "0") + '"></g>'
```

### Conditional patterns without ternary

Because you cannot use ternary in mapping values, use arithmetic:

```jexl
# Binary flag: 1 when x >= threshold, 0 when x < threshold
Math.floor(x / (threshold + 0.001))

# Complement
1 - Math.floor(x / (threshold + 0.001))

# Clamp a value to [0, 1]
Math.min(1, Math.max(0, value))

# SVG largeArcFlag: 1 when arc spans more than 180°
# (dayMinutes = sunsetMinutes - sunriseMinutes)
Math.floor(dayMinutes / 721)

# isSunUp: 1 during day, 0 at night
# sr = sunriseMinutes, ss = sunsetMinutes, nm = nowMinutes
Math.min(1, Math.max(0, Math.ceil((ss - sr - (nm - sr + 1440) % 1440) / 1440)))

# Moon phase toggle (0=left sweep, 1=right sweep)
Math.floor(1 - Math.floor(phase * 2) % 2)
```

### Available globals

```jexl
# Time
dayjs()                      # current moment as Day.js object
dayjs().hour()               # 0–23
dayjs().minute()             # 0–59
dayjs().format("HH:mm")
dayjs().format("ddd, MMM D")
dayjs().valueOf()            # Unix ms timestamp

# Math
Math.PI  Math.floor(x)  Math.ceil(x)  Math.round(x)
Math.min(a,b)  Math.max(a,b)  Math.abs(x)
Math.cos(x)  Math.sin(x)

# Data
items["ItemName"].state
items["ItemName"].displayState
props.propName
loop.varName                 # inside oh-repeater
JSON.parse(str)
```

---

## Dynamic SVG via innerHTML

The most powerful pattern for complex graphics: render an entire SVG as a single
`innerHTML` expression on a `div`. All computation is inlined — no separate components
needed for positioning.

```yaml
- component: div
  config:
    style:
      width: "100%"
    innerHTML: ='<svg viewBox="0 0 260 260" xmlns="http://www.w3.org/2000/svg">'
      + '<circle cx="130" cy="130" r="100" fill="none" stroke="#1a3548" stroke-width="28"/>'
      + '<text x="130" y="130" text-anchor="middle" fill="white" font-size="14">'
      + dayjs().format("HH:mm") + '</text>'
      + '</svg>'
```

**innerHTML rules:**

- Must be a single YAML scalar — no `>-` multiline block scalars
- All conditional logic must be arithmetic (no ternary in mapping values, but ternary
  inside the string literal is fine because the `?` is not at YAML mapping level)
- Use `<text>` SVG elements for labels — they live inside the SVG coordinate space
- Use `<g opacity="...">` with a 0/1 arithmetic expression to show/hide SVG groups

### Why CSS absolute positioning fails for SVG overlays

Vue wraps every component in its own `div`. When you try to position a `Label` or
`oh-label` absolutely on top of a SVG sibling, Vue's wrapper div breaks the stacking
context. **Anything that must appear inside or over the SVG must live inside the
`innerHTML` string.**

| Pattern | Works? | Notes |
|---------|--------|-------|
| `<text>` inside `innerHTML` | ✅ | Best for static labels, time, date |
| `<g opacity="0 or 1">` inside `innerHTML` | ✅ | Conditional SVG elements |
| CSS `position: absolute` div on top of SVG | ❌ | Vue wrapper breaks it |
| `oh-label` overlaid on SVG via absolute CSS | ❌ | Renders outside the SVG |

For live item values in the ring centre (e.g. power numbers), place them in a CSS
overlay div that is a **sibling inside the same parent** as the SVG div, using
`position: absolute` on the overlay and `position: relative` on the parent. This works
because both elements share the same Vue-rendered parent div — you're not crossing a
component boundary.

---

## SVG Donut Ring — Sol App Geometry

```text
viewBox: 0 0 260 260
Centre: cx=130, cy=130   Ring radius: 100   Stroke-width: 28

Clock orientation (noon at top):
  angle(m) = m/1440 * 2*PI + PI/2
  m=0   midnight → angle=PI/2  → bottom  (cos=0, sin=1)
  m=360 06:00    → angle=PI    → left    (cos=-1, sin=0)
  m=720 noon     → angle=3PI/2 → top     (cos=0, sin=-1)  ✓
  m=1080 18:00   → angle=2PI   → right   (cos=1, sin=0)

Point on ring (10× rounding for clean SVG):
  x = Math.round((130 + 100 * Math.cos(m/1440*2*Math.PI + Math.PI/2)) * 10) / 10
  y = Math.round((130 + 100 * Math.sin(m/1440*2*Math.PI + Math.PI/2)) * 10) / 10

Arc path (sweep-flag=1 = clockwise):
  M x1 y1 A 100 100 0 {largeArcFlag} 1 x2 y2
  largeArcFlag = Math.floor(arcDurationMinutes / 721)
```

**Twilight gradient effect:** render a short 30-minute arc in a transition colour just
before/after the main day arc to soften the sunrise/sunset edges.

---

## Moon Phase

```jexl
# Reference new moon: 2000-01-06 18:14 UTC = 947182440000 ms
# Synodic month: 29.53059 days
# phase: 0.0=New  0.25=First Quarter  0.5=Full  0.75=Last Quarter

phase = (dayjs().valueOf() - 947182440000) / 86400000 % 29.53059 / 29.53059
```

Accuracy: ±1 day — sufficient for UI display.

Moon dot via two SVG paths (no ternary needed):

```text
1. Dark base circle:
   <circle cx="X" cy="Y" r="12" fill="#0a1520"/>

2. White illuminated face:
   Path with two arc commands:
   — Outer semicircle: sweep = Math.floor(1 - Math.floor(phase*2)%2)
   — Terminator ellipse: rx = Math.abs(Math.round(Math.cos(phase*2*Math.PI)*r*10)/10)
                          sweep = Math.floor(Math.max(0, Math.cos(phase*2*Math.PI)))
```

---

## Component Reference

### oh-label

Shows an item's `displayState`. Always use `=props.propName` — never hardcode item names.

```yaml
- component: oh-label
  config:
    item: =props.myItem
    class: my-value-class
```

### oh-repeater with JSONPath

Extract values from a JSON String item:

```yaml
- component: oh-repeater
  config:
    for: e
    sourceType: jsonpath
    sourceItem: =props.timelineItem
    sourceExpression: "$.entries[?(@.title=='Sunrise'&&@.subtitle=='Event')].time"
    limit: 1
  slots:
    default:
      - component: Label
        config:
          text: =loop.e
```

JSONPath filter strings: use single quotes inside the double-quoted YAML string —
`"$.entries[?(@.key=='value')]"`. Do not mix quote types.

### oh-icon

```yaml
- component: oh-icon
  config:
    icon: "iconify:solar:panel-bold"
    width: 22
    style:
      color: "#F5A623"
```

### stylesheet scoping

```yaml
config:
  stylesheet: |
    .my-widget {
      background: #0d1b2a;
      border-radius: 20px;
    }
    .my-widget .inner-class { color: white; }
  class: my-widget
```

Scope all CSS under the root class to avoid bleeding into other widgets on the same page.

---

## Props — description Field

```yaml
# ✅ Correct
description: "String item linked to the plan#timeline channel"

# ❌ Fails — block scalar with special characters
description: >
  String item linked to plan#timeline.
```

Always double-quoted single-line strings for `description`. Block scalars break when the
text contains `#`, `:`, or other YAML special characters.

---

## Pre-Save Checklist

Before pasting a widget into the openHAB editor:

- [ ] No `new Date()` — use `dayjs()`
- [ ] No `function`, `var`, `let` in any `=` expression
- [ ] No ternary `? x : y` as a bare YAML compact mapping value
- [ ] All `description:` fields are double-quoted single-line strings
- [ ] No `>` or `>-` block scalars that contain YAML special chars or `=` expressions
- [ ] `innerHTML:` is a single-line scalar (no YAML multiline)
- [ ] CSS absolute positioning is not used to overlay dynamic labels on top of a SVG
      from a sibling component — put those labels inside the SVG `innerHTML` or in an
      absolutely-positioned div inside the same parent wrapper
- [ ] Item references in `oh-label` and `oh-repeater` use `=props.propName`
- [ ] `oh-repeater` JSONPath filter strings use single quotes inside the double-quoted
      YAML string
- [ ] Don't change text color — it will break light/dark mode design pattern
