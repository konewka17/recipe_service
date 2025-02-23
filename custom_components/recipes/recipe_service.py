from ruamel.yaml import YAML
import yaml
import os
import logging

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


def _update_recipe_sync(file_path, recipe_name, new_yaml):
    """Synchronous function for updating a recipe in YAML."""
    yaml_object = YAML()
    yaml_object.indent(mapping=2, sequence=4, offset=2)
    yaml_object.width = 4096

    # Load existing recipes
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
                return False

    if not updated:
        _LOGGER.info(f"Recipe {recipe_name} not found. Adding as a new recipe.")
        try:
            new_recipe = yaml.safe_load(new_yaml)
            new_recipe["id"] = recipe_name  # Ensure the new recipe has an ID
            recipes.append(new_recipe)
        except yaml.YAMLError as e:
            _LOGGER.error(f"Invalid YAML format: {e}")
            return False

    # Save back to YAML
    save_yaml(file_path, recipes, yaml_object)
    _LOGGER.info(f"Recipe {recipe_name} updated successfully.")
    return True
