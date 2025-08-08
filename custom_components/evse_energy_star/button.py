import logging
from datetime import datetime
from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    device_name_slug = hass.data[DOMAIN][entry.entry_id]["device_name_slug"]

    async_add_entities([
        SyncTimeButton(coordinator, entry, device_name_slug),
        ChargeNowButton(coordinator, entry, device_name_slug)
    ])

class SyncTimeButton(CoordinatorEntity, ButtonEntity):
    def __init__(self, coordinator, config_entry: ConfigEntry, slug: str):
        super().__init__(coordinator)
        self.coordinator = coordinator
        self.config_entry = config_entry
        self._attr_translation_key = "evse_energy_star_time_get"
        self._attr_unique_id = f"time_get_{config_entry.entry_id}"
        self._attr_icon = "mdi:clock-check-outline"
        self._attr_should_poll = False
        self._attr_has_entity_name = True
        self._attr_suggested_object_id = f"{slug}_{self._attr_translation_key}"

    async def async_press(self):
        try:
            raw_tz = self.coordinator.data.get("timeZone", 0)
            try:
                tz = int(float(str(raw_tz).strip()))
            except Exception:
                tz = 0
                _LOGGER.warning("button.py → невірне значення timeZone: '%s'", raw_tz)

            local_ts = int(datetime.now().timestamp())
            system_time = local_ts + tz * 3600
            _LOGGER.debug("button.py → Синхронізація часу: systemTime=%s", system_time)

            session = async_get_clientsession(self.coordinator.hass)
            await session.post(
                f"http://{self.coordinator.host}/pageEvent",
                data=f"systemTime={system_time}",
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )

        except Exception as err:
            _LOGGER.error("button.py → помилка синхронізації часу: %s", repr(err))

    @property
    def available(self):
        return self.coordinator.last_update_success

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.config_entry.entry_id)},
            "name": self.config_entry.data.get("device_name", "Eveus Pro"),
            "manufacturer": "Energy Star",
            "model": "EVSE",
            "sw_version": self.coordinator.data.get("fwVersion")
        }

class ChargeNowButton(CoordinatorEntity, ButtonEntity):
    def __init__(self, coordinator, config_entry: ConfigEntry, slug: str):
        super().__init__(coordinator)
        self.coordinator = coordinator
        self.config_entry = config_entry
        self._attr_translation_key = "evse_energy_star_start_now"
        self._attr_unique_id = f"start_now_{config_entry.entry_id}"
        self._attr_icon = "mdi:battery-charging-high"
        self._attr_should_poll = False
        self._attr_has_entity_name = True
        self._attr_suggested_object_id = f"{slug}_{self._attr_translation_key}"

    async def async_press(self):
        try:
            data = self.coordinator.data
            tz_raw = data.get("timeZone", 0)
            try:
                tz = int(float(str(tz_raw).strip()))
            except Exception:
                tz = 0
                _LOGGER.warning("chargeNow → невірне значення timeZone: '%s'", tz_raw)

            start = data.get("startTime", "23:00")
            stop = data.get("stopTime", "07:00")
            session = async_get_clientsession(self.coordinator.hass)

            await session.post(
                f"http://{self.coordinator.host}/pageEvent",
                data="oneCharge=0",
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )

            await session.post(
                f"http://{self.coordinator.host}/pageEvent",
                data="evseEnabled=1",
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )

            payload_timer = f"isAlarm=false&startTime={start}&stopTime={stop}&timeZone={tz}"
            await session.post(
                f"http://{self.coordinator.host}/timer",
                data=payload_timer,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            _LOGGER.debug("chargeNow → /timer: %s", payload_timer)

            await session.post(
                f"http://{self.coordinator.host}/pageEvent",
                data="timeLimit=500000",
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            await session.post(
                f"http://{self.coordinator.host}/pageEvent",
                data="energyLimit=10000",
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            await session.post(
                f"http://{self.coordinator.host}/pageEvent",
                data="chargeNow=12",
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )

            _LOGGER.debug("chargeNow → Зарядка активована")

        except Exception as err:
            _LOGGER.error("chargeNow → помилка запиту: %s", repr(err))

    @property
    def available(self):
        return self.coordinator.last_update_success

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.config_entry.entry_id)},
            "name": self.config_entry.data.get("device_name", "Eveus Pro"),
            "manufacturer": "Energy Star",
            "model": "EVSE",
            "sw_version": self.coordinator.data.get("fwVersion")
        }
