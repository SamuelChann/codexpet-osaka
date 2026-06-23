# Osaka Codex Nine-Row Animation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the Osaka pet as a Codex-compatible 8×9 spritesheet whose nine rows match the host animation states and interactions.

**Architecture:** Make the nine-row layout the single source of truth in the manifest, frame composer, atlas builder, validator, previews, and package. Reuse approved Osaka poses where their semantics match; generate four new key poses for directional dragging, jumping, and waiting, then derive stable frame sequences deterministically.

**Tech Stack:** Python 3, Pillow, unittest, Codex image generation, WebP/RGBA asset pipeline, Git.

---

### Task 1: Lock the nine-row protocol with failing tests

**Files:**
- Modify: `osaka_pet/tests/test_asset_pipeline.py`
- Test: `osaka_pet/tests/test_asset_pipeline.py`

- [ ] Add tests asserting the exact state order, frame ranges, used-frame counts `6,8,8,4,5,8,6,6,6`, transparent unused cells, and removal of legacy runtime states.
- [ ] Run `python -m unittest discover -s osaka_pet/tests -v` and verify the new tests fail because the manifest still defines eleven sequential states and all cells are visible.
- [ ] Commit only the failing tests with `git add osaka_pet/tests/test_asset_pipeline.py && git commit -m "test: define Codex nine-row animation contract"`.

### Task 2: Convert the manifest and validator to the nine-row contract

**Files:**
- Modify: `osaka_pet/osaka_pet.animations.json`
- Modify: `osaka_pet/tools/validate_assets.py`
- Modify: `osaka_pet/tests/test_asset_pipeline.py`

- [ ] Replace the animation keys with `idle`, `running-right`, `running-left`, `waving`, `jumping`, `failed`, `waiting`, `running`, and `review` in row order.
- [ ] Assign row-local frame lists: `0–5`, `8–15`, `16–23`, `24–27`, `32–36`, `40–47`, `48–53`, `56–61`, `64–69`.
- [ ] Define validator constants for row index, used-frame count, and transparent cells; validate that visible frames stay within their state row and unused cells are fully transparent.
- [ ] Change frame coverage validation from “all 72 referenced once” to “all used cells referenced once and all remaining cells transparent.”
- [ ] Run the focused tests and verify manifest-shape tests pass while transparent-cell tests still fail against old frames.
- [ ] Commit with `git add osaka_pet/osaka_pet.animations.json osaka_pet/tools/validate_assets.py osaka_pet/tests/test_asset_pipeline.py && git commit -m "feat: enforce Codex nine-row animation layout"`.

### Task 3: Generate missing Osaka key poses

**Files:**
- Create: `osaka_pet/keyposes/running-right.png`
- Create: `osaka_pet/keyposes/running-left.png`
- Create: `osaka_pet/keyposes/jumping.png`
- Create: `osaka_pet/keyposes/waiting.png`
- Modify: `osaka_pet/prompts/generation.md`

- [ ] Add four prompts that repeat the master identity invariants and specify: right-drag lag, left-drag lag, delayed surprised hop, and attentive confused waiting.
- [ ] Generate each key pose using both `osaka.png` and `osaka_pet/reference/osaka_pet_master.png` as references.
- [ ] Remove chroma-key backgrounds with soft matte and despill, preserving RGBA transparency.
- [ ] Visually inspect each pose for Osaka identity, uniform consistency, limb integrity, generous padding, correct direction, and absence of text or extra characters.
- [ ] Commit the prompts and approved key poses with `git add osaka_pet/prompts/generation.md osaka_pet/keyposes/running-right.png osaka_pet/keyposes/running-left.png osaka_pet/keyposes/jumping.png osaka_pet/keyposes/waiting.png && git commit -m "feat: add missing Codex animation key poses"`.

### Task 4: Rebuild deterministic frame composition by row

**Files:**
- Modify: `osaka_pet/tools/create_frames.py`
- Modify: `osaka_pet/tests/test_asset_pipeline.py`
- Replace: `osaka_pet/frames/000.png` through `osaka_pet/frames/071.png`

