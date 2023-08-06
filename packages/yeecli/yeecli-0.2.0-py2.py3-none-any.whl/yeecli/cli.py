import os
import sys

import click
import yeelight  # noqa
from yeelight import transitions as tr

try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser  # type: ignore

try:
    import tbvaccine

    tbvaccine.add_hook()
except:  # noqa
    pass

try:
    from . import __version__
except (SystemError, ValueError):
    from __init__ import __version__  # type: ignore

BULBS = []


def hex_color_to_rgb(color):
    """Convert a hex color string to an RGB tuple."""
    color = color.strip("#")
    try:
        red, green, blue = tuple(int(color[i : i + 2], 16) for i in (0, 2, 4))
    except (TypeError, ValueError):
        print("Unrecognized color, changing to red...", file=sys.stderr)
        red, green, blue = (255, 0, 0)
    return red, green, blue


def param_or_config(param, config, section, name, default):
    """Return a parameter, config item or default, in thar order of priority."""
    try:
        conf_param = config.get(section, name)
    except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
        conf_param = None

    try:
        # Try to see if this parameter is an integer.
        conf_param = int(conf_param)
    except (TypeError, ValueError):
        pass

    return param or conf_param or default


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(
    version=__version__, prog_name="yeecli", message="%(prog)s %(version)s: And there was light.",
)
@click.option("--ip", metavar="IP", help="The bulb's IP address.")
@click.option("--port", metavar="PORT", help="The bulb's port.", type=int)
@click.option(
    "--effect", "-e", metavar="EFFECT", help="The transition effect.", type=click.Choice(["smooth", "sudden"]),
)
@click.option(
    "--duration",
    "-d",
    metavar="DURATION_MS",
    help="The transition effect duration.",
    type=click.IntRange(1, 60000, clamp=True),
)
@click.option(
    "--bulb", "-b", metavar="NAME", default="default", help="The name of the bulb in the config file.", type=str,
)
@click.option(
    "--auto-on/--no-auto-on",
    default=True,
    help="Whether to turn the bulb on automatically before a command (on by default).",
)
def cli(ip, port, effect, duration, bulb, auto_on):
    """Easily control the YeeLight RGB LED lightbulb."""
    config = ConfigParser.ConfigParser()
    config.read([os.path.expanduser("~/.config/yeecli/yeecli.cfg")])

    ips = param_or_config(ip, config, bulb, "ip", None)
    port = param_or_config(port, config, bulb, "port", 55443)
    effect = param_or_config(effect, config, bulb, "effect", "sudden")
    duration = param_or_config(duration, config, bulb, "duration", 500)

    if not ips:
        click.echo("No IP address specified.")
        sys.exit(1)

    for ip in ips.split(","):
        ip = ip.strip()
        if ":" in ip:
            ip, prt = ip.split(":")
        else:
            # If no port is specified, use the default one.
            prt = port

        BULBS.append(yeelight.Bulb(ip=ip, port=prt, effect=effect, duration=duration, auto_on=auto_on,))


@cli.command()
@click.argument("value", type=click.IntRange(1, 100, clamp=True))
def brightness(value):
    """Set the brightness of the bulb."""
    click.echo("Setting the bulb to {} brightness...".format(value))
    for bulb in BULBS:
        bulb.set_brightness(value)


@cli.command()
@click.argument("degrees", type=click.IntRange(1700, 6500, clamp=True))
def temperature(degrees):
    """Set the color temperature of the bulb."""
    click.echo("Setting the bulb's color temperature to {}...".format(degrees))
    for bulb in BULBS:
        bulb.set_color_temp(degrees)


@cli.command()
@click.argument("hue", type=click.IntRange(0, 359, clamp=True))
@click.argument("saturation", type=click.IntRange(0, 100, clamp=True))
def hsv(hue, saturation):
    """Set the HSV value of the bulb."""
    click.echo("Setting the bulb to HSV {}, {}...".format(hue, saturation))
    for bulb in BULBS:
        bulb.set_hsv(hue, saturation)


@cli.command()
@click.argument("hex_color", type=str)
def rgb(hex_color):
    """Set the RGB value of the bulb."""
    red, green, blue = hex_color_to_rgb(hex_color)
    click.echo("Setting the bulb to RGB {}...".format(hex_color))
    for bulb in BULBS:
        bulb.set_rgb(red, green, blue)


@cli.command()
def toggle():
    """Toggle the bulb's state on or off."""
    click.echo("Toggling the bulb...")
    for bulb in BULBS:
        bulb.toggle()


@cli.command()
@click.argument("hex_color", type=str)
@click.option(
    "--pulses", "-p", metavar="COUNT", type=int, default=2, help="The number of times to pulse.",
)
def pulse(hex_color, pulses):
    """Pulse the bulb in a specific color."""
    red, green, blue = hex_color_to_rgb(hex_color)
    transitions = tr.pulse(red, green, blue)

    for bulb in BULBS:
        # Get the initial bulb state.
        if bulb.get_properties().get("power", "off") == "off":
            action = yeelight.Flow.actions.off
        else:
            action = yeelight.Flow.actions.recover

        bulb.start_flow(yeelight.Flow(count=pulses, action=action, transitions=transitions))


@cli.command()
@click.argument("state", type=click.Choice(["on", "off"]))
def turn(state):
    """Turn the bulb on or off."""
    click.echo("Turning the bulb {}...".format(state))
    for bulb in BULBS:
        if state == "on":
            bulb.turn_on()
        elif state == "off":
            bulb.turn_off()


