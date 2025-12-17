"""Implementation of device usage module."""

from __future__ import annotations

from ...feature import Feature
from ..smartmodule import SmartModule


class DeviceUsage(SmartModule):
    """Implementation of device usage statistics.
    
    This module exposes time_usage, power_usage, and saved_power statistics
    that are already being retrieved by the DeviceModule's get_device_usage query.
    """

    REQUIRED_COMPONENT = "device"

    async def _post_update_hook(self) -> None:
        """Perform actions after a device update.
        
        Initialize features here instead of _initialize_features because
        get_device_usage data is not available on the first update (DeviceModule
        is in FIRST_UPDATE_MODULES so it doesn't query on first update).
        """
        # Only initialize features once, and only when data is available
        if self._module_features or "get_device_usage" not in self._device._last_update:
            return

        usage_data = self._device._last_update.get("get_device_usage", {})

        # Time usage features (in minutes)
        if "time_usage" in usage_data:
            self._add_feature(
                Feature(
                    self._device,
                    id="time_usage_today",
                    name="Time usage today",
                    container=self,
                    attribute_getter="time_usage_today",
                    icon="mdi:clock-outline",
                    unit_getter=lambda: "min",
                    category=Feature.Category.Info,
                    type=Feature.Type.Sensor,
                )
            )
            self._add_feature(
                Feature(
                    self._device,
                    id="time_usage_past7",
                    name="Time usage past 7 days",
                    container=self,
                    attribute_getter="time_usage_past7",
                    icon="mdi:clock-outline",
                    unit_getter=lambda: "min",
                    category=Feature.Category.Info,
                    type=Feature.Type.Sensor,
                )
            )
            self._add_feature(
                Feature(
                    self._device,
                    id="time_usage_past30",
                    name="Time usage past 30 days",
                    container=self,
                    attribute_getter="time_usage_past30",
                    icon="mdi:clock-outline",
                    unit_getter=lambda: "min",
                    category=Feature.Category.Info,
                    type=Feature.Type.Sensor,
                )
            )

        # Power usage features (in Wh)
        if "power_usage" in usage_data:
            self._add_feature(
                Feature(
                    self._device,
                    id="power_usage_today",
                    name="Power usage today",
                    container=self,
                    attribute_getter="power_usage_today",
                    icon="mdi:lightning-bolt",
                    unit_getter=lambda: "Wh",
                    category=Feature.Category.Info,
                    type=Feature.Type.Sensor,
                )
            )
            self._add_feature(
                Feature(
                    self._device,
                    id="power_usage_past7",
                    name="Power usage past 7 days",
                    container=self,
                    attribute_getter="power_usage_past7",
                    icon="mdi:lightning-bolt",
                    unit_getter=lambda: "Wh",
                    category=Feature.Category.Info,
                    type=Feature.Type.Sensor,
                )
            )
            self._add_feature(
                Feature(
                    self._device,
                    id="power_usage_past30",
                    name="Power usage past 30 days",
                    container=self,
                    attribute_getter="power_usage_past30",
                    icon="mdi:lightning-bolt",
                    unit_getter=lambda: "Wh",
                    category=Feature.Category.Info,
                    type=Feature.Type.Sensor,
                )
            )

        # Saved power features (in Wh)
        if "saved_power" in usage_data:
            self._add_feature(
                Feature(
                    self._device,
                    id="saved_power_today",
                    name="Saved power today",
                    container=self,
                    attribute_getter="saved_power_today",
                    icon="mdi:leaf",
                    unit_getter=lambda: "Wh",
                    category=Feature.Category.Info,
                    type=Feature.Type.Sensor,
                )
            )
            self._add_feature(
                Feature(
                    self._device,
                    id="saved_power_past7",
                    name="Saved power past 7 days",
                    container=self,
                    attribute_getter="saved_power_past7",
                    icon="mdi:leaf",
                    unit_getter=lambda: "Wh",
                    category=Feature.Category.Info,
                    type=Feature.Type.Sensor,
                )
            )
            self._add_feature(
                Feature(
                    self._device,
                    id="saved_power_past30",
                    name="Saved power past 30 days",
                    container=self,
                    attribute_getter="saved_power_past30",
                    icon="mdi:leaf",
                    unit_getter=lambda: "Wh",
                    category=Feature.Category.Info,
                    type=Feature.Type.Sensor,
                )
            )
        
        # After adding features, we need to register them with the device
        # This is normally done in _initialize_features, but we're doing it here
        for feat in self._module_features.values():
            self._device._add_feature(feat)

    def query(self) -> dict:
        """Query to execute during the update cycle."""
        # DeviceModule already queries get_device_usage, so we don't need to
        return {}

    @property
    def time_usage_today(self) -> int:
        """Return time usage for today in minutes."""
        return self.data.get("time_usage", {}).get("today", 0)

    @property
    def time_usage_past7(self) -> int:
        """Return time usage for past 7 days in minutes."""
        return self.data.get("time_usage", {}).get("past7", 0)

    @property
    def time_usage_past30(self) -> int:
        """Return time usage for past 30 days in minutes."""
        return self.data.get("time_usage", {}).get("past30", 0)

    @property
    def power_usage_today(self) -> int:
        """Return power usage for today in Wh."""
        return self.data.get("power_usage", {}).get("today", 0)

    @property
    def power_usage_past7(self) -> int:
        """Return power usage for past 7 days in Wh."""
        return self.data.get("power_usage", {}).get("past7", 0)

    @property
    def power_usage_past30(self) -> int:
        """Return power usage for past 30 days in Wh."""
        return self.data.get("power_usage", {}).get("past30", 0)

    @property
    def saved_power_today(self) -> int:
        """Return saved power for today in Wh."""
        return self.data.get("saved_power", {}).get("today", 0)

    @property
    def saved_power_past7(self) -> int:
        """Return saved power for past 7 days in Wh."""
        return self.data.get("saved_power", {}).get("past7", 0)

    @property
    def saved_power_past30(self) -> int:
        """Return saved power for past 30 days in Wh."""
        return self.data.get("saved_power", {}).get("past30", 0)

    @property
    def data(self) -> dict:
        """Return device usage data from the last update."""
        data = self._device._last_update.get("get_device_usage", {})
        # If get_device_usage returned an error, data might be an error code
        # In that case, return an empty dict
        if not isinstance(data, dict):
            return {}
        return data

    async def _check_supported(self) -> bool:
        """Check if the module is supported by the device."""
        # Only supported if device component version >= 2
        # get_device_usage will be available after the first modular update
        return self.supported_version >= 2
