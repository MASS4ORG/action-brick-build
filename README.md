# Brick build action

Verify and pack a brick, then install and compile its source and optional twin in fresh consumer projects. This action has no publishing credentials and does not upload to a registry.

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
      - uses: MASS4ORG/action-brick-build@v1
```

For push/PR verification with optional source tests, use the [reusable verify workflow](https://github.com/MASS4ORG/action-brick-release). For MASS4 store publication, use its release workflow. For your own registry, upload this action's output archives through your own pipeline.

| Input | Default | Purpose |
|---|---|---|
| `brick-path` | `.` | Brick folder |
| `precast` | `true` | Compile runtime assemblies |
| `twin` | `false` | Also produce the baked variant |
| `consumer-test` | `true` | Install, compile and cold-restore each archive |
| `version` | Empty | Highest stable semver CLI image tag; exact stable version override supported |
| `image` | Empty | Exact CLI image supplied by an orchestrating workflow |
| `release-tag` | Empty | Inject the tag's semver into the packed manifest; warn on manifest drift |
| `out` | Runner temp folder | Archive output directory outside the brick |

Outputs are `image`, `version`, `directory`, `archive` and `twin-archive`. `build.json` records the resolved CLI digest/version and archive hashes. No Docker `latest` tag is used. A manifest already matching `release-tag` is preserved byte-for-byte for retry reproducibility.

`@v1` follows compatible implementation updates. Breaking inputs use a new major version; Turian releases do not require action releases.
