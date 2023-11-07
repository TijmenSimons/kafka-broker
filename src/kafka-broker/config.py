from configparser import ConfigParser


config_parser = ConfigParser()
config_parser.read("broker/base_config.ini")
base_config = dict(config_parser._sections)


def check_config(config: dict) -> dict:
    """Quick check if the config has the required settings."""
    
    general = config.get("general")
    if not general:
        raise AttributeError('"general" needs to be defined')

    cur_loc = general.get("current_location")
    if not cur_loc:
        raise AttributeError('"general:current_location" needs to be defined')
    
    return config
