import logging
import json

from pyIndego import IndegoClient

logging.basicConfig(filename="pyIndego.log", level=logging.DEBUG)
_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)


def main(config):
    with IndegoClient(**config) as indego:
        # print("=[alerts]====")
        indego.update_state()
        print(indego.state)
        indego.update_state(longpoll=True, longpoll_timeout=20)
        print(indego.state)
        indego.update_alerts()
        print(indego.alerts)
        # print("=[alerts_count]====")
        # print(indego.alerts_count)

        # print("=[generic_data]====")
        # indego.update_generic_data()
        # print(indego.generic_data)

        # print("=[last_completed_mow]====")
        # indego.update_last_completed_mow()
        # print(indego.last_completed_mow)

        # print("=[location]====")
        # indego.update_location()
        # print(indego.location)

        # print("=[longpoll_state]====")
        # indego.update_longpoll_state(40)
        # print(indego.longpoll_state)

        # indego.update_network()
        # print(indego.network)
        # indego.update_all(force=True)
        # print(indego)
        # print("=[state]====")
        # indego.update_state()
        # print(indego.state)
        
        print(" ")
        print("=[alerts]====")
        indego.update_alerts()
        print(indego.alerts)
        print("=[alerts_count]====")
        print(indego.alerts_count)

        print(" ")
        print("=[generic_data]====")
        indego.update_generic_data()
        print(indego.generic_data)

        print(" ")
        print("=[last_completed_mow]====")
        indego.update_last_completed_mow()
        print(indego.last_completed_mow)

        print(" ")
        print("=[location]====")
        indego.update_location()
        print(indego.location)

        # print("=[longpoll_state]====")
        # indego.update_longpoll_state(40)
        # print(indego.longpoll_state)

        print(" ")
        print("=[operating data]====")
        indego.update_operating_data()
        print(indego.operating_data)

        # indego.update_network()
        # print(indego.network)

        # indego.update_all(force=True)
        # print(indego)

        print("=[state]====")
        indego.update_state()
        print(indego.state)

        # indego.update_next_mow()
        # indego.update_operating_data()
        # # indego.update_updates()
        # # indego.update_users()
        # # indego.update_network()
        
        print("=[updates]====")
        indego.update_updates_available()
        print(indego.update_available)
        print(" ")
        print("=[users]====")
        indego.update_users()
        print(indego.users)
        # indego.update_network()

        # indego.download_map()

        # print("map: ", indego.map_filename)
        # print("network ", indego.network)
        # print("state: ", indego.state)
        # print("users: ", indego.users)
        # print("Generic data: ", indego.generic_data)
        # print("Generic data min voltage: ", indego.generic_data.model_voltage.min)
        # print("Alerts: ", indego.alerts)
        # print("Operating_data: ", indego.operating_data)
        # print("Battery: ", indego.operating_data.battery)
        # print("Battery percent: ", indego.operating_data.battery.percent_adjusted)
        # print("Battery voltage: ", indego.operating_data.battery.voltage)
        # # indego.update_generic_data()
        # print("Battery: ", indego.operating_data.battery)
        # print("Session charge: ", indego.operating_data.runtime.session.charge)

        # print("Next mow: ", indego.next_mow)
        print(" ")
        indego.update_next_mow()
        print("Next mow: ", indego.next_mow)

        # print("location: ", indego.location)
        # print("last mow: ", indego.last_completed_mow)
        # print(indego.generic_data.alm_mode)
        # print(indego.alm_name)
        # print(indego.service_counter)
        # print(indego.needs_service)
        # print(indego.alm_mode)
        # print(indego.bare_tool_number)
        # print(indego.alm_firmware_version)
        # print(indego.model_description)
        # print(indego.model_voltage)
        # print(indego.mowing_mode_description)
        # print(indego.model_description)
        # print(indego.model_description)
        # print(indego.mower_state)
        # print(indego.mower_state_description)
        # print(indego.mower_state_description_detailed)
        # print(indego.battery)
        # print(indego.email)
        # print(indego.garden)
        # print(indego.x_pos, ", ", indego.y_pos)
        # indego.show_vars()


if __name__ == "__main__":
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
    main(config)
