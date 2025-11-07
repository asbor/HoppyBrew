### services/backend/api/endpoints/batches.py
| Method | Path | Handler | Response | Summary | Source |
| --- | --- | --- | --- | --- | --- |
| GET | /batches | get_all_batches | List[schemas.Batch] |  | services/backend/api/endpoints/batches.py:210 |
| GET | /batches/{batch_id} | get_batch_by_id | schemas.Batch |  | services/backend/api/endpoints/batches.py:234 |
| PUT | /batches/{batch_id} | update_batch | schemas.Batch |  | services/backend/api/endpoints/batches.py:256 |
| DELETE | /batches/{batch_id} | delete_batch | - |  | services/backend/api/endpoints/batches.py:273 |
| POST | /batches | create_batch | schemas.Batch |  | services/backend/api/endpoints/batches.py:33 |

### services/backend/api/endpoints/beer_styles.py
| Method | Path | Handler | Response | Summary | Source |
| --- | --- | --- | --- | --- | --- |
| DELETE | /style-guideline-sources/{source_id} | delete_style_guideline_source | - | Delete a style guideline source | services/backend/api/endpoints/beer_styles.py:103 |
| GET | /style-categories | get_style_categories | List[schemas.StyleCategory] | List all style categories | services/backend/api/endpoints/beer_styles.py:132 |
| GET | /style-categories/{category_id} | get_style_category | schemas.StyleCategory | Get a specific style category | services/backend/api/endpoints/beer_styles.py:151 |
| POST | /style-categories | create_style_category | schemas.StyleCategory | Create a new style category | services/backend/api/endpoints/beer_styles.py:162 |
| PUT | /style-categories/{category_id} | update_style_category | schemas.StyleCategory | Update a style category | services/backend/api/endpoints/beer_styles.py:182 |
| DELETE | /style-categories/{category_id} | delete_style_category | - | Delete a style category | services/backend/api/endpoints/beer_styles.py:208 |
| GET | /style-guideline-sources | get_style_guideline_sources | List[schemas.StyleGuidelineSource] | List all style guideline sources | services/backend/api/endpoints/beer_styles.py:23 |
| GET | /beer-styles | get_beer_styles | List[schemas.BeerStyle] | List all beer styles with filtering | services/backend/api/endpoints/beer_styles.py:236 |
| GET | /beer-styles/search | search_beer_styles | List[schemas.BeerStyle] | Search beer styles | services/backend/api/endpoints/beer_styles.py:265 |
| GET | /beer-styles/{style_id} | get_beer_style | schemas.BeerStyle | Get a specific beer style | services/backend/api/endpoints/beer_styles.py:349 |
| POST | /beer-styles | create_beer_style | schemas.BeerStyle | Create a new beer style (custom) | services/backend/api/endpoints/beer_styles.py:368 |
| GET | /style-guideline-sources/{source_id} | get_style_guideline_source | schemas.StyleGuidelineSource | Get a specific style guideline source | services/backend/api/endpoints/beer_styles.py:38 |
| PUT | /beer-styles/{style_id} | update_beer_style | schemas.BeerStyle | Update a beer style | services/backend/api/endpoints/beer_styles.py:388 |
| DELETE | /beer-styles/{style_id} | delete_beer_style | - | Delete a beer style | services/backend/api/endpoints/beer_styles.py:420 |
| POST | /style-guideline-sources | create_style_guideline_source | schemas.StyleGuidelineSource | Create a new style guideline source | services/backend/api/endpoints/beer_styles.py:55 |
| PUT | /style-guideline-sources/{source_id} | update_style_guideline_source | schemas.StyleGuidelineSource | Update a style guideline source | services/backend/api/endpoints/beer_styles.py:75 |

### services/backend/api/endpoints/devices.py
| Method | Path | Handler | Response | Summary | Source |
| --- | --- | --- | --- | --- | --- |
| GET | /devices | get_all_devices | List[schemas.Device] |  | services/backend/api/endpoints/devices.py:14 |
| GET | /devices/{device_id} | get_device | schemas.Device |  | services/backend/api/endpoints/devices.py:26 |
| POST | /devices | create_device | schemas.Device |  | services/backend/api/endpoints/devices.py:40 |
| PUT | /devices/{device_id} | update_device | schemas.Device |  | services/backend/api/endpoints/devices.py:56 |
| DELETE | /devices/{device_id} | delete_device | schemas.Device |  | services/backend/api/endpoints/devices.py:82 |

