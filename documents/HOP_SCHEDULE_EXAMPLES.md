# Hop Schedule Optimizer - Example Recipes

This document provides example hop schedules for various beer styles using the Hop Schedule Optimizer.

## Example 1: West Coast IPA

A classic hoppy IPA with pronounced bitterness and citrus/pine character.

**Batch Parameters:**
- Batch Size: 5.0 gallons
- Boil Gravity: 1.060

**Hop Schedule:**
| Hop | Alpha Acid | Amount | Time | Type | Form |
|-----|-----------|---------|------|------|------|
| Columbus | 14.0% | 1.0 oz | 60 min | Bittering | Pellet |
| Cascade | 5.5% | 1.0 oz | 15 min | Aroma | Pellet |
| Centennial | 10.0% | 1.0 oz | 10 min | Aroma | Pellet |
| Citra | 12.0% | 2.0 oz | 0 min | Aroma | Pellet |

**Expected Results:**
- Total IBU: ~65-70
- Bittering contribution: ~50 IBU from Columbus
- Aroma hop contribution: ~15-20 IBU
- Dominant flavors: Pine, grapefruit, citrus

## Example 2: Session IPA

A lower alcohol IPA with balanced hop character.

**Batch Parameters:**
- Batch Size: 5.0 gallons
- Boil Gravity: 1.045

**Hop Schedule:**
| Hop | Alpha Acid | Amount | Time | Type | Form |
|-----|-----------|---------|------|------|------|
| Magnum | 12.0% | 0.5 oz | 60 min | Bittering | Pellet |
| Mosaic | 12.0% | 1.0 oz | 15 min | Dual Purpose | Pellet |
| Citra | 11.5% | 1.0 oz | 5 min | Aroma | Pellet |
| Amarillo | 9.0% | 1.5 oz | 0 min | Aroma | Pellet |

**Expected Results:**
- Total IBU: ~35-40
- Clean bittering backbone
- Tropical fruit and citrus aroma
- Lower perceived bitterness for drinkability

## Example 3: New England IPA (NEIPA)

A hazy, juicy IPA with minimal perceived bitterness.

**Batch Parameters:**
- Batch Size: 5.0 gallons
- Boil Gravity: 1.065

**Hop Schedule:**
| Hop | Alpha Acid | Amount | Time | Type | Form |
|-----|-----------|---------|------|------|------|
| Warrior | 15.0% | 0.5 oz | 60 min | Bittering | Pellet |
| Citra | 12.0% | 1.0 oz | 10 min | Aroma | Pellet |
| Mosaic | 12.5% | 2.0 oz | 5 min | Aroma | Pellet |
| Galaxy | 14.0% | 2.0 oz | 0 min | Aroma | Pellet |

**Expected Results:**
- Total IBU: ~45-50 (low perceived bitterness)
- Most IBU from late additions
- Intense tropical fruit character
- Minimal clean bittering

**Note:** NEIPAs typically include additional dry hopping (3-5 oz) during fermentation, which isn't calculated in boil IBU.

## Example 4: English Bitter

A traditional English ale with earthy, floral hop character.

**Batch Parameters:**
- Batch Size: 5.0 gallons
- Boil Gravity: 1.042

**Hop Schedule:**
| Hop | Alpha Acid | Amount | Time | Type | Form |
|-----|-----------|---------|------|------|------|
| East Kent Golding | 5.0% | 1.5 oz | 60 min | Dual Purpose | Whole |
| Fuggle | 4.5% | 1.0 oz | 15 min | Aroma | Whole |
| East Kent Golding | 5.0% | 0.5 oz | 0 min | Aroma | Whole |

**Expected Results:**
- Total IBU: ~30-35
- Traditional English character
- Earthy, woody notes
- Subtle floral finish

## Example 5: Czech Pilsner

A classic European lager with noble hop character.

**Batch Parameters:**
- Batch Size: 5.0 gallons
- Boil Gravity: 1.048

**Hop Schedule:**
| Hop | Alpha Acid | Amount | Time | Type | Form |
|-----|-----------|---------|------|------|------|
| Saaz | 3.5% | 1.5 oz | 60 min | Dual Purpose | Pellet |
| Saaz | 3.5% | 1.0 oz | 30 min | Aroma | Pellet |
| Saaz | 3.5% | 1.0 oz | 0 min | Aroma | Pellet |

**Expected Results:**
- Total IBU: ~35-40
- Noble hop character
- Spicy, herbal notes
- Clean, crisp bitterness

## Example 6: American Pale Ale

A balanced pale ale with classic American hop character.

**Batch Parameters:**
- Batch Size: 5.0 gallons
- Boil Gravity: 1.052

**Hop Schedule:**
| Hop | Alpha Acid | Amount | Time | Type | Form |
|-----|-----------|---------|------|------|------|
| Chinook | 13.0% | 0.5 oz | 60 min | Bittering | Pellet |
| Cascade | 5.5% | 1.0 oz | 20 min | Aroma | Pellet |
| Cascade | 5.5% | 1.0 oz | 5 min | Aroma | Pellet |
| Cascade | 5.5% | 1.0 oz | 0 min | Aroma | Pellet |

**Expected Results:**
- Total IBU: ~45-50
- Citrus and grapefruit character
- Balanced bitterness
- Classic American C-hop profile

## Hop Substitution Examples

### If you can't find Cascade:
- **Centennial** (85% match): Similar citrus character, slightly higher alpha
- **Amarillo** (78% match): More orange/tangerine notes
- **Citra** (72% match): More intense tropical fruit

### If you can't find Citra:
- **Mosaic** (88% match): Similar tropical notes, adds berry character
- **Amarillo** (75% match): More subdued, orangey
- **Simcoe** (72% match): More piney, less tropical

### If you can't find Saaz:
- **Sterling** (85% match): American-grown Saaz substitute
- **Liberty** (82% match): Similar noble character
- **Tettnanger** (78% match): Slightly more floral

## Tips for Using the Calculator

1. **Start with bittering hops**: Add your 60-minute addition first
2. **Build flavor layers**: Add mid-boil hops (15-30 min) for complexity
3. **Finish with aroma**: Late additions (0-5 min) for maximum aroma
4. **Check total IBU**: Aim for style-appropriate bitterness levels
5. **Use substitutions wisely**: Higher similarity scores = better matches

## Common IBU Ranges by Style

- **American Lager**: 8-15 IBU
- **Hefeweizen**: 10-15 IBU
- **English Bitter**: 25-40 IBU
- **American Pale Ale**: 30-50 IBU
- **IPA**: 40-70 IBU
- **Double IPA**: 60-120 IBU
- **Imperial Stout**: 50-90 IBU

## Advanced Techniques

### Hop Bursting
Add most hops in the last 15 minutes of boil:
- Provides flavor and aroma with lower IBU
- Popular in NEIPAs
- Example: 0.5 oz @ 60 min, then 4+ oz in last 15 minutes

### First Wort Hopping (FWH)
Add hops to the kettle during runoff:
- Smoother bitterness
- Enhanced hop flavor
- Typically noble or low-alpha hops

### Whirlpool/Hopstand
Add hops after flame-out, let steep 15-30 minutes:
- Maximum aroma extraction
- Minimal IBU contribution
- Temperature-dependent (160-180°F optimal)
