# Journal Design System

> **Status:** This document is the visual and interaction specification for the
> journal screens implemented by #14-#23. It is a specification only. This issue
> does not add Vue components, CSS files, routes, dependencies, or scaffold
> changes.

For product scope read [`_docs/plan.md`](plan.md), for workflow and roles read
[`_docs/process.md`](process.md), for agent commands and rules read
[`_docs/AGENTS.md`](AGENTS.md), and for test layers and conventions read
[`_docs/testing-guidelines.md`](testing-guidelines.md). Those documents remain
the source of truth for product scope, workflow, and testing. This document
adds the shared visual and interaction contract that #14-#23 apply.

The target implementation is plain CSS custom properties and semantic HTML.
Do not add a UI component library, CSS framework, icon library, or other
dependency.

## Contents

1. [Design tokens](#design-tokens)
2. [Typography](#typography)
3. [Spacing and layout](#spacing-and-layout)
4. [Color and contrast](#color-and-contrast)
5. [Buttons](#buttons)
6. [Links and navigation actions](#links-and-navigation-actions)
7. [Forms](#forms)
8. [Validation and copy](#validation-and-copy)
9. [Status badges](#status-badges)
10. [Empty states](#empty-states)
11. [Loading states](#loading-states)
12. [Error states](#error-states)
13. [Destructive confirmation](#destructive-confirmation)
14. [Accessibility](#accessibility)
15. [Responsive rules](#responsive-rules)
16. [Consistency rules](#consistency-rules)
17. [Implementation map](#implementation-map)
18. [Out of scope and change control](#out-of-scope-and-change-control)

## Design tokens

Define the following tokens once at the application root, normally on `:root`.
Components consume tokens instead of repeating literal values.

```css
:root {
  /* Typography */
  --font-sans: system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  --font-mono: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace;
  --font-size-xs: 0.75rem;
  --line-height-xs: 1rem;
  --font-size-sm: 0.875rem;
  --line-height-sm: 1.25rem;
  --font-size-base: 1rem;
  --line-height-base: 1.5rem;
  --font-size-lg: 1.125rem;
  --line-height-lg: 1.75rem;
  --font-size-xl: 1.5rem;
  --line-height-xl: 2rem;
  --font-size-2xl: 2rem;
  --line-height-2xl: 2.5rem;
  --font-weight-regular: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;

  /* Spacing, shape, and layout */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-5: 1.25rem;
  --space-6: 1.5rem;
  --space-8: 2rem;
  --space-10: 2.5rem;
  --space-12: 3rem;
  --space-16: 4rem;
  --radius-sm: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
  --radius-full: 9999px;
  --shadow-sm: 0 1px 2px rgba(15, 23, 42, 0.08);
  --shadow-md: 0 4px 12px rgba(15, 23, 42, 0.12);
  --layout-max: 72rem;
  --reading-max: 42rem;
  --page-gutter: clamp(1rem, 4vw, 2rem);
  --focus-ring-width: 2px;
  --focus-ring-offset: 2px;

  /* Breakpoint aliases for documentation only. */
  --breakpoint-sm: 40rem;
  --breakpoint-md: 48rem;
  --breakpoint-lg: 64rem;

  /* Color */
  --color-bg: #f8fafc;
  --color-surface: #ffffff;
  --color-surface-muted: #f1f5f9;
  --color-border: #cbd5e1;
  --color-border-strong: #94a3b8;
  --color-text: #0f172a;
  --color-text-muted: #475569;
  --color-primary: #1d4ed8;
  --color-primary-hover: #1e40af;
  --color-primary-active: #1e3a8a;
  --color-primary-soft: #eff6ff;
  --color-danger: #b91c1c;
  --color-danger-hover: #991b1b;
  --color-danger-active: #7f1d1d;
  --color-danger-soft: #fef2f2;
  --color-success: #166534;
  --color-success-soft: #dcfce7;
  --color-warning: #b45309;
  --color-warning-soft: #fffbeb;
  --color-focus: #2563eb;
  --color-on-primary: #ffffff;

  /* Status badges */
  --badge-planned-bg: #e2e8f0;
  --badge-planned-text: #334155;
  --badge-planned-border: #cbd5e1;
  --badge-progress-bg: #dbeafe;
  --badge-progress-text: #1e3a8a;
  --badge-progress-border: #93c5fd;
  --badge-finished-bg: #dcfce7;
  --badge-finished-text: #14532d;
  --badge-finished-border: #86efac;
  --badge-dropped-bg: #fee2e2;
  --badge-dropped-text: #7f1d1d;
  --badge-dropped-border: #fca5a5;
  --badge-neutral-bg: var(--color-surface-muted);
  --badge-neutral-text: var(--color-text-muted);
  --badge-neutral-border: var(--color-border);
}
```

### Typography tokens

| Token | Value | Use |
| --- | --- | --- |
| `--font-sans` | `system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif` | All UI text |
| `--font-mono` | `ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace` | Timestamps or code, when needed |
| `--font-size-xs` | `0.75rem` | Badges, captions |
| `--line-height-xs` | `1rem` | Text at `xs` |
| `--font-size-sm` | `0.875rem` | Labels, help/error text, buttons |
| `--line-height-sm` | `1.25rem` | Text at `sm` |
| `--font-size-base` | `1rem` | Body, inputs |
| `--line-height-base` | `1.5rem` | Text at `base` |
| `--font-size-lg` | `1.125rem` | h3, card titles |
| `--line-height-lg` | `1.75rem` | Text at `lg` |
| `--font-size-xl` | `1.5rem` | h2, section titles |
| `--line-height-xl` | `2rem` | Text at `xl` |
| `--font-size-2xl` | `2rem` | h1, page title |
| `--line-height-2xl` | `2.5rem` | Text at `2xl` |
| `--font-weight-regular` | `400` | Body text |
| `--font-weight-medium` | `500` | Labels, buttons |
| `--font-weight-semibold` | `600` | Headings, badges |

### Spacing, shape, and layout tokens

| Token | Value | Use |
| --- | --- | --- |
| `--space-1` | `0.25rem` | 4px |
| `--space-2` | `0.5rem` | 8px |
| `--space-3` | `0.75rem` | 12px |
| `--space-4` | `1rem` | 16px |
| `--space-5` | `1.25rem` | 20px |
| `--space-6` | `1.5rem` | 24px |
| `--space-8` | `2rem` | 32px |
| `--space-10` | `2.5rem` | 40px |
| `--space-12` | `3rem` | 48px |
| `--space-16` | `4rem` | 64px |
| `--radius-sm` | `0.25rem` | Small controls |
| `--radius-md` | `0.375rem` | Inputs, buttons, cards |
| `--radius-lg` | `0.5rem` | Dialogs |
| `--radius-full` | `9999px` | Badges, pills |
| `--shadow-sm` | `0 1px 2px rgba(15, 23, 42, 0.08)` | Cards, raised controls |
| `--shadow-md` | `0 4px 12px rgba(15, 23, 42, 0.12)` | Dialogs, popovers |
| `--layout-max` | `72rem` | Page container |
| `--reading-max` | `42rem` | Forms, detail copy |
| `--page-gutter` | `clamp(1rem, 4vw, 2rem)` | Page side padding |
| `--focus-ring-width` | `2px` | Focus outline |
| `--focus-ring-offset` | `2px` | Gap around focus outline |
| `--breakpoint-sm` | `40rem` | 640px |
| `--breakpoint-md` | `48rem` | 768px |
| `--breakpoint-lg` | `64rem` | 1024px |

The breakpoint tokens are documentation aliases only. CSS custom properties
are not valid inside `@media`, so media queries use the literal widths
`40rem`, `48rem`, and `64rem`.

### Color tokens

| Token | Value | Use |
| --- | --- | --- |
| `--color-bg` | `#f8fafc` | Page background |
| `--color-surface` | `#ffffff` | Cards, forms, dialogs |
| `--color-surface-muted` | `#f1f5f9` | Disabled/read-only fields, subtle panels |
| `--color-border` | `#cbd5e1` | Default borders |
| `--color-border-strong` | `#94a3b8` | Hover/secondary button borders |
| `--color-text` | `#0f172a` | Primary text |
| `--color-text-muted` | `#475569` | Secondary text, help text |
| `--color-primary` | `#1d4ed8` | Primary actions, links |
| `--color-primary-hover` | `#1e40af` | Primary hover |
| `--color-primary-active` | `#1e3a8a` | Primary active |
| `--color-primary-soft` | `#eff6ff` | Primary hover backgrounds |
| `--color-danger` | `#b91c1c` | Destructive actions, errors |
| `--color-danger-hover` | `#991b1b` | Destructive hover |
| `--color-danger-active` | `#7f1d1d` | Destructive active |
| `--color-danger-soft` | `#fef2f2` | Error backgrounds |
| `--color-success` | `#166534` | Finished/success text |
| `--color-success-soft` | `#dcfce7` | Finished/success background |
| `--color-warning` | `#b45309` | In-progress/warning text |
| `--color-warning-soft` | `#fffbeb` | Warning background |
| `--color-focus` | `#2563eb` | Focus outline |
| `--color-on-primary` | `#ffffff` | Text on primary/danger fills |

## Typography

Use `--font-sans` for all UI text. Use `--font-mono` only for timestamps or
code when a monospaced presentation is genuinely needed.

Set body text to `1rem` with `1.5rem` line height (`--font-size-base` and
`--line-height-base`). Body text is never smaller than `1rem`; the `sm` and
`xs` sizes are for labels, help/error text, badges, and captions, not for
paragraphs.

| Role | Element or class | Size and line height | Weight |
| --- | --- | --- | --- |
| Page title | `h1` | `--font-size-2xl` / `--line-height-2xl` | `--font-weight-semibold` |
| Section title | `h2` | `--font-size-xl` / `--line-height-xl` | `--font-weight-semibold` |
| Card title | `h3` | `--font-size-lg` / `--line-height-lg` | `--font-weight-semibold` |
| Body | `p`, list items, detail copy | `--font-size-base` / `--line-height-base` | `--font-weight-regular` |
| Small/caption | Help text, metadata, caption | `--font-size-sm` / `--line-height-sm`; badge/caption text uses `--font-size-xs` / `--line-height-xs` | `--font-weight-regular` |
| Label/button | `label`, button text | `--font-size-sm` / `--line-height-sm` | `--font-weight-medium` |

Heading rules:

- Use exactly one `h1` per page.
- Do not skip heading levels. A card title inside a page section is an `h3`
  only when the page has an `h2` section heading above it; otherwise use the
  next correct level rather than choosing a heading by its visual size.
- Long titles and long unbroken text must wrap. Use `overflow-wrap: anywhere`,
  `hyphens: auto`, and `min-width: 0` on flex/grid children. Do not truncate a
  journal item title or note; do not use `white-space: nowrap` on titles.
- Headings may use `text-wrap: balance` as progressive enhancement, but wrapping
  must remain usable without it.

## Spacing and layout

The spacing scale is based on 4px. Use the tokens in the table above; do not
introduce values such as `13px`, `1.1rem`, or a one-off `margin-top: 18px`.
Margins, padding, and gaps use spacing tokens, except for `0` and `1px` borders.

| Layout rule | Value |
| --- | --- |
| Page gutters | `padding-inline: var(--page-gutter)` |
| Page container width | `width: 100%; max-width: var(--layout-max); margin-inline: auto` |
| Reading/form width | `max-width: var(--reading-max); width: 100%` |
| Section-to-section gap | `var(--space-8)`; use `var(--space-12)` at `64rem` and above |
| Page header to content gap | `var(--space-6)` |
| Card padding | `var(--space-6)`; `var(--space-4)` below `40rem` |
| Card-to-card gap | `var(--space-4)` |
| Form field gap | `var(--space-4)` |
| Label-to-control gap | `var(--space-2)` |
| Help/error text gap | `var(--space-1)` |
| Inline action gap | `var(--space-2)` or `var(--space-3)` |
| Dialog action gap | `var(--space-3)` |
| Destructive action separation | At least `var(--space-8)` from primary actions |

Example page container:

```css
.page {
  width: 100%;
  max-width: var(--layout-max);
  margin-inline: auto;
  padding-inline: var(--page-gutter);
}

.page__content {
  max-width: var(--reading-max);
}
```

Two independently built screens align because they use the same page gutter,
container width, reading width, section gap, card padding, and field gap. Do
not override these with screen-specific spacing.

## Color and contrast

Map color tokens to roles; components use the role token, not a raw hex value.

| Role | Token | Usage |
| --- | --- | --- |
| Page background | `--color-bg` | Application background |
| Surface | `--color-surface` | Cards, forms, dialogs, list rows |
| Muted surface | `--color-surface-muted` | Disabled/read-only fields, empty panels |
| Border | `--color-border` | Decorative separators and non-essential card borders |
| Strong border | `--color-border-strong` | Secondary emphasis where it is not the only state indicator |
| Text | `--color-text` | Primary text and headings |
| Muted text | `--color-text-muted` | Help text, metadata, optional values, essential control boundaries |
| Primary | `--color-primary` | Primary actions, links, selected controls, focus-adjacent emphasis |
| Primary hover | `--color-primary-hover` | Primary hover |
| Primary active | `--color-primary-active` | Primary active |
| Danger | `--color-danger` | Destructive actions, errors, invalid borders |
| Danger hover | `--color-danger-hover` | Destructive hover |
| Danger active | `--color-danger-active` | Destructive active |
| Success | `--color-success` | Finished/success text |
| Warning | `--color-warning` | In-progress/warning text |
| Focus | `--color-focus` | Visible focus outline |

Rules:

- Use `--color-on-primary` for text on primary and danger fills.
- Use `--color-text-muted` for essential control boundaries (inputs, selects,
  textareas, secondary buttons) because it meets non-text contrast against both
  page and surface backgrounds. `--color-border` and `--color-border-strong`
  do not meet the 3:1 non-text requirement on their own against light
  backgrounds, so they are never the only way to identify an interactive
  control or its state.
- Status is never communicated by color alone; the badge text is required.
- Errors are never communicated by color alone; inline error text and an
  accessible alert are required.

### Contrast checks

WCAG 2.1 AA requires at least `4.5:1` for normal text, `3:1` for large text,
and `3:1` for non-text UI components and states. Ratios below are measured
against the listed background.

Normal text:

| Text token | Background token | Ratio | Result |
| --- | --- | --- | --- |
| `--color-text` | `--color-bg` | `17.06:1` | Pass |
| `--color-text` | `--color-surface` | `17.85:1` | Pass |
| `--color-text` | `--color-surface-muted` | `16.30:1` | Pass |
| `--color-text-muted` | `--color-bg` | `7.24:1` | Pass |
| `--color-text-muted` | `--color-surface` | `7.58:1` | Pass |
| `--color-text-muted` | `--color-surface-muted` | `6.92:1` | Pass |
| `--color-primary` | `--color-bg` | `6.41:1` | Pass |
| `--color-primary` | `--color-surface` | `6.70:1` | Pass |
| `--color-primary` | `--color-primary-soft` | `6.16:1` | Pass |
| `--color-danger` | `--color-bg` | `6.18:1` | Pass |
| `--color-danger` | `--color-surface` | `6.47:1` | Pass |
| `--color-danger` | `--color-danger-soft` | `5.91:1` | Pass |
| `--color-success` | `--color-bg` | `6.81:1` | Pass |
| `--color-success` | `--color-surface` | `7.13:1` | Pass |
| `--color-success` | `--color-success-soft` | `6.49:1` | Pass |
| `--color-warning` | `--color-bg` | `4.80:1` | Pass |
| `--color-warning` | `--color-surface` | `5.02:1` | Pass |
| `--color-warning` | `--color-warning-soft` | `4.84:1` | Pass |
| `--color-on-primary` | `--color-primary` | `6.70:1` | Pass |
| `--color-on-primary` | `--color-primary-hover` | `8.72:1` | Pass |
| `--color-on-primary` | `--color-primary-active` | `10.36:1` | Pass |
| `--color-on-primary` | `--color-danger` | `6.47:1` | Pass |
| `--color-on-primary` | `--color-danger-hover` | `8.31:1` | Pass |
| `--color-on-primary` | `--color-danger-active` | `10.02:1` | Pass |
| `--badge-planned-text` | `--badge-planned-bg` | `8.40:1` | Pass |
| `--badge-progress-text` | `--badge-progress-bg` | `8.49:1` | Pass |
| `--badge-finished-text` | `--badge-finished-bg` | `8.30:1` | Pass |
| `--badge-dropped-text` | `--badge-dropped-bg` | `8.20:1` | Pass |

Large text:

Every pair in the normal-text table exceeds `4.5:1`, so every pair also
exceeds the `3:1` large-text requirement. Do not use a token combination for
large text that would fail the normal-text requirement.

Non-text UI:

| Non-text element | Foreground token | Background token | Ratio | Result |
| --- | --- | --- | --- | --- |
| Focus outline | `--color-focus` | `--color-bg` | `4.94:1` | Pass |
| Focus outline | `--color-focus` | `--color-surface` | `5.17:1` | Pass |
| Essential control boundary | `--color-text-muted` | `--color-bg` | `7.24:1` | Pass |
| Essential control boundary | `--color-text-muted` | `--color-surface` | `7.58:1` | Pass |
| Primary fill | `--color-primary` | `--color-surface` | `6.70:1` | Pass |
| Danger fill | `--color-danger` | `--color-surface` | `6.47:1` | Pass |
| Success fill | `--color-success` | `--color-surface` | `7.13:1` | Pass |
| Warning fill | `--color-warning` | `--color-surface` | `5.02:1` | Pass |
| Decorative border | `--color-border` | `--color-surface` | `1.48:1` | Not for essential UI |
| Strong decorative border | `--color-border-strong` | `--color-surface` | `2.56:1` | Not for essential UI |

The last two rows are recorded so the tokens are not misused: they are
decorative only unless another visible cue identifies the control and its
state. Status badge borders are also decorative because the status text always
conveys the state.

## Buttons

Shared button rules apply to primary, secondary, danger, and ghost/link
variants. A button is always a `button` element for an action; it is never an
anchor used to submit or delete.

```css
.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  min-height: 2.75rem; /* 44px touch target */
  padding: var(--space-3) var(--space-4);
  border: 1px solid transparent;
  border-radius: var(--radius-md);
  font-family: var(--font-sans);
  font-size: var(--font-size-sm);
  line-height: var(--line-height-sm);
  font-weight: var(--font-weight-medium);
  text-align: center;
  text-decoration: none;
  cursor: pointer;
}

.button:focus-visible {
  outline: var(--focus-ring-width) solid var(--color-focus);
  outline-offset: var(--focus-ring-offset);
}
```

Button states:

| Variant | Default | Hover | Active | Focus-visible | Disabled | Loading |
| --- | --- | --- | --- | --- | --- | --- |
| Primary | Background `--color-primary`; text `--color-on-primary`; border `--color-primary` | Background and border `--color-primary-hover` | Background and border `--color-primary-active` | Focus outline `--focus-ring-width` solid `--color-focus`, offset `--focus-ring-offset` | Background `--color-surface-muted`; text `--color-text-muted`; border `--color-border`; `cursor: not-allowed` | Default styling plus busy label, `aria-busy="true"`, disabled submission |
| Secondary | Background `--color-surface`; text `--color-primary`; border `--color-text-muted` | Background `--color-primary-soft`; text `--color-primary-hover`; border `--color-primary` | Background `--color-primary-soft`; text `--color-primary-active`; border `--color-primary-active` | Same focus outline; keeps current background | Same disabled styling as primary | Default styling plus busy label, `aria-busy="true"`, disabled submission |
| Danger | Background `--color-danger`; text `--color-on-primary`; border `--color-danger` | Background and border `--color-danger-hover` | Background and border `--color-danger-active` | Same focus outline | Same disabled styling as primary | Default styling plus busy label, `aria-busy="true"`, disabled submission |
| Ghost/link | Background transparent; text `--color-primary`; border transparent; underlined | Background `--color-primary-soft`; text `--color-primary-hover`; underline thickness `2px` | Background `--color-primary-soft`; text `--color-primary-active` | Same focus outline | Text `--color-text-muted`; no hover background; `cursor: not-allowed` | Default styling plus busy label, `aria-busy="true"`, disabled submission |

Rules:

- Use the primary variant for the one main action in a view, such as
  `Add item`, `Save changes`, `Add note`, or `Log in`.
- Use the secondary variant for supporting actions such as `Cancel`,
  `Clear filters`, `Try again`, or navigation back to the list.
- Use the danger variant only for destructive actions and only inside the
  confirmation flow: `Delete item` or `Delete note`.
- Use the ghost/link variant for low-emphasis non-destructive actions such as
  `Clear filters` or `Add note` when the screen already has another primary
  action. Do not use it for navigation; use an actual link for navigation.
- Every button has a minimum `44px` by `44px` touch target. Do not reduce the
  target with negative margins.
- Buttons size to their content by default. A form's submit button and dialog
  actions may be full width only where the responsive rules below say so, or
  when the button is the only control in a narrow action area. Inline row
  actions never stretch to fill leftover space.

Loading behavior:

- Keep the button width stable between its idle and busy labels. Reserve the
  idle label's space, for example with a fixed minimum width measured from the
  idle label or by rendering both labels in the same grid cell, with the idle
  label hidden but occupying space.
- Show the specific busy label in the button. Do not replace the label with an
  icon alone.
- Set `aria-busy="true"` on the button and disable submission with the
  `disabled` attribute (or `aria-disabled="true"` plus an event guard when
  focus must be preserved).
- Ignore repeated clicks/keyboard activation until the request finishes. This
  prevents double submission.

| Action | Busy label |
| --- | --- |
| Log in | `Logging in…` |
| Register | `Creating account…` |
| Log out | `Logging out…` |
| Add item | `Adding item…` |
| Save item changes | `Saving changes…` |
| Add note | `Adding note…` |
| Save note changes | `Saving note…` |
| Delete item | `Deleting item…` |
| Delete note | `Deleting note…` |

Use the ellipsis character `…` in these labels.

## Links and navigation actions

Use an anchor with a real `href` for navigation, including primary navigation
and links between pages.

| State | Treatment |
| --- | --- |
| Default | Color `--color-primary`; underlined; `text-underline-offset: 0.15em` |
| Hover | Color `--color-primary-hover`; underline thickness `2px` |
| Active | Color `--color-primary-active`; underline remains visible |
| Focus-visible | `outline: var(--focus-ring-width) solid var(--color-focus)` with `outline-offset: var(--focus-ring-offset)`; underline remains visible |
| Visited | Same color as default, `--color-primary`; never a different visited color |

Rules:

- Links are underlined by default. Do not remove the underline unless another
  non-color cue, such as the focus outline or a clearly button-like control,
  still identifies the interactive element.
- Navigation actions use the same link treatment. The current page link sets
  `aria-current="page"` and uses a `2px` underline plus
  `--color-primary-active`. The visible label still matches the destination.
- Inline links are for navigation only. Do not use an inline link to submit a
  form, save, delete, or trigger any destructive action. Use a button instead.
- Link text must describe the destination, not "click here".
- A skip link is the first focusable element on every page; see
  [Accessibility](#accessibility).

## Forms

Form layout:

- Constrain forms and detail reading copy to `--reading-max`. Below `40rem`,
  forms fill the available content width.
- Put a visible `label` above each control. The label is associated with the
  control with `for`/`id`. Placeholder text is never the label.
- Stack fields with `var(--space-4)` between fields. Use `var(--space-8)`
  between form sections or fieldsets.
- Put help text below the control with `var(--space-1)` separation.
- Show a required indicator on required labels. Use a visible `*` immediately
  after the label text, mark it `aria-hidden="true"`, set the control's
  `required` attribute, and show the note `Fields marked * are required.` once
  near the start of the form.
- Group related checkboxes or radios in a `fieldset` with a visible `legend`.

Control rules:

- Inputs, selects, and textareas use `1rem` text (`--font-size-base`) and
  `1.5rem` line height (`--line-height-base`).
- Controls have a minimum `44px` touch target. For checkbox and radio, make the
  entire label row at least `44px` tall even if the visual control is smaller.
- Use `--radius-md`, background `--color-surface`, text `--color-text`, and a
  `1px` border. The default border is `--color-text-muted` so the control
  boundary meets non-text contrast.
- Padding for inputs, selects, and textareas is `var(--space-2)
  var(--space-3)`.
- Textareas have `min-height: 8rem` and resize vertically only.
- Selects keep a native select affordance; do not replace it with a custom
  JS-only control.
- Checkboxes use `accent-color: var(--color-primary)`; radio buttons use the
  same accent. Never hide the native focus indicator without an equivalent
  visible focus style.

Control states:

| Control state | Input, select, textarea | Checkbox and radio |
| --- | --- | --- |
| Default | Background `--color-surface`; text `--color-text`; border `1px solid var(--color-text-muted)` | Accent `--color-primary`; label row at least `44px` tall |
| Hover | Border `--color-text` | Accent `--color-primary-hover`; label row keeps pointer |
| Focus | Border `--color-focus`; outline `var(--focus-ring-width) solid var(--color-focus)` with `var(--focus-ring-offset)` | Visible focus ring around the control or its label row; accent `--color-focus` |
| Filled | Text `--color-text`; default boundary remains visible | Selected control remains visibly checked |
| Disabled | Background `--color-surface-muted`; text `--color-text-muted`; border `--color-border`; `cursor: not-allowed` | Disabled attribute on the control and group; label text `--color-text-muted` |
| Read-only | Background `--color-surface-muted`; text `--color-text`; border `--color-border-strong`; `cursor: default` | Not applicable; use disabled for a non-editable group |
| Invalid | Border `--color-danger`; inline error text `--color-danger`; `aria-invalid="true"` | Invalid group has error text and `aria-invalid="true"` on the group/control |

Help and error linkage:

- Give help text an `id` and reference it from the control with
  `aria-describedby`.
- Give the error message an `id` and include it in `aria-describedby`. When a
  field has both help and error text, reference both ids in a space-separated
  list.
- Set `aria-invalid="true"` only while the field is invalid; remove it when the
  error is resolved.
- Error text is visible; do not rely on a red border alone.

Illustrative markup:

```html
<div class="field">
  <label for="title">Title <span aria-hidden="true">*</span></label>
  <input id="title" name="title" type="text" required
         aria-describedby="title-help title-error" aria-invalid="true">
  <p id="title-help" class="field__help">Use the title as you want it shown in your journal.</p>
  <p id="title-error" class="field__error">Enter a title.</p>
</div>
```

## Validation and copy

Validation timing:

1. Do not show an error for an untouched field before submission.
2. On submit, validate every field and show all inline errors.
3. On field blur, validate that field after the user has interacted with it.
4. After a field's first error, revalidate it on `input` or `change` so the
   error clears as soon as the value becomes valid.
5. Keep the user's input values and note text when validation or saving fails.
   Never reset a form on a failed request.
6. On submit failure, move focus to the first invalid field. If the failure is
   a non-field error, focus the page-level alert heading.
7. Map server field errors to the matching inline field using the same error
   presentation. Put non-field server errors in the page-level alert.
8. Never expose raw server messages, status codes, API paths, or stack traces.

Exact validation copy:

| Case | Copy |
| --- | --- |
| Required title | `Enter a title.` |
| Required type | `Choose a type.` |
| Required note | `Enter a note.` |
| Invalid date range | `Finish date cannot be before start date.` |
| Invalid credentials | `The username or password is incorrect.` |
| Expired session | `Your session expired. Log in again to continue.` |
| Generic save fallback | `We couldn't save your changes. Try again.` |
| Generic load fallback | `We couldn't load this page. Try again.` |

Inline errors use the danger text token and the field linkage rules above.
Non-field errors use the page-level alert structure in
[Error states](#error-states).

## Status badges

Use exactly these four status labels and capitalization: `Planned`,
`In progress`, `Finished`, `Dropped`.

| Status | Background token and value | Text token and value | Border token and value |
| --- | --- | --- | --- |
| `Planned` | `--badge-planned-bg` `#e2e8f0` | `--badge-planned-text` `#334155` | `--badge-planned-border` `#cbd5e1` |
| `In progress` | `--badge-progress-bg` `#dbeafe` | `--badge-progress-text` `#1e3a8a` | `--badge-progress-border` `#93c5fd` |
| `Finished` | `--badge-finished-bg` `#dcfce7` | `--badge-finished-text` `#14532d` | `--badge-finished-border` `#86efac` |
| `Dropped` | `--badge-dropped-bg` `#fee2e2` | `--badge-dropped-text` `#7f1d1d` | `--badge-dropped-border` `#fca5a5` |

Badge composition:

- Padding: `var(--space-1) var(--space-2)`.
- Radius: `var(--radius-full)`.
- Font size: `var(--font-size-xs)`; line height `var(--line-height-xs)`.
- Font weight: `var(--font-weight-semibold)`.
- Border: `1px solid` using the status token above.
- Keep the status text visible and keep it on one line; let surrounding
  containers wrap instead of shrinking the label.
- Status is conveyed by the text label, not color alone. Never render a
  status as a colored dot without its label.

Unexpected status fallback:

- If a status is missing or not one of the four known values, render a neutral
  badge with `--badge-neutral-bg`, `--badge-neutral-text`, and
  `--badge-neutral-border`.
- The fallback label is `Unknown`. Do not invent a status or map an unexpected
  value silently to `Planned`.

Illustrative markup:

```html
<span class="badge badge--progress">In progress</span>
```

## Empty states

Empty states are displayed only after a successful load returns an empty
result. They are never displayed while loading, and they are never displayed
when an error alert is present.

| State | When shown | Heading (`h2`) | Body | Action |
| --- | --- | --- | --- | --- |
| No items yet | The list loaded successfully, there are no items, and no search or filters are active | `No items yet` | `Add a book or movie to start your journal.` | `Add your first item` |
| No search or filter matches | The list loaded successfully, at least one search term or filter is active, and the result is empty | `No matching items` | `No items match your search or filters. Try changing them.` | `Clear filters` |
| No notes | The item detail loaded successfully and the item has no notes | `No notes yet` | `Add a note to capture your thoughts about this item.` | `Add note` |

Rules:

- Empty states use neutral styling: `--color-surface` or
  `--color-surface-muted` background, `--color-border` border, `--color-text`
  heading, and `--color-text-muted` body. Do not use a danger fill.
- The no-items action is the documented empty-state variant of the `Add item`
  action and uses the primary button variant.
- The no-match action uses the secondary or ghost/link button variant. It
  clears every active search term and filter. It must not say or imply that
  the journal has no items.
- The no-notes action uses the primary button variant within the notes area, or
  the ghost/link variant when the detail page already has a primary action.
- Do not repeat an empty-state action that is already available in the page
  header.

## Loading states

Every loading state has at least one visible loading cue (text, skeleton, or a
spinner with text), a status announcement, reserved space to avoid layout
shift, disabled repeat actions, and a guard that prevents an empty state from
rendering.

| Loading area | Visible treatment | Announcement | Reserved space and repeat-action rule |
| --- | --- | --- | --- |
| Initial page load | Page skeleton matching the header and first content block, plus visible `Loading page…` | Put `role="status"` and `aria-live="polite"` on the loading message; set `aria-busy="true"` on the main content region | Reserve at least a header block plus one card; do not render empty states or action buttons for unloaded content |
| Item list load | Three skeleton rows, or visible `Loading items…` with a spinner | `role="status"` and `aria-live="polite"`; `aria-busy="true"` on the list region | Reserve three row heights; hide empty state and keep the toolbar's Add action disabled if it depends on loaded data |
| Item detail load | Heading and text skeletons, or visible `Loading item…` with a spinner | `role="status"` and `aria-live="polite"`; `aria-busy="true"` on the detail region | Reserve the detail heading and first card height; do not render the notes empty state early |
| Form submit | Keep the form visible; replace the submit label with its busy label from the button table | `aria-busy="true"` on the button and, if the whole form is pending, on the form region; visible busy label | Button width stays stable; disable the submit button and prevent double submission |
| Note submit | Keep the note editor visible; replace the note button label with `Adding note…` or `Saving note…` | `aria-busy="true"` on the note button and note region | Keep the editor height and action-row height stable; disable the note action |
| Delete | Keep the confirmation dialog open; use `Deleting item…` or `Deleting note…` on the confirm button | `aria-busy="true"` on the confirm button; visible busy label | Do not close the dialog until success; disable both dialog action buttons while pending |

Rules:

- Do not show an empty state based on initial default data before the request
  finishes. Check the loading state before the empty state.
- Loading text is still text: do not use an unlabeled spinner as the only cue.
- For a spinner, mark the spinner graphic `aria-hidden="true"` and put the
  accessible loading text in the status message.
- If a skeleton is used, keep it neutral with `--color-surface-muted` and
  `--color-border`. Do not use a skeleton shimmer when
  `prefers-reduced-motion: reduce` is active.

Illustrative markup:

```html
<div class="loading-state" role="status" aria-live="polite">
  <span class="spinner" aria-hidden="true"></span>
  <span>Loading items…</span>
</div>
```

## Error states

Page-level alert structure:

- Use `role="alert"` on the alert container.
- Use `--color-danger-soft` background, `--color-danger` text, and a
  `--color-danger` border.
- Include a heading (`h2`) and a body paragraph. Add an optional retry or
  navigation action using the button or link rules.
- Place the alert near the top of the affected page or form region.
- Use the same structure for non-field server errors.
- Never expose raw server or stack details.

```html
<section class="alert alert--danger" role="alert">
  <h2>We couldn't load this page</h2>
  <p>Check your connection and try again.</p>
  <button type="button" class="button button--secondary">Try again</button>
</section>
```

Exact error copy:

| Failure | Heading | Body | Action |
| --- | --- | --- | --- |
| Network or 5xx load failure | `We couldn't load this page` | `Check your connection and try again.` | `Try again` |
| Not found or forbidden | `This item isn't available` | `It may have been deleted, or you may not have access to it.` | `Back to items` |
| Unauthorized or expired session | `Your session expired` | `Log in again to continue.` | `Log in` |
| Item delete failure | `We couldn't delete this item` | `Try again. Nothing was deleted.` | `Try again` |
| Note save failure | `We couldn't save your note` | `Try again. Your text is still here.` | `Try again` |
| Note delete failure | `We couldn't delete this note` | `Try again. Nothing was deleted.` | `Try again` |
| Generic fallback | `Something went wrong` | `Try again. If the problem continues, reload the page.` | `Try again` |

Inline field errors use the exact validation copy in
[Validation and copy](#validation-and-copy), the danger text token, and the
`aria-describedby`/`aria-invalid` linkage in [Forms](#forms).

## Destructive confirmation

Both destructive dialogs use the same accessible modal behavior:

- Render a modal dialog with `role="dialog"`, `aria-modal="true"`, and
  `aria-labelledby` pointing to the dialog heading. Use `aria-describedby` for
  the consequence text.
- Initial focus is on `Cancel`.
- `Escape` and a click on the backdrop cancel the dialog. A click inside the
  dialog does not.
- Trap focus inside the dialog while it is open. `Tab` and `Shift+Tab` cycle
  through the dialog's controls only.
- Return focus to the element that opened the dialog when it is cancelled.
  After a successful deletion the trigger may no longer exist; move focus to
  the page heading or the next item in the list and announce the removal.
- Keep the dialog open and disable its actions while the delete request is
  pending.
- Never use vague copy such as "Are you sure?" or "OK".

### Delete item dialog

- Heading: `Delete "{item title}"?`
- Body: `This permanently deletes "{item title}" and all of its notes. This can't be undone.`
- Actions: `Cancel` (secondary) and `Delete item` (danger).
- The item title must appear in both the heading and the body. The note
  consequence is required even when the item currently has no notes.

### Delete note dialog

- Heading: `Delete this note?`
- Body: `This permanently deletes the note dated {date}: "{note excerpt}". This can't be undone.`
- Actions: `Cancel` (secondary) and `Delete note` (danger).
- `{date}` uses the date display format in
  [Consistency rules](#consistency-rules).
- `{note excerpt}` is the first 80 characters of the note, followed by `...`
  when truncated. It identifies the note without rendering arbitrary HTML.
- If the note has no text, the body still identifies it by its date and uses
  `an empty note` in place of the excerpt.

Dialog actions use `var(--space-3)` between buttons. On widths below `40rem`,
stack them with Cancel first and make both full width. The confirm action keeps
its danger styling and its specific label; never change `Delete item` or
`Delete note` to `OK`.

## Accessibility

All screens meet WCAG 2.1 AA.

- **Contrast:** Use the checked token pairs in [Color and contrast](#color-and-contrast).
  Normal text meets `4.5:1`, large text meets `3:1`, and non-text UI meets
  `3:1`.
- **Visible focus:** Every focusable control has a visible focus indicator of
  at least `--focus-ring-width` (`2px`) with `--focus-ring-offset` (`2px`),
  using `--color-focus`. Never remove an outline without an equivalent visible
  replacement.
- **Keyboard:** Every action is operable with a keyboard. Use logical DOM
  order, native controls, and expected keys. `Enter` and `Space` activate
  buttons; `Escape` closes menus and dialogs. Do not create keyboard traps
  outside modal focus management.
- **Labels and names:** Every control has a visible label and an accessible
  name. Icon-only controls require an accessible name. Placeholder text does
  not replace a label.
- **Semantics:** Use one `h1` per page, do not skip heading levels, use
  `header`, `nav`, `main`, and `footer` landmarks appropriately, and use list
  markup for item and note collections.
- **No color-only meaning:** Status uses text labels; errors use visible error
  text and an alert; required fields use the visible indicator plus the
  required attribute.
- **Announcements:** Loading uses `role="status"` or `aria-live="polite"`.
  Errors use `role="alert"`. Avoid duplicate announcements from nested live
  regions.
- **Dialogs:** Use the focus management, Escape handling, focus trap, and focus
  return described in [Destructive confirmation](#destructive-confirmation).
- **Skip link:** The first focusable element on each page is
  `Skip to main content`, linking to `#main-content`. The main landmark has
  `id="main-content"` and receives focus when the skip link is used.
- **Touch targets:** Interactive targets are at least `44px` by `44px`,
  including checkbox and radio rows.
- **Reduced motion:** Support `prefers-reduced-motion: reduce`. Disable
  non-essential transitions and skeleton shimmer; use static loading blocks or
  text. Motion is never required to understand state.
- **Zoom and reflow:** The layout remains usable at 200% browser zoom and at
  `320px` viewport width. Text is not clipped, controls remain operable, and
  there is no horizontal scrolling.
- **Language and titles:** Set the document language (for example
  `lang="en"`) and give every route a descriptive page title.

## Responsive rules

Build mobile-first. The default rules apply below `40rem`, then the literal
media query widths add enhancements. The `--breakpoint-*` tokens are
documentation aliases only; use the literal values in `@media`.

### Below `40rem` (mobile)

- Use `--page-gutter` side padding. At `320px` this resolves to `1rem`; content
  must not require more horizontal space than the viewport.
- Content is one column with a maximum width of `100%`.
- Primary navigation collapses to a `Menu` disclosure button with
  `aria-expanded` and `aria-controls`. The expanded menu lists the same
  navigation links in a vertical list.
- Item lists render as stacked cards. Each card shows title, type, status,
  optional author/director, and updated date without overlapping.
- Forms fill the available content width. Form fields are full width.
- Action groups stack vertically. Form submit buttons and dialog action buttons
  are full width; inline ghost/link actions may stay content width when they
  fit.
- Dialogs are inset from the viewport: `width: min(32rem, calc(100vw - 2 *
  var(--space-4)))`, with `max-height: calc(100vh - 2 * var(--space-6))` and
  vertical scrolling when needed.
- Long titles, long note words, and email-like strings wrap with
  `overflow-wrap: anywhere`. Badges may wrap to the next line rather than
  forcing horizontal scroll.
- Ensure there is no horizontal scrolling at `320px`.

### At `40rem` and above

```css
@media (min-width: 40rem) {
  /* small-screen enhancements */
}
```

- Keep `--page-gutter` and the `--layout-max` container.
- List cards may become two-column rows: title and metadata take the flexible
  first column, status takes the second. Use `minmax(0, 1fr)` for the flexible
  column.
- Form submit and dialog action groups may align inline at the end of their
  container; they are no longer forced full width.
- Dialogs use `width: min(32rem, calc(100vw - 2 * var(--space-8)))` and stay
  centered vertically with a viewport margin.
- Forms and detail reading copy keep `--reading-max`.

### At `48rem` and above

```css
@media (min-width: 48rem) {
  /* tablet enhancements */
}
```

- Replace the collapsed menu with horizontal primary navigation in the page
  header. Keep the skip link first in DOM order.
- Item list rows use a stable grid: title and metadata, then status, then
  updated date. Rows remain full width within the page container.
- Page headers may place the page title and the single primary action on one
  row, with the action aligned to the end.
- Forms stay at `--reading-max`; do not stretch form controls across the full
  page width.

### At `64rem` and above

```css
@media (min-width: 64rem) {
  /* desktop enhancements */
}
```

- Center the page container at `--layout-max` with `--page-gutter` side
  padding.
- Increase section separation to `var(--space-12)` and keep card padding at
  `var(--space-6)`.
- List rows may show the complete metadata set (type, author/director,
  status, updated date) without wrapping under normal lengths; long values
  still wrap.
- Detail reading copy remains at `--reading-max`; cards may use the remaining
  space only when they do not reduce reading comfort.
- Dialogs keep `width: min(32rem, calc(100vw - 2 * var(--space-8)))` and the
  `--shadow-md` elevation.
- Navigation remains horizontal and links keep the same underline, hover,
  active, focus, and visited treatment.

Across all breakpoints, no horizontal scrolling is allowed. Avoid fixed widths
larger than the viewport, negative margins that create overflow, and truncation
of titles or note text.

## Consistency rules

Use a small shared set of UI primitives. #14-#23 may implement them in shared
Vue code, but they must agree on these names and responsibilities:

| Primitive | Responsibility | Primary tokens |
| --- | --- | --- |
| Page container and header | Page gutters, `--layout-max`, `h1`, optional page action | `--page-gutter`, `--layout-max`, `--space-6`, `--space-8` |
| Card | Group related content or list rows | `--color-surface`, `--color-border`, `--radius-md`, `--shadow-sm`, `--space-6` |
| Button | Primary, secondary, danger, ghost/link actions and loading state | Button rules above |
| Form field | Label, control, help text, inline error linkage | Form rules above |
| Badge | The four journal statuses and neutral fallback | Status badge rules above |
| Alert | Page-level error or non-field message | `role="alert"`, `--color-danger-soft`, `--color-danger` |
| Empty state | Neutral empty-result explanation and one action | `--color-surface-muted`, `--color-text`, `--color-text-muted` |
| Loading state | Visible loading cue and announcement | `role="status"`, `--color-surface-muted`, `--color-border` |
| Confirmation dialog | Destructive confirmation with focus management | `--radius-lg`, `--shadow-md`, danger action rules |

Consistency rules:

- Use tokens instead of one-off styles. Do not put raw hex colors, arbitrary
  spacing, or custom radii in components.
- Use one primary action per view. If a view has no natural primary action,
  leave the primary variant unused rather than promoting a secondary action.
- Use the same label and variant for the same action everywhere. Canonical
  labels include `Add item`, `Save changes`, `Add note`, `Save note`,
  `Delete item`, `Delete note`, `Cancel`, `Clear filters`, `Try again`,
  `Log in`, `Register`, and `Log out`.
- `Add your first item` is the required no-items empty-state label for the
  add action; the persistent toolbar action remains `Add item`. Both use the
  primary variant and go to the same create screen.
- Use sentence case for headings, labels, buttons, help text, and messages.
  The four status labels are the only intentional title-case exception:
  `Planned`, `In progress`, `Finished`, `Dropped`.
- Keep destructive actions separate from primary actions. Do not place
  `Delete item` or `Delete note` in the same action row as `Edit item` or
  `Save changes`; use a separate danger area or a dialog, with at least
  `var(--space-8)` separation and no default focus.
- Show missing optional values with an em dash: `—`. The accessible name is
  `Not provided`, for example `<span aria-label="Not provided">—</span>`. Do
  not use a blank cell, `N/A`, or `null`.
- Display dates in one documented format: `MMM D, YYYY`, for example
  `Nov 14, 2026`. When a timestamp is needed, append the time as
  `MMM D, YYYY, h:mm A`, for example `Nov 14, 2026, 3:45 PM`. Month
  abbreviations are `Jan`, `Feb`, `Mar`, `Apr`, `May`, `Jun`, `Jul`, `Aug`,
  `Sep`, `Oct`, `Nov`, `Dec`.
- Wrap every displayed date and timestamp in a semantic `<time>` element with
  an ISO 8601 `datetime` value:
  `<time datetime="2026-11-14">Nov 14, 2026</time>` or
  `<time datetime="2026-11-14T15:45:00Z">Nov 14, 2026, 3:45 PM</time>`.
- Use one date format for progress dates, notes, and list metadata. Do not
  switch to relative labels such as "2 days ago" in one screen and absolute
  dates in another.

## Implementation map

These issues apply this specification. Each issue keeps its own acceptance
criteria; this document does not duplicate or replace them.

| Issue | UI area | This document supplies |
| --- | --- | --- |
| #14 | App shell, navigation, layout, and routes | Page container/header, skip link, navigation collapse, focus and responsive shell rules |
| #15 | Shared API client, token attachment, and error mapping | Error alert structure, exact user-facing copy, inline versus non-field error mapping |
| #16 | Registration, login, and logout screens | Form layout, validation copy, button loading labels, session-expired alert |
| #17 | Item list screen | List loading, empty states, status badges, list row/card responsive behavior |
| #18 | Item create screen | Form controls, validation copy, date display, save loading and error states |
| #19 | Item detail screen | Reading width, notes empty state, status badges, date display, detail loading/error states |
| #20 | Item edit and delete screens | Form states, destructive confirmation dialog, delete loading and failure copy |
| #21 | Progress and date controls | Required/optional field rules, date-range validation copy, date display format |
| #22 | Notes UI | Note form, note empty state, note loading states, note deletion dialog, note error copy |
| #23 | Search and filter UI | No-match empty state, `Clear filters` action, form control states, accessibility |

If an implementation appears to conflict with this specification, follow the
issue's acceptance criteria and raise the conflict with the PM rather than
changing this document silently. No new follow-up issue is needed for the
out-of-scope work listed below because each area already has an issue.

## Out of scope and change control

This documentation task changes only `_docs/design-system.md`. It does not
modify `_docs/tasks.md`, `frontend/`, `backend/`, dependencies, configs, tests,
routes, or components. It does not create CSS/SCSS files, Vue components,
global styles, or scaffold changes.

The following are implemented by their existing issues:

- App shell, navigation, layout, and routes: #14.
- Shared API client, token attachment, and error mapping: #15.
- Registration, login, and logout screens: #16.
- Item list screen: #17.
- Item create screen: #18.
- Item detail screen: #19.
- Item edit and delete screens: #20.
- Progress and date controls: #21.
- Notes UI: #22.
- Search and filter UI: #23.
- Playwright end-to-end tests: #24.
- Containerization, CI, deployment, observability, alerting, responder
  runbook, and PostgreSQL migration: #25-#33.

Future changes to these tokens, states, copy, or interaction rules require a
new groomed task. Do not change acceptance criteria after implementation
starts.