### services/backend/api/endpoints/equipment_profiles.py
| Method | Path | Handler | Response | Summary | Source |
| --- | --- | --- | --- | --- | --- |
| GET | /equipment/{profile_id} | get_equipment_profile | dict |  | services/backend/api/endpoints/equipment_profiles.py:110 |
| GET | /equipment | get_equipment_profiles | List[dict] |  | services/backend/api/endpoints/equipment_profiles.py:15 |
| PUT | /equipment/{profile_id} | update_equipment_profile | dict |  | services/backend/api/endpoints/equipment_profiles.py:151 |
| DELETE | /equipment/{profile_id} | delete_equipment_profile | dict |  | services/backend/api/endpoints/equipment_profiles.py:220 |
| POST | /equipment | create_equipment_profile | dict |  | services/backend/api/endpoints/equipment_profiles.py:57 |

### services/backend/api/endpoints/fermentables.py
| Method | Path | Handler | Response | Summary | Source |
| --- | --- | --- | --- | --- | --- |
| GET | /recipes/fermentables | get_all_recipe_fermentables | List[schemas.RecipeFermentable] |  | services/backend/api/endpoints/fermentables.py:16 |
| GET | /inventory/fermentables | get_all_inventory_fermentables | List[schemas.InventoryFermentable] |  | services/backend/api/endpoints/fermentables.py:28 |
| GET | /inventory/fermentables/{fermentable_id} | get_inventory_fermentable | schemas.InventoryFermentable |  | services/backend/api/endpoints/fermentables.py:37 |
| DELETE | /inventory/fermentables/{id} | delete_inventory_fermentable | schemas.InventoryFermentable |  | services/backend/api/endpoints/fermentables.py:49 |

### services/backend/api/endpoints/fermentation_profiles.py
| Method | Path | Handler | Response | Summary | Source |
| --- | --- | --- | --- | --- | --- |
| PUT | /fermentation-profiles/{profile_id} | update_fermentation_profile | schemas.FermentationProfile | Update a fermentation profile | services/backend/api/endpoints/fermentation_profiles.py:106 |
| DELETE | /fermentation-profiles/{profile_id} | delete_fermentation_profile | - | Delete a fermentation profile | services/backend/api/endpoints/fermentation_profiles.py:142 |
| GET | /fermentation-profiles/{profile_id}/steps | get_fermentation_steps | List[schemas.FermentationStep] | Get steps for a fermentation profile | services/backend/api/endpoints/fermentation_profiles.py:164 |
| POST | /fermentation-profiles/{profile_id}/steps | add_fermentation_step | schemas.FermentationStep | Add a step to a fermentation profile | services/backend/api/endpoints/fermentation_profiles.py:194 |
| GET | /fermentation-profiles | get_all_fermentation_profiles | List[schemas.FermentationProfile] | List all fermentation profiles | services/backend/api/endpoints/fermentation_profiles.py:23 |
| PUT | /fermentation-steps/{step_id} | update_fermentation_step | schemas.FermentationStep | Update a fermentation step | services/backend/api/endpoints/fermentation_profiles.py:231 |
| DELETE | /fermentation-steps/{step_id} | delete_fermentation_step | - | Delete a fermentation step | services/backend/api/endpoints/fermentation_profiles.py:258 |
| GET | /fermentation-profiles/{profile_id} | get_fermentation_profile | schemas.FermentationProfile | Get a specific fermentation profile | services/backend/api/endpoints/fermentation_profiles.py:37 |
| POST | /fermentation-profiles | create_fermentation_profile | schemas.FermentationProfile | Create a new fermentation profile | services/backend/api/endpoints/fermentation_profiles.py:58 |

### services/backend/api/endpoints/health.py
| Method | Path | Handler | Response | Summary | Source |
| --- | --- | --- | --- | --- | --- |
| GET | /health | health_check | HealthResponse | Health probe | services/backend/api/endpoints/health.py:27 |

