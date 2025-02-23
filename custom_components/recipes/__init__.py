"""Recipe Editor Integration for Home Assistant."""
import logging
from homeassistant.core import HomeAssistant, ServiceCall

from .const import DOMAIN, SERVICE_UPDATE_RECIPE
from .recipe_service import _update_recipe_sync

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Recipe Editor component."""

    async def update_recipe(call: ServiceCall):
        """Asynchronously update a recipe in recipes.yaml."""
        file_path = hass.config.path("www/recipes.yaml")
        recipe_name = call.data.get("recipe_name")
        new_yaml = call.data.get("new_yaml")

        if not recipe_name or not new_yaml:
            _LOGGER.error("Missing required parameters: recipe_name or new_yaml")
            return

        _LOGGER.info(f"Updating recipe {recipe_name} in {file_path}")

        # Run the file update in a separate thread to prevent blocking the event loop
        success = await hass.async_add_executor_job(_update_recipe_sync, file_path, recipe_name, new_yaml)

        if not success:
            _LOGGER.error(f"Failed to update recipe {recipe_name}")

    hass.services.async_register(DOMAIN, SERVICE_UPDATE_RECIPE, update_recipe)
    _LOGGER.info("Recipe Editor integration loaded successfully")
    return True
