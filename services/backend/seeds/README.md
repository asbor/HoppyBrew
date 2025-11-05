# American IPA Seed Script

This directory contains seed scripts to populate the HoppyBrew database with initial recipe data.

## American IPA (BJCP 21A)

The `seed_american_ipa.py` script adds a comprehensive American IPA recipe to the database.

### Recipe Details

- **Style**: American IPA (BJCP 21A)
- **Batch Size**: 25L
- **Original Gravity (OG)**: 1.063
- **Final Gravity (FG)**: 1.014
- **IBU**: 55
- **Color**: 14 EBC
- **ABV**: 6.4%
- **Efficiency**: 75%

### Ingredients

**Fermentables** (6 kg total):
- Pale Malt (2-Row): 5.0 kg
- Wheat Malt: 0.5 kg
- Crystal/Caramel 40L: 0.3 kg
- Vienna Malt: 0.2 kg

**Hops** (150g total):
- Cascade (60 min): 25g @ 5.5% AA
- Centennial (30 min): 20g @ 10% AA
- Citra (15 min): 30g @ 12% AA
- Simcoe (Flameout): 25g @ 13% AA
- Amarillo (Dry Hop, 5 days): 50g @ 9% AA

**Yeast**:
- SafAle US-05: 11.5g (Ale, Dry)

**Misc**:
- Irish Moss (15 min): 5g
- Yeast Nutrient (10 min): 2g

## Running the Seed Script

### For Testing (SQLite)

```bash
cd /path/to/HoppyBrew/services/backend
PYTHONPATH=/path/to/HoppyBrew/services/backend TESTING=1 python3 seeds/seed_american_ipa.py
```

### For Production (PostgreSQL)

First, ensure the database container is running:

```bash
cd /path/to/HoppyBrew
docker compose up -d db
```

Wait for the database to be ready, then run:

```bash
cd /path/to/HoppyBrew/services/backend
PYTHONPATH=/path/to/HoppyBrew/services/backend python3 seeds/seed_american_ipa.py
```

Or run inside the Docker container:

```bash
docker exec -it hoppybrew-backend-1 python3 seeds/seed_american_ipa.py
```

## Idempotent Behavior

The seed script is idempotent - running it multiple times will not create duplicate recipes. If the recipe already exists, it will return the existing recipe ID.

## Testing

Tests for the seed script are located in `tests/test_seeds/test_seed_american_ipa.py`.

Run the tests with:

```bash
cd /path/to/HoppyBrew/services/backend
python3 -m pytest tests/test_seeds/test_seed_american_ipa.py -v
```

## Usage Notes

This is a **base recipe** that can be used as a template for actual brewing sessions. When creating a brew batch from this recipe:

1. The recipe can be scaled up or down (e.g., 2x for 50L, 3x for 75L)
2. You can make alterations specific to each batch
3. Alterations might vary from brew to brew based on available ingredients or preferences
4. The recipe serves as a starting point for tracking your brewing process
