# Database Optimization Agent – Relationship & Index Notes

## Relationship Mapping Summary
- `recipes` (`services/backend/Database/Models/recipes.py`): self-referential `origin_recipe_id` clones a recipe for batches but no parent-side `derived_recipes` collection or cascade. Collections for hops, fermentables, yeasts, miscs, and batches align with ingredient/inventory usage.
- `batches` (`services/backend/Database/Models/batches.py`) ⇄ `batch_logs` (`services/backend/Database/Models/batch_logs.py`): intended 1↔1 via `batch_log`/`batch`, yet `batch_logs.batch_id` is nullable; neither side enforces cascades.
- Inventory links: each `Inventory*` table (`inventory_fermentables`, `inventory_hops`, `inventory_miscs`, `inventory_yeasts`) references `batches` with `back_populates`, but `Batches` relations lack `cascade=\"all, delete-orphan\"`, so dependents linger after batch removal.
- Style/profile tables (`style_guidlines.py`, `styles.py`, `Profiles/equipment_profiles.py`, `Profiles/water_profiles.py`) have `recipe_id` foreign keys but no SQLAlchemy `relationship()` wiring or reciprocal collections on `Recipes`, leaving them effectively write-only.
- `MashProfiles`/`MashStep` (`Profiles/mash_profiles.py`): `MashStep.mash_id` points to `mash.id` without ORM relationships; docstrings promise recipe/user ownership that is still unmodelled.
- Ingredient subtypes in `Ingredients/Fermentables/` (e.g. `grain.py`, `adjunct.py`, `sugar.py`) reference `recipe_fermentables`/`inventory_fermentables` through foreign keys but expose no `relationship()` helpers, limiting eager loading and cascade handling.
- `Questions` ↔ `Choices` bindings are complete with proper `back_populates`.

## Indexing Recommendations
- Create single-column indexes for all high-traffic foreign keys: `recipes.origin_recipe_id`, `batches.recipe_id`, `batch_logs.batch_id`, `style_guidelines.recipe_id`, `styles.recipe_id`, `equipment.recipe_id`, `water.recipe_id`, every recipe-level ingredient `recipe_id`, inventory `batch_id`, and fermentable subtype `fermentable_id`.
- Introduce composite indexes for frequent lookups: `(name, version)` on `recipes`, `(recipe_id, batch_number)` on `batches`, `(batch_id, name)` on each inventory table, `(recipe_id, type)` (or `(recipe_id, name)`) on recipe ingredient tables, `(question_id, is_correct)` on `choices`, and `(mash_id, step_time)` on `mash_step`.
- Enforce expected uniqueness with indexes or constraints on profile names (`equipment.name`, `mash.name`, `water.name`) per model docstrings.
- Ensure future migrations build foreign-key indexes concurrently to avoid retroactive full-table scans.
- Harden primary keys to be non-nullable on `styles` and `style_guidelines`, and audit remaining tables for similar PK nullability leaks.
