from ruamel.yaml import YAML
import yaml
import os
import logging
from homeassistant.core import HomeAssistant, ServiceCall

_LOGGER = logging.getLogger(__name__)

def load_yaml(file_path, yaml_object):
    """Load YAML file safely."""
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r", encoding="utf-8") as file:
        return yaml_object.load(file) or []

def save_yaml(file_path, data, yaml_object):
    """Save YAML file safely."""
    with open(file_path, "w", encoding="utf-8") as file:
        yaml_object.dump(data, file)

def update_recipe(hass: HomeAssistant, call: ServiceCall):
    """Update a recipe in recipes.yaml."""
    file_path = hass.config.path("www/recipes.yaml")

    recipe_name = call.data.get("recipe_name")
    new_yaml = call.data.get("new_yaml")

    if not recipe_name or not new_yaml:
        _LOGGER.error("Missing required parameters: recipe_name or new_yaml")
        return

    _LOGGER.info(f"Updating recipe {recipe_name} in {file_path}")

    # Load existing recipes
    yaml_object = YAML()
    yaml_object.indent(mapping=2, sequence=4, offset=2)
    recipes = load_yaml(file_path, yaml_object)

    # Find and update the recipe
    updated = False
    for recipe in recipes:
        if recipe.get("name") == recipe_name:
            try:
                updated_data = yaml.safe_load(new_yaml)  # Validate YAML structure
                recipe.update(updated_data)
                updated = True
            except yaml.YAMLError as e:
                _LOGGER.error(f"Invalid YAML format: {e}")
                return

    if not updated:
        _LOGGER.info(f"Recipe with ID {recipe_name} not found. Adding as a new recipe.")
        try:
            new_recipe = yaml.safe_load(new_yaml)
            new_recipe["id"] = recipe_name  # Ensure the new recipe has an ID
            recipes.append(new_recipe)
        except yaml.YAMLError as e:
            _LOGGER.error(f"Invalid YAML format: {e}")
            return

    # Save back to YAML
    save_yaml(file_path, recipes, yaml_object)
    _LOGGER.info(f"Recipe {recipe_name} updated successfully.")
