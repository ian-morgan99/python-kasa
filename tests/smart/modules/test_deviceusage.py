"""Tests for DeviceUsage module."""

import pytest

from kasa import Module
from kasa.smart import SmartDevice

from ...device_fixtures import parametrize

device_usage = parametrize(
    "has device usage",
    component_filter="device",
    protocol_filter={"SMART"},
)


@device_usage
async def test_device_usage_features(dev: SmartDevice):
    """Test that device usage features are available when get_device_usage exists."""
    # Device needs a second update for get_device_usage data to be fetched
    # (DeviceModule is in FIRST_UPDATE_MODULES so it doesn't query on first update)
    await dev.update()
    
    device_usage_module = dev.modules.get(Module.DeviceUsage)
    
    # Module should only be present if device component version >= 2
    if device_usage_module is None:
        pytest.skip("DeviceUsage module not available for this device")
        return
    
    # If get_device_usage exists, features should be present
    if "get_device_usage" not in dev._last_update:
        pytest.skip("get_device_usage not available for this device")
        return
    
    usage_data = dev._last_update["get_device_usage"]
    
    # If usage_data is an error code, skip the test
    if not isinstance(usage_data, dict):
        pytest.skip("get_device_usage returned an error for this device")
        return
    
    # Check time_usage features
    if "time_usage" in usage_data:
        assert "time_usage_today" in device_usage_module._module_features
        assert "time_usage_past7" in device_usage_module._module_features
        assert "time_usage_past30" in device_usage_module._module_features
        
        assert device_usage_module.time_usage_today == usage_data["time_usage"]["today"]
        assert device_usage_module.time_usage_past7 == usage_data["time_usage"]["past7"]
        assert device_usage_module.time_usage_past30 == usage_data["time_usage"]["past30"]
    
    # Check power_usage features
    if "power_usage" in usage_data:
        assert "power_usage_today" in device_usage_module._module_features
        assert "power_usage_past7" in device_usage_module._module_features
        assert "power_usage_past30" in device_usage_module._module_features
        
        assert device_usage_module.power_usage_today == usage_data["power_usage"]["today"]
        assert device_usage_module.power_usage_past7 == usage_data["power_usage"]["past7"]
        assert device_usage_module.power_usage_past30 == usage_data["power_usage"]["past30"]
    
    # Check saved_power features
    if "saved_power" in usage_data:
        assert "saved_power_today" in device_usage_module._module_features
        assert "saved_power_past7" in device_usage_module._module_features
        assert "saved_power_past30" in device_usage_module._module_features
        
        assert device_usage_module.saved_power_today == usage_data["saved_power"]["today"]
        assert device_usage_module.saved_power_past7 == usage_data["saved_power"]["past7"]
        assert device_usage_module.saved_power_past30 == usage_data["saved_power"]["past30"]


@device_usage
async def test_device_usage_data_property(dev: SmartDevice):
    """Test the data property returns get_device_usage data."""
    # Need second update for data to be available
    await dev.update()
    
    device_usage_module = dev.modules.get(Module.DeviceUsage)
    
    if not device_usage_module:
        pytest.skip("DeviceUsage module not available for this device")
        return
    
    # data property should return get_device_usage from last_update if it's a dict
    # If get_device_usage returned an error, data should be an empty dict
    raw_data = dev._last_update.get("get_device_usage", {})
    if isinstance(raw_data, dict):
        assert device_usage_module.data == raw_data
    else:
        # Error code - should return empty dict
        assert device_usage_module.data == {}


@device_usage
async def test_device_usage_default_values(dev: SmartDevice):
    """Test that missing keys return 0 as default."""
    # Need second update for data to be available
    await dev.update()
    
    device_usage_module = dev.modules.get(Module.DeviceUsage)
    
    if not device_usage_module:
        pytest.skip("DeviceUsage module not available for this device")
        return
    
    # All properties should return integers (0 if missing)
    assert isinstance(device_usage_module.time_usage_today, int)
    assert isinstance(device_usage_module.time_usage_past7, int)
    assert isinstance(device_usage_module.time_usage_past30, int)
    assert isinstance(device_usage_module.power_usage_today, int)
    assert isinstance(device_usage_module.power_usage_past7, int)
    assert isinstance(device_usage_module.power_usage_past30, int)
    assert isinstance(device_usage_module.saved_power_today, int)
    assert isinstance(device_usage_module.saved_power_past7, int)
    assert isinstance(device_usage_module.saved_power_past30, int)
