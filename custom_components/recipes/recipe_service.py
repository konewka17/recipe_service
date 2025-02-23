from ruamel.yaml import YAML
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

    recipes = load_yaml(file_path, yaml_object)

    try:
        new_recipe = YAML(typ="safe").load(new_yaml)
    except Exception as e:
        _LOGGER.error(f"Invalid YAML format: {e}")
        return False

    updated = False
    for recipe in recipes:
        if recipe.get("name") == recipe_name:
            recipe.update(new_recipe)
            updated = True
            break

    if not updated:
        _LOGGER.info(f"Recipe {recipe_name} not found. Adding as a new recipe.")
        recipes.append(new_recipe)

    save_yaml(file_path, recipes, yaml_object)
    _LOGGER.info(f"Recipe {recipe_name} updated successfully.")
    return True
