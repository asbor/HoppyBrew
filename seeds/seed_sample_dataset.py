#!/usr/bin/env python3
"""Populate the database with a rich demo dataset for HoppyBrew."""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

# Prefer the lightweight SQLite test database when no explicit configuration is
# provided. This keeps the script runnable on developer machines without a
# running PostgreSQL instance.
if not os.getenv("TESTING") and not os.getenv("DATABASE_HOST"):
    os.environ["TESTING"] = "1"
    os.environ.setdefault("TEST_DATABASE_URL", "sqlite:///./hoppybrew_sample.db")

import sys

BACKEND_ROOT = Path(__file__).resolve().parents[1] / "services" / "backend"
sys.path.append(str(BACKEND_ROOT))

from sqlalchemy.orm import Session  # type: ignore

from logger_config import get_logger  # type: ignore
from database import Base, SessionLocal, engine  # type: ignore
import Database.Models as models  # type: ignore
from Database.Models.users import Users  # type: ignore

LOGGER = get_logger("SampleDataset")
DATASET_PATH = Path(__file__).resolve().parents[1] / "data" / "sample_dataset.json"


def _load_dataset() -> Dict[str, Any]:
    if not DATASET_PATH.exists():
        raise FileNotFoundError(f"Sample dataset not found: {DATASET_PATH}")
    with DATASET_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _upsert_user(session: Session, payload: Dict[str, Any]) -> bool:
    existing = (
        session.query(Users)
        .filter(Users.username == payload["username"])
        .one_or_none()
    )
    if existing:
        for key, value in payload.items():
            setattr(existing, key, value)
        return False
    session.add(Users(**payload))
    return True


def _upsert_inventory(
    session: Session,
    model,
    unique_fields: Tuple[str, ...],
    payloads: Iterable[Dict[str, Any]],
) -> int:
    created = 0
    for payload in payloads:
        query = {field: payload[field] for field in unique_fields if field in payload}
        existing = session.query(model).filter_by(**query).one_or_none()
        if existing:
            for key, value in payload.items():
                setattr(existing, key, value)
        else:
            session.add(model(**payload))
            created += 1
    return created


def _replace_children(
    session: Session,
    relationship: Iterable,
    model,
    parent_field: str,
    parent_id: int,
    payloads: Iterable[Dict[str, Any]],
) -> None:
    for child in list(relationship):
        session.delete(child)
    session.flush()
    for payload in payloads:
        data = dict(payload)
        data[parent_field] = parent_id
        session.add(model(**data))


def _upsert_recipe(session: Session, payload: Dict[str, Any]) -> Tuple[models.Recipes, bool]:
    related_keys = {"hops", "fermentables", "yeasts", "miscs"}
    base_payload = {k: v for k, v in payload.items() if k not in related_keys}

    existing = (
        session.query(models.Recipes)
        .filter(
            models.Recipes.name == base_payload["name"],
            models.Recipes.version == base_payload.get("version"),
            models.Recipes.is_batch == False,
        )
        .one_or_none()
    )

    created = existing is None
    recipe = existing or models.Recipes(is_batch=False, **base_payload)
    if created:
        session.add(recipe)
        session.flush()
    else:
        for key, value in base_payload.items():
            setattr(recipe, key, value)

    _replace_children(
        session,
        recipe.hops,
        models.RecipeHop,
        "recipe_id",
        recipe.id,
        payload.get("hops", []),
    )
    _replace_children(
        session,
        recipe.fermentables,
        models.RecipeFermentable,
        "recipe_id",
        recipe.id,
        payload.get("fermentables", []),
    )
    _replace_children(
        session,
        recipe.yeasts,
        models.RecipeYeast,
        "recipe_id",
        recipe.id,
        payload.get("yeasts", []),
    )
    _replace_children(
        session,
        recipe.miscs,
        models.RecipeMisc,
        "recipe_id",
        recipe.id,
        payload.get("miscs", []),
    )

    return recipe, created