### services/backend/api/endpoints/homeassistant.py
| Method | Path | Handler | Response | Summary | Source |
| --- | --- | --- | --- | --- | --- |
| GET | /homeassistant/batches/{batch_id} | get_batch_for_homeassistant | HomeAssistantBatchSensor | Get specific batch as HomeAssistant sensor | services/backend/api/endpoints/homeassistant.py:153 |
| GET | /homeassistant/summary | get_brewery_summary | - | Get brewery summary for HomeAssistant | services/backend/api/endpoints/homeassistant.py:223 |
| GET | /homeassistant/discovery/batch/{batch_id} | get_batch_mqtt_discovery | - | Get MQTT discovery configuration for a batch | services/backend/api/endpoints/homeassistant.py:280 |
| GET | /homeassistant/batches | get_batches_for_homeassistant | List[HomeAssistantBatchSensor] | Get all batches as HomeAssistant sensors | services/backend/api/endpoints/homeassistant.py:79 |

### services/backend/api/endpoints/hops.py
| Method | Path | Handler | Response | Summary | Source |
| --- | --- | --- | --- | --- | --- |
| GET | /recipes/hops | get_all_recipe_hops | List[schemas.RecipeHop] |  | services/backend/api/endpoints/hops.py:16 |
| GET | /inventory/hops | get_all_inventory_hops | List[schemas.InventoryHop] |  | services/backend/api/endpoints/hops.py:25 |
| GET | /inventory/hops/{hop_id} | get_inventory_hop | schemas.InventoryHop |  | services/backend/api/endpoints/hops.py:31 |
| DELETE | /inventory/hops/{id} | delete_inventory_hop | schemas.InventoryHop |  | services/backend/api/endpoints/hops.py:39 |

### services/backend/api/endpoints/inventory_fermentables.py
| Method | Path | Handler | Response | Summary | Source |
| --- | --- | --- | --- | --- | --- |
| POST | /inventory/fermentables | create_inventory_fermentable | schemas.InventoryFermentable |  | services/backend/api/endpoints/inventory_fermentables.py:14 |
| PUT | /inventory/fermentables/{id} | update_inventory_fermentable | schemas.InventoryFermentable |  | services/backend/api/endpoints/inventory_fermentables.py:29 |

### services/backend/api/endpoints/inventory_hops.py
| Method | Path | Handler | Response | Summary | Source |
| --- | --- | --- | --- | --- | --- |
| POST | /inventory/hops | create_inventory_hop | schemas.InventoryHop |  | services/backend/api/endpoints/inventory_hops.py:14 |
| PUT | /inventory/hops/{id} | update_inventory_hop | schemas.InventoryHop |  | services/backend/api/endpoints/inventory_hops.py:26 |

### services/backend/api/endpoints/inventory_miscs.py
| Method | Path | Handler | Response | Summary | Source |
| --- | --- | --- | --- | --- | --- |
| POST | /inventory/miscs | create_inventory_misc | schemas.InventoryMisc |  | services/backend/api/endpoints/inventory_miscs.py:14 |
| PUT | /inventory/miscs/{id} | update_inventory_misc | schemas.InventoryMisc |  | services/backend/api/endpoints/inventory_miscs.py:26 |

### services/backend/api/endpoints/inventory_yeasts.py
| Method | Path | Handler | Response | Summary | Source |
| --- | --- | --- | --- | --- | --- |
| POST | /inventory/yeasts | create_inventory_yeast | schemas.InventoryYeast |  | services/backend/api/endpoints/inventory_yeasts.py:14 |
| PUT | /inventory/yeasts/{id} | update_inventory_yeast | schemas.InventoryYeast |  | services/backend/api/endpoints/inventory_yeasts.py:28 |

### services/backend/api/endpoints/logs.py
| Method | Path | Handler | Response | Summary | Source |
| --- | --- | --- | --- | --- | --- |
| GET | /api/logs | get_logs | LogContentResponse | Download backend logs | services/backend/api/endpoints/logs.py:26 |

