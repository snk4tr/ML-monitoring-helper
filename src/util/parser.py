def parse_output(output):
    """
    Parses console outputs of performed commands.
    Args:
        output (dict): dict, a part of which may be used as a generator object (host_out.stdout) for retrieving
        lines of console output.
    Returns:
        (str) sting of all console output.
    """
    out = ""
    for host, host_out in output.items():
        for line in host_out.stdout:
            out += line + " "
    return out