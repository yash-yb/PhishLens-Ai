# Graph Report - PhishLens-Ai  (2026-05-02)

## Corpus Check
- 13 files · ~8,270 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 33 nodes · 24 edges · 3 communities detected
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 2 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]

## God Nodes (most connected - your core abstractions)
1. `PhishLensClassifier` - 6 edges
2. `PhishLensOCR` - 5 edges
3. `DetectionResult` - 4 edges
4. `Load the model and vectorizer from disk if they exist.` - 1 edges
5. `Predict the risk score based on the text content.         Returns a probability` - 1 edges
6. `Preprocess image to improve OCR accuracy and performance` - 1 edges
7. `Extract text and bounding boxes from image` - 1 edges

## Surprising Connections (you probably didn't know these)
- `DetectionResult` --uses--> `PhishLensClassifier`  [INFERRED]
  ml-service\main.py → ml-service\classifier.py
- `DetectionResult` --uses--> `PhishLensOCR`  [INFERRED]
  ml-service\main.py → ml-service\ocr_engine.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.29
Nodes (3): PhishLensClassifier, Load the model and vectorizer from disk if they exist., Predict the risk score based on the text content.         Returns a probability

### Community 1 - "Community 1"
Cohesion: 0.33
Nodes (3): PhishLensOCR, Preprocess image to improve OCR accuracy and performance, Extract text and bounding boxes from image

### Community 2 - "Community 2"
Cohesion: 0.4
Nodes (2): BaseModel, DetectionResult

## Knowledge Gaps
- **4 isolated node(s):** `Load the model and vectorizer from disk if they exist.`, `Predict the risk score based on the text content.         Returns a probability`, `Preprocess image to improve OCR accuracy and performance`, `Extract text and bounding boxes from image`
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 2`** (5 nodes): `BaseModel`, `analyze_image()`, `DetectionResult`, `main.py`, `read_root()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DetectionResult` connect `Community 2` to `Community 0`, `Community 1`?**
  _High betweenness centrality (0.240) - this node is a cross-community bridge._
- **Why does `PhishLensClassifier` connect `Community 0` to `Community 2`?**
  _High betweenness centrality (0.204) - this node is a cross-community bridge._
- **Why does `PhishLensOCR` connect `Community 1` to `Community 2`?**
  _High betweenness centrality (0.175) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `DetectionResult` (e.g. with `PhishLensOCR` and `PhishLensClassifier`) actually correct?**
  _`DetectionResult` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Load the model and vectorizer from disk if they exist.`, `Predict the risk score based on the text content.         Returns a probability`, `Preprocess image to improve OCR accuracy and performance` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._