### services/backend/api/endpoints/mash_profiles.py
| Method | Path | Handler | Response | Summary | Source |
| --- | --- | --- | --- | --- | --- |
| PUT | /mash/{profile_id} | update_mash_profile | dict |  | services/backend/api/endpoints/mash_profiles.py:112 |
| GET | /mash | get_mash_profiles | List[dict] |  | services/backend/api/endpoints/mash_profiles.py:15 |
| DELETE | /mash/{profile_id} | delete_mash_profile | dict |  | services/backend/api/endpoints/mash_profiles.py:168 |
| GET | /mash/{profile_id}/steps | get_mash_steps | List[dict] |  | services/backend/api/endpoints/mash_profiles.py:191 |
| POST | /mash/{profile_id}/steps | create_mash_step | dict |  | services/backend/api/endpoints/mash_profiles.py:234 |
| PUT | /mash/steps/{step_id} | update_mash_step | dict |  | services/backend/api/endpoints/mash_profiles.py:276 |
| DELETE | /mash/steps/{step_id} | delete_mash_step | dict |  | services/backend/api/endpoints/mash_profiles.py:317 |
| POST | /mash | create_mash_profile | dict |  | services/backend/api/endpoints/mash_profiles.py:46 |
| GET | /mash/{profile_id} | get_mash_profile | dict |  | services/backend/api/endpoints/mash_profiles.py:84 |

### services/backend/api/endpoints/miscs.py
| Method | Path | Handler | Response | Summary | Source |
| --- | --- | --- | --- | --- | --- |
| GET | /recipes/miscs | get_all_recipe_miscs | List[schemas.RecipeMisc] |  | services/backend/api/endpoints/miscs.py:16 |
| GET | /inventory/miscs | get_all_inventory_miscs | List[schemas.InventoryMisc] |  | services/backend/api/endpoints/miscs.py:25 |
| GET | /inventory/miscs/{misc_id} | get_inventory_misc | schemas.InventoryMisc |  | services/backend/api/endpoints/miscs.py:31 |
| DELETE | /inventory/miscs/{id} | delete_inventory_misc | schemas.InventoryMisc |  | services/backend/api/endpoints/miscs.py:39 |

### services/backend/api/endpoints/questions.py
| Method | Path | Handler | Response | Summary | Source |
| --- | --- | --- | --- | --- | --- |
| POST | /questions | create_questions | question_schemas.QuestionWithID |  | services/backend/api/endpoints/questions.py:13 |
| GET | /questions | get_all_questions | List[question_schemas.QuestionWithID] |  | services/backend/api/endpoints/questions.py:43 |
| DELETE | /questions/{question_id} | delete_question | question_schemas.QuestionWithID |  | services/backend/api/endpoints/questions.py:55 |

### services/backend/api/endpoints/recipes.py
| Method | Path | Handler | Response | Summary | Source |
| --- | --- | --- | --- | --- | --- |
| GET | /recipes | get_all_recipes | List[schemas.Recipe] |  | services/backend/api/endpoints/recipes.py:127 |
| GET | /recipes/{recipe_id} | get_recipe_by_id | schemas.Recipe |  | services/backend/api/endpoints/recipes.py:140 |
| POST | /recipes | create_recipe | schemas.Recipe |  | services/backend/api/endpoints/recipes.py:155 |
| PUT | /recipes/{recipe_id} | update_recipe | schemas.Recipe |  | services/backend/api/endpoints/recipes.py:202 |
| DELETE | /recipes/{recipe_id} | delete_recipe | - |  | services/backend/api/endpoints/recipes.py:252 |
| POST | /recipes/{recipe_id}/scale | scale_recipe | schemas.RecipeScaleResponse |  | services/backend/api/endpoints/recipes.py:272 |

