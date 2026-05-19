# PATCH_NOTES.md — How to apply the v1.3 overlay

This bundle is an overlay, not a destructive rewrite. It adds v1.3 files and can replace the root README if you approve the new examples.

From the root of `agisota/wu-wei-skill`:

```bash
mkdir -p skill/references skill/evals docs
cp /path/to/bundle/README.md README.md
cp /path/to/bundle/skill/system_prompt_v1.3.md skill/system_prompt_v1.3.md
cp /path/to/bundle/skill/references/anti_slop.md skill/references/anti_slop.md
cp /path/to/bundle/skill/references/ru_style_guide.md skill/references/ru_style_guide.md
cp /path/to/bundle/skill/references/refusal_conditions_v2.md skill/references/refusal_conditions_v2.md
cp /path/to/bundle/skill/references/mode_matrix.md skill/references/mode_matrix.md
cp /path/to/bundle/skill/evals/golden_set_ru.jsonl skill/evals/golden_set_ru.jsonl
cp /path/to/bundle/skill/evals/grader_prompt_v2.md skill/evals/grader_prompt_v2.md
cp /path/to/bundle/skill/evals/regression_checklist.md skill/evals/regression_checklist.md
cp /path/to/bundle/docs/examples_v2.md docs/examples_v2.md
```

Recommended minimal `skill/SKILL.md` updates:

```diff
- Load `system_prompt_v1.2.md` and run Diagnose → Test → Rewrite → Kill → Frame Log → Deliver.
+ Load `system_prompt_v1.3.md` and run Diagnose → Test → Rewrite → Kill → Repair/Object → Deliver.

- output_mode: `full | quick | frame_log_only` — default `full`
+ output_mode: `compact | decision | frame_log | critique_only` — default `compact`
+ aliases: `quick=compact`, `full=decision`, `frame_log_only=frame_log`

- Schema headers stay English even when the rewrite itself is Russian, Chinese, or another language.
+ Schema headers default to the artifact language unless `strict_schema=true`.

+ Read `references/anti_slop.md` for language-integrity checks.
+ Read `references/ru_style_guide.md` for Russian output.
+ Read `references/refusal_conditions_v2.md` when a repair-first structural objection may be needed.
```

Recommended eval runner update:

```diff
- skill/evals/grader_prompt.md
+ skill/evals/grader_prompt_v2.md
```

Optional regression run:

```bash
bash skill/scripts/run_evals.sh --dry-run --limit 5
bash skill/scripts/run_evals.sh --case gs_ru_v2_001
bash skill/scripts/run_evals.sh --type pitch
```
