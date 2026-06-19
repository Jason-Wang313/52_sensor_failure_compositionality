# Paper 52 VLA Highlight Hardening Plan

Objective: make Paper 52's boxed PDF highlights match the VLA-v4 role-model PDF while preserving the final OrderComp evidence, page count, and scientific claims.

## Role-Model Target

- Citation links use green rectangular borders with no fill.
- Internal references use red rectangular borders with no fill.
- URL links use the same green border family as citations.
- Border width is `pdfborder={0 0 1}`, matching the VLA-v4 annotation metadata.
- Boxes remain tight to linked text and must not change typography, spacing, captions, result tables, figures, or scientific wording.

## Current Paper 52 Mismatch

- `Downloads/52.pdf` has link annotations on pages 2, 4, 5, 6, 7, and 24.
- Annotation colors are already red/green, but every link has border width `0`.
- `paper/main.tex` uses `\hypersetup{hidelinks}`, so the link boxes are invisible and do not match the VLA-v4 role model.

## Execution Plan

1. Keep RAM use low by rendering only affected pages before and after the edit: pages 2, 4, 5, 6, 7, and 24.
2. Replace `\hypersetup{hidelinks}` in `paper/main.tex` with explicit VLA-style link annotation settings:
   - `colorlinks=false`
   - `pdfborder={0 0 1}`
   - `citebordercolor={0 1 0}`
   - `linkbordercolor={1 0 0}`
   - `urlbordercolor={0 1 0}`
3. Rebuild with `scripts/build_pdf.ps1`, which exports the canonical final PDF to `C:\Users\wangz\Downloads\52.pdf`, writes build metadata, and removes local `paper/main.pdf`.
4. Validate the rebuilt PDF annotation metadata with `pypdf`.
5. Render pages 2, 4, 5, 6, 7, and 24 again and visually compare with the VLA-v4 role model.
6. Update child/build metadata and SHA text if present.
7. Remove Paper 52 temporary render folders, then commit and push the clean repo.

## Non-Goals

- Do not rerun the full-scale experiment.
- Do not change tables, figures, page count target, benchmark claims, or scientific results.
- Do not pad the paper or alter the final manuscript content beyond the link-box styling.