### services/backend/api/endpoints/references.py
| Method | Path | Handler | Response | Summary | Source |
| --- | --- | --- | --- | --- | --- |
| GET | /references | get_all_references | List[schemas.Reference] |  | services/backend/api/endpoints/references.py:125 |
| GET | /references/{reference_id} | get_reference | schemas.Reference |  | services/backend/api/endpoints/references.py:131 |
| POST | /references | create_reference | schemas.Reference |  | services/backend/api/endpoints/references.py:139 |
| DELETE | /references/{reference_id} | delete_reference | schemas.Reference |  | services/backend/api/endpoints/references.py:151 |
| PUT | /references/{reference_id} | update_reference | schemas.Reference |  | services/backend/api/endpoints/references.py:161 |
| POST | /references/import | import_references | ReferenceImportResponse | Import references from BeerXML | services/backend/api/endpoints/references.py:58 |
| GET | /references/export | export_references | - |  | services/backend/api/endpoints/references.py:98 |

### services/backend/api/endpoints/style_guidelines.py
| Method | Path | Handler | Response | Summary | Source |
| --- | --- | --- | --- | --- | --- |
| GET | /style_guidelines | get_all_style_guidelines | List[schemas.StyleGuidelineBase] |  | services/backend/api/endpoints/style_guidelines.py:16 |
| GET | /style_guidelines/{guideline_id} | get_style_guideline | schemas.StyleGuidelineBase |  | services/backend/api/endpoints/style_guidelines.py:25 |
| POST | /style_guidelines | create_style_guideline | schemas.StyleGuidelineBase |  | services/backend/api/endpoints/style_guidelines.py:35 |
| DELETE | /style_guidelines/{id} | delete_style_guideline | schemas.StyleGuidelineBase |  | services/backend/api/endpoints/style_guidelines.py:49 |
| PUT | /style_guidelines/{id} | update_style_guideline | schemas.StyleGuidelineBase |  | services/backend/api/endpoints/style_guidelines.py:59 |

### services/backend/api/endpoints/styles.py
| Method | Path | Handler | Response | Summary | Source |
| --- | --- | --- | --- | --- | --- |
| GET | /styles | get_all_styles | List[schemas.Style] | List beer style definitions | services/backend/api/endpoints/styles.py:20 |

### services/backend/api/endpoints/trigger_beer_styles_processing.py
| Method | Path | Handler | Response | Summary | Source |
| --- | --- | --- | --- | --- | --- |
| POST | /refresh-beer-styles | trigger_script | BeerStyleRefreshResponse | Refresh cached beer style data | services/backend/api/endpoints/trigger_beer_styles_processing.py:35 |

### services/backend/api/endpoints/water_profiles.py
| Method | Path | Handler | Response | Summary | Source |
| --- | --- | --- | --- | --- | --- |
| DELETE | /water-profiles/{profile_id} | delete_water_profile | schemas.WaterProfile |  | services/backend/api/endpoints/water_profiles.py:140 |
| GET | /water-profiles | get_water_profiles | List[schemas.WaterProfile] |  | services/backend/api/endpoints/water_profiles.py:15 |
| POST | /water-profiles/{profile_id}/duplicate | duplicate_water_profile | schemas.WaterProfile |  | services/backend/api/endpoints/water_profiles.py:162 |
| POST | /water-profiles | create_water_profile | schemas.WaterProfile |  | services/backend/api/endpoints/water_profiles.py:44 |
| GET | /water-profiles/{profile_id} | get_water_profile | schemas.WaterProfile |  | services/backend/api/endpoints/water_profiles.py:76 |
| PUT | /water-profiles/{profile_id} | update_water_profile | schemas.WaterProfile |  | services/backend/api/endpoints/water_profiles.py:89 |

### services/backend/api/endpoints/yeasts.py
| Method | Path | Handler | Response | Summary | Source |
| --- | --- | --- | --- | --- | --- |
| GET | /recipes/yeasts | get_all_recipe_yeasts | List[schemas.RecipeYeast] |  | services/backend/api/endpoints/yeasts.py:16 |
| GET | /inventory/yeasts | get_all_inventory_yeasts | List[schemas.InventoryYeast] |  | services/backend/api/endpoints/yeasts.py:25 |
| GET | /inventory/yeasts/{yeast_id} | get_inventory_yeast | schemas.InventoryYeast |  | services/backend/api/endpoints/yeasts.py:31 |
| DELETE | /inventory/yeasts/{id} | delete_inventory_yeast | schemas.InventoryYeast |  | services/backend/api/endpoints/yeasts.py:39 |

