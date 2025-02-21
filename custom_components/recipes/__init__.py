"""Custom component to manage recipes in YAML."""
import logging
from homeassistant.core import HomeAssistant
from .const import DOMAIN, SERVICE_UPDATE_RECIPE
from .recipe_service import update_recipe

_LOGGER = logging.getLogger(__name__)

def setup(hass: HomeAssistant, config: dict):
    """Set up the custom component."""
    hass.services.register(DOMAIN, SERVICE_UPDATE_RECIPE, update_recipe)
    _LOGGER.info("Recipes custom component loaded.")
    return True
