# Graph Report - .  (2026-04-11)

## Corpus Check
- 3 files · ~4,202 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 16 nodes · 21 edges · 4 communities detected
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `main()` - 6 edges
2. `render_hero()` - 3 edges
3. `predict_risk_label()` - 3 edges
4. `load_artifacts()` - 2 edges
5. `build_metric_items()` - 2 edges
6. `inject_styles()` - 2 edges
7. `build_raw_input()` - 2 edges
8. `align_input_frame()` - 2 edges

## Surprising Connections (you probably didn't know these)
- `main()` --calls--> `predict_risk_label()`  [EXTRACTED]
  app.py → app.py  _Bridges community 2 → community 0_

## Communities

### Community 0 - "Community 0"
Cohesion: 0.52
Nodes (6): build_metric_items(), build_raw_input(), inject_styles(), load_artifacts(), main(), render_hero()

### Community 1 - "Community 1"
Cohesion: 0.33
Nodes (0): 

### Community 2 - "Community 2"
Cohesion: 1.0
Nodes (2): align_input_frame(), predict_risk_label()

### Community 3 - "Community 3"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **Thin community `Community 2`** (2 nodes): `align_input_frame()`, `predict_risk_label()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 3`** (1 nodes): `conftest.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `main()` connect `Community 0` to `Community 2`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **Why does `predict_risk_label()` connect `Community 2` to `Community 0`?**
  _High betweenness centrality (0.005) - this node is a cross-community bridge._