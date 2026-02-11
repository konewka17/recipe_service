"""Recipe Editor Integration for Home Assistant."""
import logging
from homeassistant.core import HomeAssistant, ServiceCall

from .const import DOMAIN, SERVICE_UPDATE_RECIPE, SERVICE_CREATE_RECIPE
from .recipe_service import _update_recipe_sync, _create_recipe_sync

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Recipe Editor component."""

    async def update_recipe(call: ServiceCall):
        """Asynchronously update a recipe in recipes.yaml."""
        file_path = hass.config.path("www/recipes.yaml")
        recipe_name = call.data.get("recipe_name")
        new_yaml = call.data.get("new_yaml")
        printed = call.data.get("printed")

        if not recipe_name or (not new_yaml and not printed):
            _LOGGER.error("Missing required parameters: recipe_name or new_yaml / printed")
            return

        _LOGGER.info(f"Updating recipe {recipe_name} in {file_path}")

        # Run the file update in a separate thread to prevent blocking the event loop
        success = await hass.async_add_executor_job(_update_recipe_sync, file_path, recipe_name, new_yaml, printed)

        if not success:
            _LOGGER.error(f"Failed to update recipe {recipe_name}")

    async def create_recipe(call: ServiceCall):
        """Asynchronously create a new recipe in recipes.yaml."""
        file_path = hass.config.path("www/recipes.yaml")
        recipe_name = call.data.get("recipe_name")

        if not recipe_name:
            _LOGGER.error("Missing required parameter: recipe_name")
            return

        _LOGGER.info(f"Creating new recipe {recipe_name} in {file_path}")

        # Run the file creation in a separate thread to prevent blocking the event loop
        success = await hass.async_add_executor_job(_create_recipe_sync, file_path, recipe_name)

        if not success:
            _LOGGER.error(f"Failed to create recipe {recipe_name}")

    hass.services.async_register(DOMAIN, SERVICE_UPDATE_RECIPE, update_recipe)
    hass.services.async_register(DOMAIN, SERVICE_CREATE_RECIPE, create_recipe)
    _LOGGER.info("Recipe Editor integration loaded successfully")
    return True