def _clone_recipe_for_batch(session: Session, recipe: models.Recipes) -> models.Recipes:
    clone = models.Recipes(
        name=recipe.name,
        is_batch=True,
        origin_recipe_id=recipe.id,
        version=recipe.version,
        type=recipe.type,
        brewer=recipe.brewer,
        asst_brewer=recipe.asst_brewer,
        batch_size=recipe.batch_size,
        boil_size=recipe.boil_size,
        boil_time=recipe.boil_time,
        efficiency=recipe.efficiency,
        notes=recipe.notes,
        taste_notes=recipe.taste_notes,
        taste_rating=recipe.taste_rating,
        og=recipe.og,
        fg=recipe.fg,
        fermentation_stages=recipe.fermentation_stages,
        primary_age=recipe.primary_age,
        primary_temp=recipe.primary_temp,
        secondary_age=recipe.secondary_age,
        secondary_temp=recipe.secondary_temp,
        tertiary_age=recipe.tertiary_age,
        age=recipe.age,
        age_temp=recipe.age_temp,
        carbonation_used=recipe.carbonation_used,
        est_og=recipe.est_og,
        est_fg=recipe.est_fg,
        est_color=recipe.est_color,
        ibu=recipe.ibu,
        ibu_method=recipe.ibu_method,
        est_abv=recipe.est_abv,
        abv=recipe.abv,
        actual_efficiency=recipe.actual_efficiency,
        calories=recipe.calories,
        display_batch_size=recipe.display_batch_size,
        display_boil_size=recipe.display_boil_size,
        display_og=recipe.display_og,
        display_fg=recipe.display_fg,
        display_primary_temp=recipe.display_primary_temp,
        display_secondary_temp=recipe.display_secondary_temp,
        display_tertiary_temp=recipe.display_tertiary_temp,
        display_age_temp=recipe.display_age_temp,
    )
    session.add(clone)
    session.flush()

    _replace_children(
        session,
        clone.hops,
        models.RecipeHop,
        "recipe_id",
        clone.id,
        [
            {
                "name": hop.name,
                "origin": hop.origin,
                "alpha": hop.alpha,
                "type": hop.type,
                "form": hop.form,
                "beta": hop.beta,
                "hsi": hop.hsi,
                "amount": hop.amount,
                "use": hop.use,
                "time": hop.time,
                "notes": hop.notes,
                "display_amount": hop.display_amount,
                "inventory": hop.inventory,
                "display_time": hop.display_time,
            }
            for hop in recipe.hops
        ],
    )
    _replace_children(
        session,
        clone.fermentables,
        models.RecipeFermentable,
        "recipe_id",
        clone.id,
        [
            {
                "name": item.name,
                "type": item.type,
                "yield_": item.yield_,
                "color": item.color,
                "origin": item.origin,
                "supplier": item.supplier,
                "notes": item.notes,
                "potential": item.potential,
                "amount": item.amount,
                "cost_per_unit": item.cost_per_unit,
                "manufacturing_date": item.manufacturing_date,
                "expiry_date": item.expiry_date,
                "lot_number": item.lot_number,
                "exclude_from_total": item.exclude_from_total,
                "not_fermentable": item.not_fermentable,
                "description": item.description,
                "substitutes": item.substitutes,
                "used_in": item.used_in,
            }
            for item in recipe.fermentables
        ],
    )
    _replace_children(
        session,
        clone.miscs,
        models.RecipeMisc,
        "recipe_id",
        clone.id,
        [
            {
                "name": item.name,
                "type": item.type,
                "use": item.use,
                "amount_is_weight": item.amount_is_weight,
                "use_for": item.use_for,
                "notes": item.notes,
                "amount": item.amount,
                "time": item.time,
                "display_amount": item.display_amount,
                "inventory": item.inventory,
                "display_time": item.display_time,
                "batch_size": item.batch_size,
            }
            for item in recipe.miscs
        ],
    )
    _replace_children(
        session,
        clone.yeasts,
        models.RecipeYeast,
        "recipe_id",
        clone.id,
        [
            {
                "name": item.name,
                "type": item.type,
                "form": item.form,
                "amount": item.amount,
                "amount_is_weight": item.amount_is_weight,
                "laboratory": item.laboratory,
                "product_id": item.product_id,
                "min_temperature": item.min_temperature,
                "max_temperature": item.max_temperature,
                "flocculation": item.flocculation,
                "attenuation": item.attenuation,
                "notes": item.notes,
                "best_for": item.best_for,
                "times_cultured": item.times_cultured,
                "max_reuse": item.max_reuse,
                "add_to_secondary": item.add_to_secondary,
            }
            for item in recipe.yeasts
        ],
    )
    return clone


