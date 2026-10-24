# Turian brick build action

Verify, compile and pack a [Turian](https://github.com/MASS4ORG/Turian) brick into `.brick` archives, optionally with its baked twin, then install each archive in a fresh project as a user would. It needs no secrets and talks to no store, so it suits anyone building bricks for their own registry. It runs the `ghcr.io/mass4org/turian-cli` container and needs a Linux runner with Docker.

## Usage

```yaml
jobs:
  brick:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7

      - id: build
        uses: MASS4ORG/action-brick-build@v1
        with:
          twin: true

      - uses: actions/upload-artifact@v7
        with:
          name: brick
          path: ${{ steps.build.outputs.directory }}
```

## Inputs

| Input           | Default  | Description                                                                                       |
|-----------------|----------|---------------------------------------------------------------------------------------------------|
| `brick-path`    | `.`      | Folder of the brick, holding `package.json`                                                       |
| `precast`       | `true`   | Compile the brick's assemblies into the archive, which also proves they build                     |
| `twin`          | `false`  | Also bake the brick and pack its twin, a variant of the same id and version                       |
| `consumer-test` | `true`   | Install, compile and cold-restore each archive in a fresh project; needs turian-cli 3.3.0 or later |
| `version`       | `latest` | Tag of `ghcr.io/mass4org/turian-cli` to build with                                                |
| `image`         |          | Full image reference instead, e.g. one pinned by digest                                           |
| `out`           |          | Folder for the archives, outside the brick; empty for one under the runner's temp folder          |

## Outputs

| Output         | Description                                          |
|----------------|------------------------------------------------------|
| `directory`    | Absolute path of the folder holding the archives     |
| `archive`      | File name of the brick's archive                     |
| `twin-archive` | File name of the twin's archive; empty without twin  |

Archives are named `<id>-<version>--<variant>.brick`, but the name is only a label: each one is classified by its own `package.json`, where a twin declares `bakeOf`.
| `image`        | The image that built them, pinned by digest          |
| `version`      | The Turian version of that image                     |

## Reproducing a build

`latest` is resolved to a digest once, and every command runs that digest. `build.json`, written beside the archives, records it with each archive's SHA-256:

```json
{
  "turian": { "version": "3.3.0", "image": "ghcr.io/mass4org/turian-cli@sha256:…" },
  "archives": [ { "file": "org.example.brick-1.0.0.brick", "sha256": "…" } ]
}
```

Pass that image as `image` to build again with exactly the same CLI. Archives are byte-identical only when built by the same image.

## License

[MIT](LICENSE.md)
