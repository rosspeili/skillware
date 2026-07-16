# Background Remover

Use this skill when a user asks to remove an image background, create a transparent PNG, cut out a product or person, isolate a subject, or prepare an image for design or e-commerce workflows.

Trigger phrases include: "remove background", "transparent background", "cut out", "isolate product/person", "PNG with alpha", "no background".

Do **not** use this skill for:

- videos or animated media
- batch folders or bulk directory processing
- cloud-only editing workflows with no local image bytes available

## Before calling the skill

If the user wants background removal but has **not** provided an image, file path, or attachment, **ask** for one first. Do not call the skill until input exists.

The skill does **not** fetch URLs. When the user provides an `https://…` image link, download it to a temp file first, then pass `input_path`.

For S3, GCS, Azure Blob, or Cloudflare R2, the host agent or SDK downloads the object to a temp file, calls the skill with `input_path`, then uploads from `output_path` after success. The skill stays local-only; catalog recipes are templates.

## Input choice (one required: `image` OR `input_path`)

| Scenario | Agent should use |
| :--- | :--- |
| User uploaded or pasted an image in chat | `image` (base64 from host encoding) |
| User gave a local path (e.g. `D:\photos\cat.png`) | `input_path` (absolute path preferred on Windows) |
| User gave a URL | Download to temp file, then `input_path` |
| Cloud object storage | Download object → temp file → `input_path` |

If **both** `image` and `input_path` are sent, **`image` wins** (do not double-submit).

## Output behavior

| Scenario | Agent should use |
| :--- | :--- |
| User wants a file on disk | Set `output_path`. Prefer `{same_dir}/{stem}_no_bg.png` unless the user specifies a path. Do **not** overwrite the source file unless asked. |
| Chat or API only (no disk write) | Omit `output_path`; use `image_base64` from the result (always returned on success). |
| User said "save next to the original" | Same directory, new name (e.g. `1223_no_bg.png`). |

## Dependencies

Runtime packages: `rembg`, `pillow`, `onnxruntime`. Install with `pip install "skillware[creative_bg_remover]"` or the category extra `skillware[creative]`.

The **first** `execute()` downloads the selected ONNX model (~176 MB for `isnet-general-use`) to the rembg cache (`~/.u2net/` on Linux/macOS, `%USERPROFILE%\.u2net\` on Windows). Later runs are offline and much faster.

## Error handling

| `error_code` | Agent action |
| :--- | :--- |
| `INVALID_INPUT` | Ask for an image upload, base64 payload, or local `input_path`. |
| `MISSING_DEPENDENCY` | Tell the user to run `pip install "skillware[creative_bg_remover]"` (or `pip install rembg pillow onnxruntime`). |
| `PROCESSING_FAILED` | Report the `error` string; the file may be corrupt or an unsupported format. |

This skill processes still images locally using `rembg` and returns PNG output with transparency.
