@state_trigger(
    "media_player.lg_webos_tv_oled65cs9la == 'on' or media_player.lg_webos_tv_oled65cs9la == 'off'"
)
def sync_denon_to_tv_power():
    current_state = state.get("media_player.lg_webos_tv_oled65cs9la")

    # whether state changes to on or off, ensure that the boolean starts with off by default
    service.call(
        "input_boolean", "turn_off", entity_id="input_boolean.change_denon_volume"
    )

    if current_state == "on":
        service.call("script", "turn_on_denon_and_lights")
    elif current_state == "off":
        service.call("script", "turn_off_denon_and_lights")


@state_trigger("sensor.current_lg_tv_volume")
def control_denon_volume_via_tv():
    """

    Volume changes on modern LG tv changes volume on old AVR through an IR / RF gateaway.

    This is a complex (and, unfortunately, hacky) function that employes several workarounds due to limitations in the LG
    intergration, Home Assistant, and the Broadlink IR / RF remote.

    LOGIC:
    Pressing volume up/down on the LG Magic Remote triggers this function, which tells the Broadlink
    to send an IR signal to the Denon 1908 to turn the volume up or down respectively.

    LIMITATIONS:
    - LG WebOS Integration:

      1) We do not know when the user actually presses any button on the remote. What we can know, is
         when the volume has changed. We do this through two custom sensors to track current and previous
         volume level, since Pyscript cannot reliably access a sensor's history.

      2) If the volume reported by WebOS reaches 100 or 0, no futher change in volume can be recorded.
         In other words, if TV volume is 100, further pressing up won't trigger the automation, therefore
         preventing us from incrasing the volume on the Denon 1908.
         (there is no way to sync the two incompatible devices)
      3) Keeping volume up/down pressed, will fire the automation hundreds of times per second. Broadlink
         cannot keep up with that, and we need to slow the function down/

    - Denon 1908 AVR:

      1) This AVR is nearly 20 years old, and has no smart feature. It can be controlled through an IR remote only.
         While, technically, it has HDMI-CEC capabilities, it simply does not work well with a modern TV such as the
         LG Oled in question.
      2) Therfore, the TV cannot directly control the audio of the Denon 1908 AVR.

    - Home Assistant:

      1) While vanilla HA can handle this automation, it would involve too many separate steps and scripts.
         I prefer having them all here, using Pyscript.

      2) Neither Pyscript nor HA supports traditional global varibles. Pyscript does not support classes like
         proper python does. Therefore, we use HA helper as global varibles.

      3) Pyscript cannot access sensor history since it is sandboxed. We use separate transitional sensors to
         overcome limitation.

      4) We canot use any form of delay like time.sleep(), since while the function can sleep, the input passed
         from the LG remote to the TV is independent of HA. In other words, there is nothing preventing the TV volume
         from incrasing if the user presses the volume buttons: we can only listen.


    """
    if state.get("media_player.lg_webos_tv_oled65cs9la") == "off":
        return

    # get the state of the sensors and save them into variable
    # faster than getting the state every time needed
    current_volume = state.get("sensor.current_lg_tv_volume")
    previous_volume = state.get("sensor.previous_lg_tv_volume")

    if (
        current_volume is None
        or previous_volume is None
        or current_volume == previous_volume
    ):
        return

    # This happens if the user keeps pressing up on the volume
    if state.get("input_boolean.change_denon_volume") == "on":
        service.call(
            "input_boolean", "turn_off", entity_id="input_boolean.change_denon_volume"
        )

        return  # Exit early to avoid re-triggering while adjusting the Denon volume

    service.call(
        "input_boolean", "turn_on", entity_id="input_boolean.change_denon_volume"
    )

    current_volume = int(current_volume)
    previous_volume = int(previous_volume)

    # Saving the entities in variable, for easy chagne in the future
    tv_entity_id = "media_player.lg_webos_tv_oled65cs9la"

    # the in-progress "variable" HA helper
    in_progress_entity_id = "input_boolean.changing_denon_volume_in_progress"

    # If volume increased
    if current_volume > previous_volume:
        _handle_volume_change("up", tv_entity_id, in_progress_entity_id, current_volume)

    # If volume decreased
    elif current_volume < previous_volume:
        _handle_volume_change(
            "down", tv_entity_id, in_progress_entity_id, current_volume
        )


def _handle_volume_change(
    direction, tv_entity_id, in_progress_entity_id, current_volume
):
    """
    Handle volume change for the Denon AVR and prevent TV volume from hitting 0 or 100 to keep the automation running.

    :param direction: Either "up" or "down", i.e. the direction the volume is changing.
    :param tv_entity_id: The entity ID of the LG TV media player.
    :param in_progress_entity_id: The entity ID of the helper used to track if the automation is in progress.
    """

    # if the automation is in progress, i.e. if it has been previously fired and is
    # currently running, do not call the broadlink command.
    if state.get(in_progress_entity_id) == "off":
        _adjust_denon_volume(in_progress_entity_id, direction)

    # No matter whether the Broadlink is in progress or not, if the user keeps pressing
    # volume, we need to handle it and avoid the sensor from ever reaching 100 or 0
    # Reset TV-only volume by moving it in the opposite direction of the Denon volume change

    # NOTE: this will automatically change the current_volume and previous_volume sensors,
    #       therefore firing the function again, but this automatic fire will return
    if direction == "up" and current_volume >= 99:
        service.call("media_player", "volume_down", entity_id=tv_entity_id)
    elif direction == "down" and current_volume <= 1:
        service.call("media_player", "volume_up", entity_id=tv_entity_id)

    service.call(
        "input_boolean", "turn_off", entity_id="input_boolean.change_denon_volume"
    )


def _adjust_denon_volume(in_progress_entity_id, direction):
    """
    Adjusts the volume of the Denon AVR by sending a command through a script,
    while ensuring the process is not interrupted by repeated commands.


    Args:
        in_progress_entity_id (str): The entity ID of the boolean helper
        direction (str): The direction of the volume adjustment, either "up" or "down".
    """
    # Save in a "variable" that the automation has started and the broadlink
    # command is in progress. Prevents multiple commands from being sent.
    service.call("input_boolean", "turn_on", entity_id=in_progress_entity_id)

    # Turns down / up the volume, and resets the boolean variable. In HA, this
    # acts like a  (HA calls are asynchronous), allowing the broadlink command
    # to complete, whiel the rest of this script continues.
    service.call(
        "script", "adjust_volume_denon_and_reset_boolean", volume_direction=direction
    )