def _ensure_datetime(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        return datetime.fromisoformat(value)
    raise ValueError(f"Unsupported datetime value: {value}")


def _seed_batches(session: Session, payloads: Iterable[Dict[str, Any]]) -> int:
    created = 0
    for payload in payloads:
        recipe_name = payload.get("recipe_name")
        if not recipe_name:
            LOGGER.warning("Skipping batch without recipe_name: %s", payload)
            continue
        recipe = (
            session.query(models.Recipes)
            .filter(
                models.Recipes.name == recipe_name,
                models.Recipes.is_batch == False,
            )
            .order_by(models.Recipes.version.desc())
            .first()
        )
        if not recipe:
            LOGGER.warning("No recipe found for batch %s", recipe_name)
            continue

        existing = (
            session.query(models.Batches)
            .filter(models.Batches.batch_name == payload["batch_name"])
            .one_or_none()
        )
        if existing:
            LOGGER.info("Batch already exists: %s", payload["batch_name"])
            continue

        clone = _clone_recipe_for_batch(session, recipe)
        batch = models.Batches(
            recipe_id=clone.id,
            batch_name=payload["batch_name"],
            batch_number=payload["batch_number"],
            batch_size=payload["batch_size"],
            brewer=payload["brewer"],
            brew_date=_ensure_datetime(payload["brew_date"]),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        session.add(batch)
        session.flush()

        for hop in clone.hops:
            session.add(
                models.InventoryHop(
                    name=hop.name,
                    origin=hop.origin,
                    alpha=hop.alpha,
                    type=hop.type,
                    form=hop.form,
                    beta=hop.beta,
                    hsi=hop.hsi,
                    amount=hop.amount,
                    use=hop.use,
                    time=hop.time,
                    notes=hop.notes,
                    display_amount=hop.display_amount,
                    inventory=hop.inventory,
                    display_time=hop.display_time,
                    batch_id=batch.id,
                )
            )
        for fermentable in clone.fermentables:
            session.add(
                models.InventoryFermentable(
                    name=fermentable.name,
                    type=fermentable.type,
                    yield_=fermentable.yield_,
                    color=fermentable.color,
                    origin=fermentable.origin,
                    supplier=fermentable.supplier,
                    notes=fermentable.notes,
                    potential=fermentable.potential,
                    amount=fermentable.amount,
                    cost_per_unit=fermentable.cost_per_unit,
                    manufacturing_date=fermentable.manufacturing_date,
                    expiry_date=fermentable.expiry_date,
                    lot_number=fermentable.lot_number,
                    exclude_from_total=fermentable.exclude_from_total,
                    not_fermentable=fermentable.not_fermentable,
                    description=fermentable.description,
                    substitutes=fermentable.substitutes,
                    used_in=fermentable.used_in,
                    batch_id=batch.id,
                )
            )
        for misc in clone.miscs:
            session.add(
                models.InventoryMisc(
                    name=misc.name,
                    type=misc.type,
                    use=misc.use,
                    amount_is_weight=misc.amount_is_weight,
                    use_for=misc.use_for,
                    notes=misc.notes,
                    amount=misc.amount,
                    time=misc.time,
                    display_amount=misc.display_amount,
                    inventory=misc.inventory,
                    display_time=misc.display_time,
                    batch_size=misc.batch_size,
                    batch_id=batch.id,
                )
            )
        for yeast in clone.yeasts:
            session.add(
                models.InventoryYeast(
                    name=yeast.name,
                    type=yeast.type,
                    form=yeast.form,
                    laboratory=yeast.laboratory,
                    product_id=yeast.product_id,
                    min_temperature=yeast.min_temperature,
                    max_temperature=yeast.max_temperature,
                    flocculation=yeast.flocculation,
                    attenuation=yeast.attenuation,
                    notes=yeast.notes,
                    best_for=yeast.best_for,
                    max_reuse=yeast.max_reuse,
                    batch_id=batch.id,
                )
            )

        created += 1
    return created


def _seed_batch_logs(session: Session, payloads: Iterable[Dict[str, Any]]) -> int:
    created = 0
    for payload in payloads:
        batch_name = payload.get("batch_name")
        if not batch_name:
            continue
        batch = (
            session.query(models.Batches)
            .filter(models.Batches.batch_name == batch_name)
            .one_or_none()
        )
        if not batch:
            LOGGER.warning("Skipping batch log, batch not found: %s", batch_name)
            continue
        if batch.batch_log:
            batch.batch_log.activity = payload.get("activity", batch.batch_log.activity)
            batch.batch_log.notes = payload.get("notes", batch.batch_log.notes)
        else:
            session.add(
                models.BatchLogs(
                    batch_id=batch.id,
                    activity=payload.get("activity", ""),
                    notes=payload.get("notes"),
                )
            )
            created += 1
    return created


def _attach_profile(
    session: Session,
    model,
    payloads: Iterable[Dict[str, Any]],
) -> int:
    created = 0
    for payload in payloads:
        recipe_name = payload.pop("recipe_name", None)
        recipe = None
        if recipe_name:
            recipe = (
                session.query(models.Recipes)
                .filter(
                    models.Recipes.name == recipe_name,
                    models.Recipes.is_batch == False,
                )
                .order_by(models.Recipes.version.desc())
                .first()
            )
        existing = (
            session.query(model)
            .filter(model.name == payload.get("name"))
            .one_or_none()
        )
        if existing:
            for key, value in payload.items():
                setattr(existing, key, value)
            if recipe:
                existing.recipe_id = recipe.id
        else:
            record = model(**payload)
            if recipe:
                record.recipe_id = recipe.id
            session.add(record)
            created += 1
    return created


def seed_sample_dataset(session: Session | None = None) -> Dict[str, int]:
    dataset = _load_dataset()
    Base.metadata.create_all(bind=engine, checkfirst=True)

    close_session = False
    if session is None:
        session = SessionLocal()
        close_session = True

    summary: Dict[str, int] = {
        "users": 0,
        "inventory_hops": 0,
        "inventory_fermentables": 0,
        "inventory_yeasts": 0,
        "inventory_miscs": 0,
        "recipes": 0,
        "batches": 0,
        "batch_logs": 0,
        "equipment_profiles": 0,
        "water_profiles": 0,
    }

    try:
        for user in dataset.get("users", []):
            if _upsert_user(session, user):
                summary["users"] += 1

        inventory = dataset.get("inventory", {})
        summary["inventory_hops"] = _upsert_inventory(
            session,
            models.InventoryHop,
            ("name",),
            inventory.get("hops", []),
        )
        summary["inventory_fermentables"] = _upsert_inventory(
            session,
            models.InventoryFermentable,
            ("name",),
            inventory.get("fermentables", []),
        )
        summary["inventory_yeasts"] = _upsert_inventory(
            session,
            models.InventoryYeast,
            ("name",),
            inventory.get("yeasts", []),
        )
        summary["inventory_miscs"] = _upsert_inventory(
            session,
            models.InventoryMisc,
            ("name", "use"),
            inventory.get("miscs", []),
        )

        recipes = []
        for recipe_payload in dataset.get("recipes", []):
            recipe, created = _upsert_recipe(session, recipe_payload)
            recipes.append(recipe)
            if created:
                summary["recipes"] += 1

        summary["equipment_profiles"] = _attach_profile(
            session,
            models.EquipmentProfiles,
            dataset.get("equipment_profiles", []),
        )
        summary["water_profiles"] = _attach_profile(
            session,
            models.WaterProfiles,
            dataset.get("water_profiles", []),
        )

        summary["batches"] = _seed_batches(session, dataset.get("batches", []))
        summary["batch_logs"] = _seed_batch_logs(session, dataset.get("batch_logs", []))

        session.commit()
        LOGGER.info("Sample dataset seeded: %s", summary)
        return summary
    except Exception:
        session.rollback()
        LOGGER.exception("Failed to seed sample dataset")
        raise
    finally:
        if close_session:
            session.close()


def main() -> None:
    summary = seed_sample_dataset()
    LOGGER.info("Dataset load complete: %s", summary)


if __name__ == "__main__":
    main()
