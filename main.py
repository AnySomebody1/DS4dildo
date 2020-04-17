import evdev
from evdev import ecodes, InputDevice, ff

# Find first EV_FF capable event device (that we have permissions to use).
for name in evdev.list_devices():
    dev = InputDevice(name)
    if ecodes.EV_FF in dev.capabilities():
        break

rumble = ff.Rumble(strong_magnitude=0x0000, weak_magnitude=0xffff)
effect_type = ff.EffectType(ff_rumble_effect=rumble)
duration_ms = 1000

effect = ff.Effect(
    ecodes.FF_RUMBLE, -1, 0,
    ff.Trigger(0, 0),
    ff.Replay(duration_ms, 0),
    ff.EffectType(ff_rumble_effect=rumble)
)

# ie.type = EV_FF;
# ie.code = FF_GAIN;
# ie.value = 0xFFFFUL * gain / 100;

repeat_count = 10
effect_id = dev.upload_effect(effect)
dev.write(ecodes.EV_FF, effect_id, repeat_count)
input()
dev.erase_effect(effect_id)

