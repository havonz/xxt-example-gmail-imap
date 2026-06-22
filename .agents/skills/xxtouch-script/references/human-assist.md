# XXTLanControl Human Assist Workflow

Use this slice when a script workflow needs user-provided samples: screenshots, stable color points, next-action tap points, rectangles, matrix dictionaries, or visual confirmation.

## Project Ledger

Store resumable assist state under `.tmp/xxtouch-ai/`: ledgers, screenshots, and generated snippets. Do not create separate AI config files for this workflow.

```text
.tmp/
└── xxtouch-ai/
    └── assist/
        └── camera-flow/
            ├── manifest.json
            └── screens/
                ├── page1-home.png
                └── page2-camera-icon.png
```

After creating it, ensure `.tmp/` is ignored by the XXTouch project config:

```bash
python3 scripts/ensure_config_ignores.py .
```

This adds `/.tmp` to `.config.ignores` and `.config.buildIgnores` when missing. Avoid deleting an active flow until its assist tasks have been consumed.

Minimal `manifest.json`:

```json
{
  "flowId": "camera-flow",
  "goal": "Build a screen-state automation flow",
  "steps": [
    {
      "stepId": "page2-camera-icon",
      "title": "Collect the second-page camera icon",
      "screenshot": ".tmp/xxtouch-ai/assist/camera-flow/screens/page2-camera-icon.png",
      "backendScreenshotPath": "assist/camera-flow/page2-camera-icon.png",
      "assistTaskIds": [],
      "why": "Need to identify this screen reliably and know the tap point for entering the next screen",
      "willUseFor": "Generate color match points for an XXTDo screen and run.tap",
      "status": "pending",
      "result": null
    }
  ]
}
```

Prefer the helper script to create the manifest and screenshot directory for a new flow; avoid hand-writing paths:

```bash
python3 scripts/init_assist_flow.py . --flow camera-flow --goal "Build a screen-state automation flow" \
  --step page2-camera-icon \
  --title "Collect the second-page camera icon" \
  --why "Need to identify this screen reliably and know the tap point for entering the next screen" \
  --will-use-for "Generate color match points for an XXTDo screen and run.tap" \
  --apply
```

Omit `--apply` when you only want to preview the manifest that would be written. To append a complex step to an existing flow, pass `--step-json` pointing to a step JSON file.

## Create Tasks

Create one assist task per screen or needed artifact. Put workflow metadata in `input` so the UI and later Agent runs can identify it.

Use XXTLanControl MCP assist tools when available: `xxt_assist_create_task`, `xxt_assist_list_tasks`, `xxt_assist_get_task`, `xxt_assist_wait_result`, and `xxt_assist_cancel_task`. Do not assume those tools are active in every session; if unavailable, ask the user for screenshots, points, rectangles, or matrix data.

```json
{
  "kind": "pick-colors",
  "title": "Collect color samples for the second-page camera icon",
  "prompt": "Collect several stable color points on the iOS Camera icon near the bottom center of the screenshot, and choose the tap point that enters the next screen.",
  "screenshotPath": "assist/camera-flow/page2-camera-icon.png",
  "input": {
    "flowId": "camera-flow",
    "stepId": "page2-camera-icon",
    "sequence": 2,
    "purpose": "Identify the second-page camera icon screen",
    "willUseFor": "Generate XXTDo screen: page2_camera_icon",
    "expected": {
      "stateColors": true,
      "actionPoint": true,
      "rectangles": ["icon"]
    }
  }
}
```

Store returned task IDs in `manifest.json`; do not rely on backend in-memory tasks as the only record.

## Submitted Result

The color picker can submit a `color-rule` result shaped like:

```json
{
  "kind": "color-rule",
  "points": [
    { "x": 100, "y": 200, "color": "AABBCC" }
  ],
  "records": [
    { "x": 120, "y": 220, "color": "112233" }
  ],
  "shiftRect": { "left": 90, "top": 180, "right": 150, "bottom": 240 },
  "metaRect": null,
  "snippets": {}
}
```

When the user asks the Agent to continue:

1. Read `manifest.json`.
2. For each pending task ID, call the assist-task get/list tool.
3. Copy submitted results into the matching manifest step with `scripts/merge_assist_result.py`.
4. Convert point results into Lua snippets with `scripts/assist_points_to_lua.py`.
5. Use the snippets to update the script or XXTDo screen table.

Merge a submitted assist task:

```bash
python3 scripts/merge_assist_result.py .tmp/xxtouch-ai/assist/camera-flow/manifest.json task.json --apply
```

If the task JSON does not contain `input.stepId`, pass `--step page2-camera-icon` explicitly.

## Convert Points

From a submitted task JSON:

