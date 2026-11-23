# Diagram Bench

[Open Diagram Bench](https://coolcode.ca/diagrambench/) — edit diagram text, render it locally, and save SVG, PNG or an editable JSON project.

<!-- coolcode:guide -->
Choose a starting point or write your own Mermaid source, then select **Render diagram**. The preview and exported image keep the last successful render when a later edit has a syntax error. **Save project** includes that rendered source so it can be reopened and edited. Mermaid runs locally; selecting Kroki requires your own server address and an explicit permission checkbox before code is sent there.
<!-- /coolcode:guide -->

## Use it

The first real example renders immediately. Flowchart, sequence, ER, state, timeline and Gantt examples are starting points, not a fixed list of accepted diagrams. Enter any syntax supported by Mermaid Tiny 12.3.0. Render with the button or Ctrl/Cmd+Enter. Open `.mmd`, `.txt`, `.dot`, `.puml`, `.d2` or saved project JSON. Files stay in tab memory. No input is saved automatically.

**Save SVG** keeps a scalable static image. **Save PNG** makes a white-background image (dark for the Night theme) at up to 2× natural dimensions, capped at 4096 pixels per side. **Save source** exports the current editor text; **Save project** exports the last successfully rendered source and SVG. Importing a project ignores its SVG and loads only its validated editable source.

## Expand or customize

Edit `web/config.json`. For example, append a reusable template:

```json
{"id":"backup","name":"A backup path","code":"flowchart LR\n NAS --> Offsite\n NAS --> Snapshot"}
```

`templates` holds named starting points; `defaultTheme` is `default`, `neutral`, `dark` or `forest`. `maxCharacters` may lower the 15,000-character safety ceiling. `renderTimeoutSeconds` controls the waiting limit (5–60 seconds). `krokiEndpoint` can hold your HTTPS Kroki base URL, and `krokiTypes` controls the offered server languages. Any extra language must be enabled on that server. A normal push to `main` runs checks and publishes the configuration; no data refresh workflow or API key is needed.

Mermaid Tiny is pinned and bundled in `web/vendor/`. It does not contain mindmaps, architecture diagrams, KaTeX, ELK or lazy loading. To update it, obtain the official `@mermaid-js/tiny` npm package, replace the unmodified vendored script and licence, update its filename/version and provenance note, and run the tests and browser review. The build never downloads dependencies.

## Optional self-hosted Kroki

[Kroki](https://docs.kroki.io/kroki/setup/install/) supports Graphviz, PlantUML and additional diagram engines. Deploy its documented container setup on your own server, expose it through HTTPS, and allow the CoolCode browser origin with CORS. Set the endpoint in config or enter it in the app. No public demonstration endpoint is selected by default. The complete code is sent only after the visitor selects Kroki and checks permission; no cookies or credentials are sent. Server access controls and retention remain the operator's responsibility. Do not put private API keys in config.

## Security and privacy

Mermaid renders in a sandboxed iframe with an opaque origin and a restrictive CSP. The offline build gives the two packaged renderer scripts a new CSP nonce for each build, so they load without relying on same-origin privileges inside the sandbox. Diagram text never becomes part of this frame document or its script tags. Strict Mermaid security, disabled HTML labels, limits on source and edges, and disabled embedded configuration apply. Output is parsed as SVG, stripped of active elements, external URLs, event attributes and unsafe CSS, then displayed as an inert image. Export uses the cleaned SVG. Links and interactive diagram callbacks are intentionally unavailable. Failed renders preserve the previous result. The site’s shared metrics record aggregate opens, not diagram text.

## Sources and licence

- [Mermaid official documentation](https://mermaid.js.org/) and [MIT licence](web/vendor/LICENSE-MERMAID.txt), pinned Tiny 12.3.0.
- [Kroki HTTP API](https://docs.kroki.io/kroki/setup/usage/).
- Vendored dependency provenance and SHA-256 are in `web/vendor/README.md`; upstream bundled third-party notices are retained.

## Verify and publish

```sh
node --test tests/*.test.mjs
python3 -m unittest discover -s tests -v
python3 scripts/build.py
```

GitHub Actions also runs `tests/browser_smoke.py` at a project subpath, covering local rendering, syntax-error preservation, SVG/PNG export, custom code, project reopening and a 390-pixel layout. Only successful main builds deploy to GitHub Pages. No CNAME or server component is needed for local Mermaid use.
