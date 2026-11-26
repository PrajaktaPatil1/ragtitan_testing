# Machine Learning RAG Pipeline Evaluation Report

Generated: 2026-11-26T15:37:13+00:00

## Executive scorecard

**Overall: 55.1/100 - Needs Improvement**

**Assessment: Action Required** · **Measurement coverage: 76%**

Important weaknesses were found in the evaluated pipeline. One or more critical quality checks failed.

| Pipeline stage | Score / 100 | Rating | Measurement coverage |
|---|---:|---|---:|
| Document preparation | 87.8 | Very Good | 31% |
| Semantic indexing | 88.3 | Very Good | 86% |
| Information search | 56.9 | Needs Improvement | 100% |
| Search ordering | 37.9 | Poor | 100% |
| Answer context | 46.3 | Needs Improvement | 85% |
| Answer quality | 57.3 | Needs Improvement | 73% |
| User experience | 32.4 | Poor | 50% |

### Improvement priorities

- User experience: 32.4/100
  - The response differs from the reference answer's wording or details.
  - The generated answer does not exactly match the reference wording.
- Search ordering: 37.9/100
  - The most relevant chunks are not ranked high enough.
  - The reranker dropped or added candidates.
- Answer context: 46.3/100
  - The final prompt lacks information required for a complete answer.
  - Some required evidence did not reach the LLM.
- **Quality check:** Answer context: context sufficient is below the recommended minimum.

*Ratings apply only to the measured criteria on this test set. Measurement coverage is not statistical confidence. A high score is not a production certification.*

## Chunking (Document preparation)

| Metric | Value |
|---|---:|
| chunk_count | 1992 |
| total_source_tokens | 276323 |
| coverage | 1.0000 |
| overlap_ratio | 0.0306 |
| mean_chunk_tokens | 142.9548 |
| min_chunk_tokens | 24 |
| max_chunk_tokens | 229 |
| size_cv | 0.2124 |
| lexical_cohesion | 0.0775 |
| lexical_boundary_clarity | 0.7346 |
| lexical_chunk_stickiness | 0.1873 |
| semantic_chunk_stickiness | 0.7688 |

## Embedding (Semantic indexing)

| Metric | Value |
|---|---:|
| vector_count | 1992 |
| dimension | 768 |
| zero_norm_rate | 0.0000 |
| duplicate_vector_rate | 0.0000 |
| mean_vector_norm | 1.0000 |
| index_coverage | 1.0000 |
| query_topk_recall | 0.8000 |
| positive_similarity | 0.7379 |
| negative_similarity | 0.4726 |
| similarity_margin | 0.2653 |

## Retrieval (Information search)

| Metric | Value |
|---|---:|
| query_count | 10 |
| precision_at_k | 0.1800 |
| recall_at_k | 0.8000 |
| f1_at_k | 0.2905 |
| hit_at_k | 0.8000 |
| mrr_at_k | 0.5283 |
| ndcg_at_k | 0.5948 |
| average_precision_at_k | 0.5283 |
| token_recall | 0.8000 |
| token_precision | 0.0277 |
| token_iou | 0.0277 |
| complete_evidence_recall | 0.8000 |
| p50_latency_ms | 28.4050 |
| p95_latency_ms | 327.5156 |

## Reranking (Search ordering)

| Metric | Value |
|---|---:|
| query_count | 10 |
| ndcg_at_k | 0.4631 |
| ndcg_gain | -0.1318 |
| mrr_at_k | 0.4500 |
| mrr_gain | -0.0783 |
| precision_at_k | 0.1200 |
| precision_gain | -0.0600 |
| first_relevant_rank_change | 0.0000 |
| candidate_set_preservation_rate | 0.0000 |

## Augmentation (Answer context)

| Metric | Value |
|---|---:|
| query_count | 10 |
| context_precision | 0.0470 |
| context_recall | 0.5000 |
| context_noise | 0.9530 |
| context_sufficient | 0.5000 |
| duplicate_ratio | 0.0081 |
| evidence_edge_placement | 1.0000 |

## Generation (Answer quality)

| Metric | Value |
|---|---:|
| query_count | 10 |
| exact_match | 0.0000 |
| answer_precision | 0.3130 |
| answer_recall | 0.6431 |
| answer_f1 | 0.4045 |
| rouge_l_f1 | 0.3824 |
| required_fact_coverage | 0.5500 |
| citation_precision | 0.3500 |
| citation_recall | 0.5000 |
| citation_f1 | 0.4000 |
| abstention_accuracy | 1.0000 |
| context_grounding | 0.9445 |
| unsupported_number_rate | 0.0000 |
| p50_latency_ms | 2515.2205 |
| p95_latency_ms | 4693.2660 |

## End to end (User experience)

| Metric | Value |
|---|---:|
| query_count | 10 |
| answer_exact_match | 0.0000 |
| answer_f1 | 0.4045 |
| p50_latency_ms | 2542.1940 |
| p95_latency_ms | 4724.8917 |

## Queries to look at

- `q4` (retrieval): no relevant chunk in the top K
- `q8` (retrieval): no relevant chunk in the top K
- `q1` (augmentation): required evidence is missing from the context
- `q4` (augmentation): required evidence is missing from the context
- `q6` (augmentation): required evidence is missing from the context
- `q8` (augmentation): required evidence is missing from the context
- `q9` (augmentation): required evidence is missing from the context
- `q1` (generation): answer differs from the reference (F1 0.21)
- `q4` (generation): answer differs from the reference (F1 0.34)
- `q6` (generation): answer differs from the reference (F1 0.24)
- `q7` (generation): answer differs from the reference (F1 0.24)
- `q8` (generation): answer differs from the reference (F1 0.26)
- `q9` (generation): answer differs from the reference (F1 0.15)

## Diagnostic hints

First failing stage: **reranking**

- reranking / ndcg_gain = -0.13 (minimum -0.03): The reranker makes the order worse: check its model and the relevance labels.
- augmentation / context_sufficient = 0.50 (minimum 0.9): Pack all the supporting evidence into the context, within the budget.
- generation / answer_f1 = 0.40 (minimum 0.75): Compare the answers with the references: check the prompt and the LLM.
