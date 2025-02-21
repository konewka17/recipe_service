import yaml
import os
import logging
from homeassistant.core import HomeAssistant, ServiceCall
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

def load_yaml(file_path):
    """Load YAML file safely."""
    if not os.path.exists(file_path):
        return {"recipes": []}  # Ensure a valid format if file doesn't exist
    with open(file_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file) or {"recipes": []}

def save_yaml(file_path, data):
    """Save YAML file safely."""
    with open(file_path, "w", encoding="utf-8") as file:
        yaml.safe_dump(data, file, default_flow_style=False, allow_unicode=True)

def update_recipe(hass: HomeAssistant, call: ServiceCall):
    """Update a recipe in recipes.yaml."""
    file_path = hass.config.path("www/recipes.yaml")

    recipe_id = call.data.get("recipe_id")
    new_yaml = call.data.get("new_yaml")

    if not recipe_id or not new_yaml:
        _LOGGER.error("Missing required parameters: recipe_id or new_yaml")
        return

    _LOGGER.info(f"Updating recipe {recipe_id} in {file_path}")

    # Load existing recipes
    data = load_yaml(file_path)
    recipes = data.get("recipes", [])

    # Find and update the recipe
    updated = False
    for recipe in recipes:
        if recipe.get("id") == recipe_id:
            try:
                updated_data = yaml.safe_load(new_yaml)  # Validate YAML structure
                recipe.update(updated_data)
                updated = True
            except yaml.YAMLError as e:
                _LOGGER.error(f"Invalid YAML format: {e}")
                return

    if not updated:
        _LOGGER.warning(f"Recipe with ID {recipe_id} not found.")
        return

    # Save back to YAML
    save_yaml(file_path, {"recipes": recipes})
    _LOGGER.info(f"Recipe {recipe_id} updated successfully.")