- [ ] Update `_load_fitted` to load the four new poses and retain only runtime pose dependencies plus the master reference.
- [ ] Replace the sequential eleven-state recipes with nine lists of eight cells each; emit transparent canvases for unused cells.
- [ ] Compose directional drag rows from their own key poses, with horizontal lag and gentle alternating rotation; compose jumping with anticipation, lift, apex hold, landing compression, and recovery.
- [ ] Compose waiting from master-to-waiting transition and a subtle held head tilt; map happy, cry, study, and shy to waving, failed, running, and review.
- [ ] Run the focused tests, verify they pass, then run the whole unittest suite.
- [ ] Commit the composer and generated frames with `git add osaka_pet/tools/create_frames.py osaka_pet/tests/test_asset_pipeline.py osaka_pet/frames && git commit -m "feat: compose Osaka animations by Codex state row"`.

### Task 5: Build atlas, previews, and runtime package

**Files:**
- Modify: `osaka_pet/tools/build_atlas.py`
- Replace: `osaka_pet/osaka_pet_atlas.png`
- Replace/create: `osaka_pet/previews/*.webp`
- Replace: `osaka_pet/package/spritesheet.webp`

- [ ] Update preview generation to skip transparent cells automatically and create one preview per nine-row state.
- [ ] Run `python osaka_pet/tools/create_frames.py`.
- [ ] Run `python osaka_pet/tools/build_atlas.py`.
- [ ] Encode the PNG atlas as lossless RGBA WebP at exactly 1536×1872 into `osaka_pet/package/spritesheet.webp`.
- [ ] Run `python osaka_pet/tools/validate_assets.py` and verify zero errors.
- [ ] Commit with `git add osaka_pet/tools/build_atlas.py osaka_pet/osaka_pet_atlas.png osaka_pet/previews osaka_pet/package/spritesheet.webp && git commit -m "build: package Codex-compatible Osaka spritesheet"`.

### Task 6: Update documentation and validation report

**Files:**
- Modify: `osaka_pet/START_HERE.md`
- Modify: `osaka_pet/WORKFLOW.md`
- Modify: `osaka_pet/VALIDATION_REPORT.md`
- Create: `osaka_pet/contact-sheet.png`

- [ ] Replace the legacy eleven-state mapping with the official nine-row table and document transparent unused cells.
- [ ] Record which source poses were reused and which four were generated.
- [ ] Generate a labeled contact sheet showing row name, all eight cells, and used-frame count.
- [ ] Run `rg -n "happy|shy|cry|surprised|clicked|drag|sleep|study|thinking|eating" osaka_pet/START_HERE.md osaka_pet/WORKFLOW.md osaka_pet/VALIDATION_REPORT.md` and ensure legacy names remain only in explicit source-material notes.
- [ ] Commit with `git add osaka_pet/START_HERE.md osaka_pet/WORKFLOW.md osaka_pet/VALIDATION_REPORT.md osaka_pet/contact-sheet.png && git commit -m "docs: document Osaka nine-row animation package"`.

### Task 7: Verify and install the package

**Files:**
- Verify: `osaka_pet/package/pet.json`
- Verify: `osaka_pet/package/spritesheet.webp`
- Update installed copies: `%USERPROFILE%/.codex/pets/osaka/pet.json`, `%USERPROFILE%/.codex/pets/osaka/spritesheet.webp`

- [ ] Run `python -m unittest discover -s osaka_pet/tests -v` and require all tests to pass without warnings.
- [ ] Run `python osaka_pet/tools/validate_assets.py` and require the success message.
- [ ] Inspect the final WebP for RGBA mode, 1536×1872 size, transparent unused cells, and zero transparent-RGB residue.
- [ ] Copy only `pet.json` and `spritesheet.webp` into the installed Osaka pet directory.
- [ ] Verify installed files byte-for-byte match the package files.
- [ ] Exercise idle, left/right drag, click, running task, waiting input, failed task, and completed-review states in Codex; record results in `osaka_pet/VALIDATION_REPORT.md`.
- [ ] Commit any final report update with `git add osaka_pet/VALIDATION_REPORT.md && git commit -m "test: verify installed Osaka pet interactions"`.
- [ ] Confirm `git status --short` lists only the pre-existing untracked `can_write_test_osaka.txt`.
