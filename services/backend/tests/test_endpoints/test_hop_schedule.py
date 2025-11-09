"""
Tests for hop schedule optimizer endpoints.
"""

import pytest
from api.endpoints.calculators import (
    calculate_hop_schedule,
    get_hop_substitutions,
    HopScheduleRequest,
    HopSubstitutionRequest,
    HopAddition,
)


@pytest.mark.asyncio
async def test_calculate_hop_schedule():
    """Test hop schedule calculation with multiple additions."""
    request = HopScheduleRequest(
        hops=[
            HopAddition(
                name="Magnum",
                alpha_acid=12.0,
                amount_oz=1.0,
                time_min=60.0,
                type="Bittering",
                form="Pellet",
            ),
            HopAddition(
                name="Cascade",
                alpha_acid=5.5,
                amount_oz=1.0,
                time_min=15.0,
                type="Aroma",
                form="Pellet",
            ),
        ],
        batch_size_gal=5.0,
        boil_gravity=1.050,
    )

    result = await calculate_hop_schedule(request)

    assert result.total_ibu > 0
    assert len(result.hop_contributions) == 2
    
    # First hop (Magnum) should have higher IBU contribution
    magnum = result.hop_contributions[0]
    assert magnum.name == "Magnum"
    assert magnum.ibu > 30  # Expected ~41-42 IBU
    assert magnum.utilization > 20  # Expected ~23%
    
    # Second hop (Cascade) should have lower IBU contribution
    cascade = result.hop_contributions[1]
    assert cascade.name == "Cascade"
    assert cascade.ibu > 5  # Expected ~9-10 IBU
    assert cascade.utilization > 10  # Expected ~11%
    
    # Total should be sum of contributions
    assert abs(result.total_ibu - (magnum.ibu + cascade.ibu)) < 0.1


@pytest.mark.asyncio
async def test_calculate_hop_schedule_zero_time():
    """Test hop schedule with zero boil time (flameout addition)."""
    request = HopScheduleRequest(
        hops=[
            HopAddition(
                name="Citra",
                alpha_acid=12.0,
                amount_oz=2.0,
                time_min=0.0,
                type="Aroma",
                form="Pellet",
            ),
        ],
        batch_size_gal=5.0,
        boil_gravity=1.050,
    )

    result = await calculate_hop_schedule(request)

    # Flameout additions should have minimal IBU contribution
    assert result.total_ibu == 0.0
    assert result.hop_contributions[0].ibu == 0.0
    assert result.hop_contributions[0].utilization == 0.0


@pytest.mark.asyncio
async def test_get_hop_substitutions_cascade():
    """Test hop substitution suggestions for Cascade."""
    request = HopSubstitutionRequest(hop_name="Cascade", alpha_acid=5.5)

    result = await get_hop_substitutions(request)

    assert result.original_hop == "Cascade"
    assert len(result.substitutes) > 0
    
    # Check that substitutes are sorted by similarity score
    for i in range(len(result.substitutes) - 1):
        assert result.substitutes[i].similarity_score >= result.substitutes[i + 1].similarity_score
    
    # Centennial should be a top substitute for Cascade
    sub_names = [sub.name for sub in result.substitutes]
    assert "Centennial" in sub_names


@pytest.mark.asyncio
async def test_get_hop_substitutions_unknown_hop():
    """Test hop substitution for unknown hop variety."""
    request = HopSubstitutionRequest(hop_name="UnknownHop123", alpha_acid=10.0)

    result = await get_hop_substitutions(request)

    assert result.original_hop == "UnknownHop123"
    assert len(result.substitutes) == 0


@pytest.mark.asyncio
async def test_get_hop_substitutions_case_insensitive():
    """Test that hop substitution lookup is case-insensitive."""
    request1 = HopSubstitutionRequest(hop_name="cascade", alpha_acid=5.5)
    request2 = HopSubstitutionRequest(hop_name="CASCADE", alpha_acid=5.5)
    request3 = HopSubstitutionRequest(hop_name="Cascade", alpha_acid=5.5)

    result1 = await get_hop_substitutions(request1)
    result2 = await get_hop_substitutions(request2)
    result3 = await get_hop_substitutions(request3)

    # All should return same results with proper capitalization
    assert result1.original_hop == "Cascade"
    assert result2.original_hop == "Cascade"
    assert result3.original_hop == "Cascade"
    assert len(result1.substitutes) == len(result2.substitutes) == len(result3.substitutes)
