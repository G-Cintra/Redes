# AGENTS.md

## Purpose of this repository

This is an academic Python project intended to support master's-level research.

The repository will be made public and shared with academic reviewers. The primary goal is therefore not production-grade software architecture, but a correct, reproducible, transparent, and easy-to-audit implementation of the analysis.

A technically competent reader should be able to understand what the project does without having to reverse-engineer the software structure.

## Priorities

When making any change, use this priority order:

1. Correctness.
2. Methodological transparency.
3. Readability and auditability.
4. Reproducibility.
5. Simplicity.
6. Maintainability.
7. Generality and extensibility.

Do not sacrifice the first five priorities for software-engineering sophistication.

## Core principle

Use the simplest structure that makes the analysis easier to understand.

Do not confuse simplicity with putting everything into one file.

The project should have enough structure to separate genuine analytical concepts, but no more structure than necessary.

Prefer a few clear modules corresponding directly to concepts in the analysis over many small architectural components.

## Notebook as the main entry point

The main analysis notebook should be the easiest way for a reviewer to understand the project.

It should present the analytical workflow in a clear sequence, such as:

data/input
→ cleaning or transformation
→ construction of analytical objects
→ calculations
→ results
→ figures/tables

Important methodological decisions must remain visible in the notebook.

Do not turn the notebook into a thin interface that hides the entire analysis behind calls such as:

```python
pipeline.run()
analysis.execute()
manager.process()
```

A reader should be able to follow the notebook and understand what each major step is doing.

## Python modules

Move code into Python modules when doing so improves readability, especially when the code:

* is reused;
* implements a clearly identifiable methodological calculation;
* is long enough to interrupt the notebook narrative;
* benefits from independent testing;
* or represents a genuine concept in the analysis.

Module names should normally describe analytical concepts.

Examples of reasonable names, depending on the project:

* `data.py`
* `network.py`
* `centrality.py`
* `metrics.py`
* `visualization.py`

Do not introduce generic architecture without a concrete need.

Avoid files or concepts such as:

* `services.py`
* `controllers.py`
* `managers.py`
* `factories.py`
* `interfaces.py`
* `adapters.py`
* generic `pipeline.py`
* generic `utils.py`

unless there is a clear and unavoidable project-specific reason.

## Functions and classes

Prefer small, explicit functions.

A function should normally perform one recognizable analytical operation.

Prefer:

```python
degree = adjacency.sum(axis=1)
```

over abstractions that obscure the mathematical operation.

Do not create:

* wrapper functions that add no meaningful behavior;
* helper functions used only once when inline code is clearer;
* classes that exist only to group a few functions;
* dataclasses whose only purpose is to move a few values around;
* abstract base classes;
* plugin architectures;
* factories;
* registries;
* dependency injection;
* generalized frameworks for hypothetical future requirements.

Use classes only when the problem genuinely has state or behavior that is clearer when represented as an object.

## Academic transparency

The implementation should make it easy to compare the code with the underlying methodology.

Where appropriate:

* use variable names that correspond to mathematical or methodological concepts;
* include equations or short methodological explanations in the notebook;
* keep important assumptions explicit;
* keep transformations inspectable;
* avoid clever one-liners when a few straightforward lines are easier to verify.

Do not hide important calculations inside generic abstractions.

A little repetition is acceptable when removing it would make the methodology harder to follow.

## Scope discipline

When asked to make a change:

* change only what is necessary for that task;
* do not redesign unrelated parts of the repository;
* do not add speculative features;
* do not prepare infrastructure for hypothetical future requirements;
* do not introduce new dependencies unless they provide a clear benefit;
* do not create new files unless they improve the conceptual organization of the project.

Do not perform broad "cleanup" unless explicitly requested.

## Simplification rule

Before adding any new:

* file;
* class;
* abstraction;
* dependency;
* configuration layer;
* helper layer;
* compatibility layer;

ask:

> Does this make the current academic analysis easier to understand, verify, or reproduce?

If not, do not add it.

When two solutions are both correct, prefer the one requiring the reader to understand fewer concepts.

## Refactoring

When refactoring existing code:

1. Preserve numerical and analytical results unless a correction is explicitly required.
2. Prefer deleting unnecessary code over reorganizing it.
3. Prefer merging artificial layers over renaming them.
4. Do not replace one abstraction with another abstraction of similar complexity.
5. Do not rewrite working code solely to make it stylistically different.
6. Keep changes small enough to review.

If simplification would alter methodology or results, stop and explain the issue rather than silently changing it.

## Dependencies

Prefer:

1. Python standard library;
2. established scientific Python packages already used by the project;
3. new dependencies only when they substantially simplify or improve the analysis.

Do not add a package to save a few lines of straightforward Python.

## Testing and validation

Tests should focus on calculations where an unnoticed mistake could affect the research results.

Prioritize tests for:

* mathematical calculations;
* transformations;
* network construction;
* metrics;
* indexing/alignment;
* edge cases that could materially change results.

Do not create large amounts of testing infrastructure for trivial getters, wrappers, or implementation details.

Whenever analytical code is changed, run the relevant tests and, when practical, verify that key outputs remain unchanged.

## Comments and documentation

Comments should explain:

* why something is done;
* methodological assumptions;
* non-obvious transformations;
* potential sources of error.

Do not comment obvious Python syntax.

The README should explain how to reproduce the analysis and identify the main notebook.

Do not duplicate extensive documentation across multiple files.

## Before finishing a task

Before considering a task complete, check:

* Is the code easier to understand than before?
* Can the main analytical path still be followed from the notebook?
* Did I introduce any unnecessary abstraction?
* Did I add files that could reasonably be avoided?
* Are important calculations still visible and auditable?
* Did I preserve existing results unless intentionally correcting them?
* Did I run the relevant validation or tests?
* Is there any obsolete code that should be removed because of this change?

If a change makes the repository larger or conceptually more complicated, there should be a clear analytical reason for it.
