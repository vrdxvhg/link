# JARVIS V2 UI Lock — eDEX-UI Foundation

## Status

**LOCKED** — JARVIS V2 desktop UI must retain the eDEX-UI visual foundation already selected for this project.

The repository contains the source archive `edex-ui-master.zip`, which is the selected UI reference.

## Rule

Do not replace the eDEX-UI shell with a conventional dashboard, card-grid admin panel, or generic chatbot interface.

JARVIS functionality is integrated **inside the eDEX-UI-style shell**.

## Visual foundation

The UI keeps the major eDEX-UI characteristics:

- fullscreen sci-fi command-console presentation
- futuristic terminal-first composition
- system-monitoring panels around the central workspace
- dense technical information layout
- dark sci-fi presentation with luminous accent elements
- file-system visibility
- terminal / command interaction
- live machine and network telemetry areas
- modular panels that can host JARVIS functions

The upstream eDEX-UI interface is built around a terminal plus filesystem and monitoring modules; JARVIS extends that composition rather than redesigning it.

## JARVIS module mapping

| eDEX-style area | JARVIS V2 role |
| --- | --- |
| Main terminal | JARVIS command console / agent interaction |
| Filesystem panel | uploaded files, workspace, generated assets |
| CPU/RAM/system modules | JARVIS runtime and system monitor |
| Network modules | Bridge/API connectivity and automation health |
| Process panels | active agents, workers, and jobs |
| Clock/status areas | runtime state, listening state, lock state |
| Secondary module slots | song pipeline, rendering, thumbnail, metadata, YouTube state |
| Keyboard/touch interaction | direct JARVIS command input |

## Interaction principles

1. Voice and text commands must feel native to the terminal/console environment.
2. Active jobs and automation status are represented as live technical modules, not generic web cards.
3. Uploads from the Android/Bridge layer appear through the existing filesystem/workspace presentation.
4. Human approval before YouTube publishing remains a visible control/state in the JARVIS workflow.
5. UI changes must preserve the eDEX visual language even when new JARVIS capabilities are added.

## Implementation boundary

The UI layer should communicate with JARVIS Core through stable APIs/adapters. Core logic must not depend on DOM selectors or visual layout details. This keeps YouTube/browser automation and backend logic independent from UI changes.

## Reference

The selected eDEX source archive is kept in the repository as `edex-ui-master.zip` and must remain the source reference for the desktop UI direction.