```bash
python3 scripts/assist_points_to_lua.py task.json --format is-colors --similarity 92
```

From a workflow manifest step:

```bash
python3 scripts/assist_points_to_lua.py .tmp/xxtouch-ai/assist/camera-flow/manifest.json \
  --step page2-camera-icon \
  --format xxtdo-screen \
  --name page2_camera_icon \
  --tap 512,866
```

Output example:

```lua
{
    name = 'page2_camera_icon',
    csim = 92,
    {100, 200, 0xAABBCC},
    {120, 220, 0x112233},
    run = function()
        touch.tap(512, 866)
        sys.msleep(300)
    end,
}
```

If the submitted color result does not contain a dedicated `actionPoint`, pass the next-action tap with `--tap x,y`, or record it in the manifest as `result.actionPoint` before conversion.

## Convert Rectangles

Rectangle results are used for OCR, regional image matching, image cropping, or custom match regions. Prefer reading from `metaRect`; pass `--rect-key shiftRect` when another rectangle is needed.

```bash
python3 scripts/assist_rect_to_lua.py .tmp/xxtouch-ai/assist/camera-flow/manifest.json \
  --step page2-camera-icon \
  --rect-key metaRect \
  --format ocr \
  --engine zh-Hans
```

Common formats:

- `--format args` outputs `left, top, right, bottom` arguments.
- `--format table` outputs a Lua region table.
- `--format find-image --image-var tpl` outputs a regional `screen.find_image` call.
- `--format crop --image-var img --output-var cropped` outputs an `ImageObject:crop` call.

## Convert Matrix Dictionaries

Matrix dictionary tasks submit `matrixLines`, `currentLine`, `colorRange`, `word`, `shiftRect`, and `metaRect`. The converter validates the `$` segments in matrix lines.

```bash
python3 scripts/assist_matrix_to_lua.py .tmp/xxtouch-ai/assist/camera-flow/manifest.json \
  --step title-text \
  --format find-matrix
```

Common formats:

- `--format load-dict` outputs `dm.LoadDict` and `dm.UseDict`.
- `--format find-matrix` outputs a temporary matrix lookup with `dm.FindMatrix`.
- `--format find-str --word "Confirm"` outputs a text-search snippet with `dm.FindStr`.
- `--format ocr` outputs a `dm.Ocr` snippet.

If the input is plain matrix-line text, you can pass the file path directly instead of wrapping it as JSON.

## Render Flow

Multiple completed color-picking steps can be rendered into a flow skeleton:

```bash
python3 scripts/render_flow.py .tmp/xxtouch-ai/assist/camera-flow/manifest.json --mode xxtdo
```

For plain XXTouch scripts that do not use XXTDo:

```bash
python3 scripts/render_flow.py .tmp/xxtouch-ai/assist/camera-flow/manifest.json --mode plain
```

The renderer only uses steps whose status is `submitted`, `completed`, `done`, or `consumed` and that contain `result`. Repeat `--step step-id` when you need to limit the rendered steps.

## Clean Workspace

Clean completed assist screenshots only after submitted results are copied into the manifest. Always preview first:

```bash
python3 scripts/clean_assist_workspace.py .
```

Apply the cleanup only when the preview lists the intended files:

```bash
python3 scripts/clean_assist_workspace.py . --apply
```

The cleaner only removes local screenshot files under `.tmp/xxtouch-ai/assist/` that are referenced by `manifest.json` steps with completed statuses and non-null `result`. It does not delete backend `screenshotPath` files.

## Agent Rules

- Use `.tmp/xxtouch-ai/` as the only project-local AI assist state root.
- Do not create separate AI config files for this workflow.
- Use `scripts/init_assist_flow.py` to create new flow manifests when possible.
- Use `scripts/merge_assist_result.py` to record submitted task results before generating code.
- Use `scripts/ensure_config_ignores.py` instead of hand-editing `.config.ignores` or `.config.buildIgnores`.
- Create `.tmp/xxtouch-ai/assist/<flowId>/manifest.json` before creating the first task for a workflow.
- Every assist task must have `flowId`, `stepId`, `purpose` or `why`, and `willUseFor`.
- Save screenshots before creating tasks, then record both local and backend screenshot paths.
- Prefer one screen state per manifest step.
- For XXTDo projects, turn submitted screen samples into `group`/color points and put the next action in `run`.
- For plain XXTouch projects, convert samples into `screen.is_colors` checks plus explicit `touch.tap` actions.
- Use `scripts/render_flow.py` when a manifest contains multiple completed screen-state steps.
- Use `scripts/clean_assist_workspace.py` for local screenshot cleanup; never manually delete active pending assist screenshots.
- If the result lacks enough stable points or a needed action point, create another assist task instead of guessing.
