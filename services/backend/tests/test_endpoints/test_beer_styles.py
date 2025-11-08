import Database.Models as models
import Database.Schemas as schemas


def test_create_style_guideline_source(client, db_session):
    """Test creating a new style guideline source"""
    response = client.post(
        "/style-guideline-sources",
        json={
            "name": "BJCP 2021",
            "year": 2021,
            "abbreviation": "BJCP",
            "description": "BJCP Beer Style Guidelines 2021 Edition",
            "is_active": True,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "BJCP 2021"
    assert data["year"] == 2021
    assert data["abbreviation"] == "BJCP"
    assert "id" in data


def test_get_all_style_guideline_sources(client, db_session):
    """Test getting all style guideline sources"""
    # Create test sources
    source1 = models.StyleGuidelineSource(
        name="BJCP 2021", year=2021, abbreviation="BJCP", is_active=True
    )
    source2 = models.StyleGuidelineSource(
        name="Brewers Association 2025", year=2025, abbreviation="BA", is_active=True
    )
    db_session.add_all([source1, source2])
    db_session.commit()

    response = client.get("/style-guideline-sources")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert any(s["name"] == "BJCP 2021" for s in data)
    assert any(s["name"] == "Brewers Association 2025" for s in data)


def test_get_style_guideline_source_by_id(client, db_session):
    """Test getting a specific style guideline source"""
    source = models.StyleGuidelineSource(
        name="BJCP 2021", year=2021, abbreviation="BJCP"
    )
    db_session.add(source)
    db_session.commit()
    db_session.refresh(source)

    response = client.get(f"/style-guideline-sources/{source.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == source.id
    assert data["name"] == "BJCP 2021"


def test_update_style_guideline_source(client, db_session):
    """Test updating a style guideline source"""
    source = models.StyleGuidelineSource(name="BJCP 2021", year=2021, is_active=True)
    db_session.add(source)
    db_session.commit()
    db_session.refresh(source)

    response = client.put(
        f"/style-guideline-sources/{source.id}", json={"is_active": False}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["is_active"] is False


def test_create_style_category(client, db_session):
    """Test creating a new style category"""
    # First create a guideline source
    source = models.StyleGuidelineSource(name="BJCP 2021", year=2021)
    db_session.add(source)
    db_session.commit()
    db_session.refresh(source)

    response = client.post(
        "/style-categories",
        json={
            "guideline_source_id": source.id,
            "name": "American Ale",
            "code": "18",
            "description": "American-style ales",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "American Ale"
    assert data["code"] == "18"


def test_get_style_categories_by_guideline(client, db_session):
    """Test getting categories filtered by guideline source"""
    source1 = models.StyleGuidelineSource(name="BJCP 2021", year=2021)
    source2 = models.StyleGuidelineSource(name="BA 2025", year=2025)
    db_session.add_all([source1, source2])
    db_session.commit()
    db_session.refresh(source1)
    db_session.refresh(source2)

    cat1 = models.StyleCategory(
        guideline_source_id=source1.id, name="American Ale", code="18"
    )
    cat2 = models.StyleCategory(
        guideline_source_id=source2.id, name="American IPA", code="21"
    )
    db_session.add_all([cat1, cat2])
    db_session.commit()

    response = client.get(f"/style-categories?guideline_source_id={source1.id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "American Ale"


def test_create_beer_style(client, db_session):
    """Test creating a new beer style"""
    source = models.StyleGuidelineSource(name="BJCP 2021", year=2021)
    db_session.add(source)
    db_session.commit()
    db_session.refresh(source)

    category = models.StyleCategory(
        guideline_source_id=source.id, name="IPA", code="21"
    )
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    response = client.post(
        "/beer-styles",
        json={
            "guideline_source_id": source.id,
            "category_id": category.id,
            "name": "American IPA",
            "style_code": "21A",
            "subcategory": "American IPA",
            "abv_min": 5.5,
            "abv_max": 7.5,
            "og_min": 1.056,
            "og_max": 1.070,
            "fg_min": 1.008,
            "fg_max": 1.014,
            "ibu_min": 40,
            "ibu_max": 70,
            "color_min_srm": 6,
            "color_max_srm": 14,
            "description": "A decidedly hoppy and bitter, moderately strong American pale ale",
            "is_custom": False,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "American IPA"
    assert data["style_code"] == "21A"
    assert data["is_custom"] is True  # Should be forced to True
    assert data["abv_min"] == 5.5
    assert data["ibu_min"] == 40


def test_get_all_beer_styles(client, db_session):
    """Test getting all beer styles"""
    source = models.StyleGuidelineSource(name="BJCP 2021", year=2021)
    db_session.add(source)
    db_session.commit()
    db_session.refresh(source)

    style1 = models.BeerStyle(
        guideline_source_id=source.id,
        name="American IPA",
        style_code="21A",
        is_custom=False,
    )
    style2 = models.BeerStyle(
        guideline_source_id=source.id,
        name="American Pale Ale",
        style_code="18B",
        is_custom=False,
    )
    db_session.add_all([style1, style2])
    db_session.commit()

    response = client.get("/beer-styles")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_get_beer_style_by_id(client, db_session):
    """Test getting a specific beer style"""
    source = models.StyleGuidelineSource(name="BJCP 2021", year=2021)
    db_session.add(source)
    db_session.commit()
    db_session.refresh(source)

    style = models.BeerStyle(
        guideline_source_id=source.id,
        name="American IPA",
        style_code="21A",
        abv_min=5.5,
        abv_max=7.5,
        is_custom=False,
    )
    db_session.add(style)
    db_session.commit()
    db_session.refresh(style)

    response = client.get(f"/beer-styles/{style.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == style.id
    assert data["name"] == "American IPA"
    assert data["abv_min"] == 5.5


def test_search_beer_styles_by_name(client, db_session):
    """Test searching beer styles by name"""
    source = models.StyleGuidelineSource(name="BJCP 2021", year=2021)
    db_session.add(source)
    db_session.commit()
    db_session.refresh(source)

    style1 = models.BeerStyle(
        guideline_source_id=source.id, name="American IPA", is_custom=False
    )
    style2 = models.BeerStyle(
        guideline_source_id=source.id, name="American Pale Ale", is_custom=False
    )
    style3 = models.BeerStyle(
        guideline_source_id=source.id, name="English IPA", is_custom=False
    )
    db_session.add_all([style1, style2, style3])
    db_session.commit()

    response = client.get("/beer-styles/search?query=IPA")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all("IPA" in s["name"] for s in data)


def test_search_beer_styles_by_abv_range(client, db_session):
    """Test searching beer styles by ABV range"""
    source = models.StyleGuidelineSource(name="BJCP 2021", year=2021)
    db_session.add(source)
    db_session.commit()
    db_session.refresh(source)

    style1 = models.BeerStyle(
        guideline_source_id=source.id,
        name="Light Lager",
        abv_min=4.0,
        abv_max=5.0,
        is_custom=False,
    )
    style2 = models.BeerStyle(
        guideline_source_id=source.id,
        name="American IPA",
        abv_min=5.5,
        abv_max=7.5,
        is_custom=False,
    )
    style3 = models.BeerStyle(
        guideline_source_id=source.id,
        name="Imperial Stout",
        abv_min=8.0,
        abv_max=12.0,
        is_custom=False,
    )
    db_session.add_all([style1, style2, style3])
    db_session.commit()

    # Search for styles that can produce 6% ABV beer
    response = client.get("/beer-styles/search?abv_min=6.0&abv_max=6.0")
    assert response.status_code == 200
    data = response.json()
    # Should match American IPA (5.5-7.5%) but not Light Lager or Imperial Stout
    assert len(data) == 1
    assert data[0]["name"] == "American IPA"


def test_search_beer_styles_by_ibu_range(client, db_session):
    """Test searching beer styles by IBU range"""
    source = models.StyleGuidelineSource(name="BJCP 2021", year=2021)
    db_session.add(source)
    db_session.commit()
    db_session.refresh(source)

    style1 = models.BeerStyle(
        guideline_source_id=source.id,
        name="Light Lager",
        ibu_min=8,
        ibu_max=15,
        is_custom=False,
    )
    style2 = models.BeerStyle(
        guideline_source_id=source.id,
        name="American IPA",
        ibu_min=40,
        ibu_max=70,
        is_custom=False,
    )
    db_session.add_all([style1, style2])
    db_session.commit()

    response = client.get("/beer-styles/search?ibu_min=50&ibu_max=60")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "American IPA"


def test_update_custom_beer_style(client, db_session):
    """Test updating a custom beer style"""
    source = models.StyleGuidelineSource(name="BJCP 2021", year=2021)
    db_session.add(source)
    db_session.commit()
    db_session.refresh(source)

    style = models.BeerStyle(
        guideline_source_id=source.id, name="My Custom IPA", is_custom=True
    )
    db_session.add(style)
    db_session.commit()
    db_session.refresh(style)

    response = client.put(
        f"/beer-styles/{style.id}", json={"description": "My special custom IPA recipe"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "My special custom IPA recipe"


def test_cannot_update_standard_style(client, db_session):
    """Test that standard styles cannot be updated"""
    source = models.StyleGuidelineSource(name="BJCP 2021", year=2021)
    db_session.add(source)
    db_session.commit()
    db_session.refresh(source)

    style = models.BeerStyle(
        guideline_source_id=source.id, name="American IPA", is_custom=False
    )
    db_session.add(style)
    db_session.commit()
    db_session.refresh(style)

    response = client.put(
        f"/beer-styles/{style.id}", json={"description": "Modified description"}
    )
    assert response.status_code == 403
    assert "Cannot modify standard beer styles" in response.json()["detail"]


def test_delete_custom_beer_style(client, db_session):
    """Test deleting a custom beer style"""
    source = models.StyleGuidelineSource(name="BJCP 2021", year=2021)
    db_session.add(source)
    db_session.commit()
    db_session.refresh(source)

    style = models.BeerStyle(
        guideline_source_id=source.id, name="My Custom Style", is_custom=True
    )
    db_session.add(style)
    db_session.commit()
    db_session.refresh(style)

    response = client.delete(f"/beer-styles/{style.id}")
    assert response.status_code == 200
    assert "deleted successfully" in response.json()["message"]


def test_cannot_delete_standard_style(client, db_session):
    """Test that standard styles cannot be deleted"""
    source = models.StyleGuidelineSource(name="BJCP 2021", year=2021)
    db_session.add(source)
    db_session.commit()
    db_session.refresh(source)

    style = models.BeerStyle(
        guideline_source_id=source.id, name="American IPA", is_custom=False
    )
    db_session.add(style)
    db_session.commit()
    db_session.refresh(style)

    response = client.delete(f"/beer-styles/{style.id}")
    assert response.status_code == 403
    assert "Cannot delete standard beer styles" in response.json()["detail"]


def test_filter_beer_styles_by_custom(client, db_session):
    """Test filtering beer styles by custom flag"""
    source = models.StyleGuidelineSource(name="BJCP 2021", year=2021)
    db_session.add(source)
    db_session.commit()
    db_session.refresh(source)

    style1 = models.BeerStyle(
        guideline_source_id=source.id, name="American IPA", is_custom=False
    )
    style2 = models.BeerStyle(
        guideline_source_id=source.id, name="My Custom IPA", is_custom=True
    )
    db_session.add_all([style1, style2])
    db_session.commit()

    # Get only custom styles
    response = client.get("/beer-styles?is_custom=true")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "My Custom IPA"

    # Get only standard styles
    response = client.get("/beer-styles?is_custom=false")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "American IPA"
