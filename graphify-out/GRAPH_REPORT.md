# Graph Report - .  (2026-04-11)

## Corpus Check
- 3 files · ~3,813 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 12 nodes · 14 edges · 3 communities detected
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `main()` - 4 edges
2. `predict_risk_label()` - 3 edges
3. `load_artifacts()` - 2 edges
4. `build_raw_input()` - 2 edges
5. `align_input_frame()` - 2 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Communities

### Community 0 - "Community 0"
Cohesion: 0.6
Nodes (5): align_input_frame(), build_raw_input(), load_artifacts(), main(), predict_risk_label()

### Community 1 - "Community 1"
Cohesion: 0.4
Nodes (0): 

### Community 2 - "Community 2"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **Thin community `Community 2`** (1 nodes): `conftest.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Not enough signal to generate questions. This usually means the corpus has no AMBIGUOUS edges, no bridge nodes, no INFERRED relationships, and all communities are tightly cohesive. Add more files or run with --mode deep to extract richer edges._