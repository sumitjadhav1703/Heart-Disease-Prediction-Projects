# Graph Report - .  (2026-04-12)

## Corpus Check
- 3 files · ~4,446 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 22 nodes · 31 edges · 6 communities detected
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `main()` - 9 edges
2. `render_hero()` - 3 edges
3. `predict_risk_label()` - 3 edges
4. `render_result_card()` - 3 edges
5. `load_artifacts()` - 2 edges
6. `build_metric_items()` - 2 edges
7. `inject_styles()` - 2 edges
8. `render_prediction_form()` - 2 edges
9. `render_info_panel()` - 2 edges
10. `build_raw_input()` - 2 edges

## Surprising Connections (you probably didn't know these)
- `main()` --calls--> `render_hero()`  [EXTRACTED]
  app.py → app.py  _Bridges community 3 → community 1_
- `main()` --calls--> `predict_risk_label()`  [EXTRACTED]
  app.py → app.py  _Bridges community 2 → community 1_
- `main()` --calls--> `render_result_card()`  [EXTRACTED]
  app.py → app.py  _Bridges community 4 → community 1_

## Communities

### Community 0 - "Community 0"
Cohesion: 0.25
Nodes (0): 

### Community 1 - "Community 1"
Cohesion: 0.52
Nodes (6): build_raw_input(), inject_styles(), load_artifacts(), main(), render_info_panel(), render_prediction_form()

### Community 2 - "Community 2"
Cohesion: 1.0
Nodes (2): align_input_frame(), predict_risk_label()

### Community 3 - "Community 3"
Cohesion: 1.0
Nodes (2): build_metric_items(), render_hero()

### Community 4 - "Community 4"
Cohesion: 1.0
Nodes (2): build_result_theme(), render_result_card()

### Community 5 - "Community 5"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **Thin community `Community 2`** (2 nodes): `align_input_frame()`, `predict_risk_label()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 3`** (2 nodes): `build_metric_items()`, `render_hero()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 4`** (2 nodes): `build_result_theme()`, `render_result_card()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 5`** (1 nodes): `conftest.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `main()` connect `Community 1` to `Community 2`, `Community 3`, `Community 4`?**
  _High betweenness centrality (0.067) - this node is a cross-community bridge._
- **Why does `render_hero()` connect `Community 3` to `Community 1`?**
  _High betweenness centrality (0.002) - this node is a cross-community bridge._
- **Why does `predict_risk_label()` connect `Community 2` to `Community 1`?**
  _High betweenness centrality (0.002) - this node is a cross-community bridge._