@cli.group()
def preset():
    """Various presets."""


@preset.command()
def alarm():
    """Flash a red alarm."""
    click.echo("Alarm!")
    transitions = tr.alarm(500)
    flow = yeelight.Flow(count=0, transitions=transitions)
    for bulb in BULBS:
        bulb.start_flow(flow)


@preset.command()
def christmas():
    """Christmas lights."""
    click.echo("Happy holidays.")
    transitions = tr.christmas()
    flow = yeelight.Flow(count=0, transitions=transitions)
    for bulb in BULBS:
        bulb.start_flow(flow)


@preset.command()
@click.option(
    "--bpm", metavar="BPM", type=int, default=200, help="The beats per minute to pulse at.",
)
def disco(bpm):
    """Party."""
    click.echo("Party mode: activated.")
    flow = yeelight.Flow(count=0, transitions=tr.disco(bpm))
    for bulb in BULBS:
        bulb.start_flow(flow)


@preset.command()
@click.option(
    "-d",
    "--duration",
    metavar="DURATION",
    type=int,
    default=3000,
    help="The number of milliseconds to take for each change.",
)
def lsd(duration):
    """Color changes to a trippy palette."""
    click.echo("Enjoy your trip.")
    transitions = tr.lsd(duration=duration)
    flow = yeelight.Flow(count=0, transitions=transitions)
    for bulb in BULBS:
        bulb.start_flow(flow)


@preset.command()
def police():
    """Police lights."""
    click.echo("It's the fuzz!")
    transitions = tr.police()
    flow = yeelight.Flow(count=0, transitions=transitions)
    for bulb in BULBS:
        bulb.start_flow(flow)


@preset.command()
def police2():
    """More police lights."""
    click.echo("It's the fuzz again!")
    transitions = tr.police2()
    flow = yeelight.Flow(count=0, transitions=transitions)
    for bulb in BULBS:
        bulb.start_flow(flow)


@preset.command()
@click.option(
    "-d",
    "--duration",
    metavar="DURATION",
    type=int,
    default=750,
    help="The number of milliseconds to take for each change.",
)
def random(duration):
    """Random colors."""
    click.echo("Random colors!")
    transitions = tr.randomloop(duration=duration)
    flow = yeelight.Flow(count=0, transitions=transitions)
    for bulb in BULBS:
        bulb.start_flow(flow)


@preset.command()
def redgreenblue():
    """Change from red to green to blue."""
    click.echo("Pretty colors.")
    transitions = tr.rgb()
    flow = yeelight.Flow(count=0, transitions=transitions)
    for bulb in BULBS:
        bulb.start_flow(flow)


@preset.command()
def slowdown():
    """Cycle with increasing transition time."""
    click.echo("Sloooooowwwwlllyyy..")
    transitions = tr.slowdown()
    flow = yeelight.Flow(count=0, transitions=transitions)
    for bulb in BULBS:
        bulb.start_flow(flow)


@preset.command()
def strobe():
    """Epilepsy warning."""
    click.echo("Strobing.")
    transitions = tr.strobe()
    flow = yeelight.Flow(count=0, transitions=transitions)
    for bulb in BULBS:
        bulb.start_flow(flow)


@preset.command()
def temp():
    """Slowly-changing color temperature."""
    click.echo("Enjoy.")
    transitions = tr.temp()
    flow = yeelight.Flow(count=0, transitions=transitions)
    for bulb in BULBS:
        bulb.start_flow(flow)


@preset.command()
@click.option(
    "-d",
    "--duration",
    metavar="DURATION",
    type=click.IntRange(50, 24 * 60 * 60),
    default=5 * 60,
    help="The number of seconds until the bulb reaches full color.",
)
def sunrise(duration):
    """Simulate sunrise in seconds (default 5min)."""
    click.echo("Good morning!")
    # We're using seconds for duration because it's a more natural timescale
    # for this preset.
    duration = duration * 1000
    transitions = [
        # First set to minimum temperature, low brightness, nearly immediately.
        tr.TemperatureTransition(1700, duration=50, brightness=1),
        # Then slowly transition to higher temperature, max brightness.
        # 5000 is about regular daylight white.
        tr.TemperatureTransition(2100, duration=duration / 2, brightness=50),
        tr.TemperatureTransition(5000, duration=duration / 2, brightness=100),
    ]
    flow = yeelight.Flow(count=1, action=yeelight.flow.Action.stay, transitions=transitions)
    for bulb in BULBS:
        bulb.start_flow(flow)


@preset.command()
def stop():
    """Stop any currently playing presets and return to the prior state."""
    for bulb in BULBS:
        bulb.stop_flow()


@cli.command()
def save():
    """Save the current settings as default."""
    click.echo("Saving settings...")
    for bulb in BULBS:
        bulb.set_default()


@cli.command()
def status():
    """Show the bulb's status."""
    for bulb in BULBS:
        click.echo("\nBulb parameters:")
        for key, value in bulb.get_properties().items():
            if key == "rgb":
                try:
                    value = hex(int(value)).replace("0x", "#")
                except TypeError:
                    # Ignore exception on white-only bulbs.
                    pass
            click.echo("* {}: {}".format(key, value))


if __name__ == "__main__":
    cli()
