import streamlit as st
from library.config import set_data_root, read_dashboard_available_variables
from library.language import TEXTS

def _is_loaded(key):
    st.session_state[f"is_loaded_{key}"] = True

def controls_widget(variables):
    # State management
    data_root = set_data_root()

    SCENARIOS = read_dashboard_available_variables(data_root)

    # TARGET YEAR
    target_year_title = f'{TEXTS["Target year"]}'
    if len(SCENARIOS["target-year"]) > 1:
        if 'is_loaded_target_year' not in st.session_state:
            target_year = st.select_slider(target_year_title, options=SCENARIOS["target-year"], value=variables["target_year"], on_change=lambda: _is_loaded("target_year"))
        else:
            target_year = st.select_slider(target_year_title, options=SCENARIOS["target-year"])
    else:
        if SCENARIOS["target-year"][0] != variables["target_year"]:
            st.write("")
            st.write("It seems like you have a /api/config.json file that does not match the data in /api")
            return
        
        if 'is_loaded_target_year' not in st.session_state:
            target_year = st.select_slider(target_year_title, options=[SCENARIOS["target-year"][0], SCENARIOS["target-year"][0]], value=SCENARIOS["target-year"][0], on_change=lambda: _is_loaded("target_year"))
        else:
            target_year = st.select_slider(target_year_title, options=[SCENARIOS["target-year"][0], SCENARIOS["target-year"][0]])

    # SELF SUFFICIENCY
    self_sufficiency_title = f'{TEXTS["Self-sufficiency"]}'
    if len(SCENARIOS["self-sufficiency"]) > 1:
        if 'is_loaded_self_sufficiency' not in st.session_state:
            self_sufficiency = st.select_slider(self_sufficiency_title, options=SCENARIOS["self-sufficiency"], value=variables["self_sufficiency"], format_func=lambda x: f"{x:.0%}", on_change=lambda: _is_loaded("self_sufficiency"))
        else:
            self_sufficiency = st.select_slider(self_sufficiency_title, options=SCENARIOS["self-sufficiency"], format_func=lambda x: f"{x:.0%}")
    else:
        if SCENARIOS["self-sufficiency"][0] != variables["self_sufficiency"]:
            st.write("")
            st.write("It seems like you have a /api/config.json file that does not match the data in /api")
            return
        
        if 'is_loaded_self_sufficiency' not in st.session_state:
            self_sufficiency = st.select_slider(self_sufficiency_title, options=[SCENARIOS["self-sufficiency"][0], SCENARIOS["self-sufficiency"][0]], value=SCENARIOS["self-sufficiency"][0], format_func=lambda x: f"{x:.0%}", on_change=lambda: _is_loaded("self_sufficiency"))
        else:
            self_sufficiency = st.select_slider(self_sufficiency_title, options=[SCENARIOS["self-sufficiency"][0], SCENARIOS["self-sufficiency"][0]], format_func=lambda x: f"{x:.0%}")

    # ENERGY SCENARIO
    energy_scenario_title = f'{TEXTS["Energy scenario"]}'
    if len(SCENARIOS["energy-scenario"]) > 1:
        if 'is_loaded_energy_scenario' not in st.session_state:
            energy_scenario = st.select_slider(energy_scenario_title, options=SCENARIOS["energy-scenario"], value=variables["energy_scenario"], format_func=lambda x: f"{x:.0%}", on_change=lambda: _is_loaded("energy_scenario"))
        else:
            energy_scenario = st.select_slider(energy_scenario_title, options=SCENARIOS["energy-scenario"], format_func=lambda x: f"{x:.0%}")
    else:
        if SCENARIOS["energy-scenario"][0] != variables["energy_scenario"]:
            st.write("")
            st.write("It seems like you have a /api/config.json file that does not match the data in /api")
            return
        
        if 'is_loaded_energy_scenario' not in st.session_state:
            energy_scenario = st.select_slider(energy_scenario_title, options=[SCENARIOS["energy-scenario"][0], SCENARIOS["energy-scenario"][0]], value=SCENARIOS["energy-scenario"][0], format_func=lambda x: f"{x:.0%}", on_change=lambda: _is_loaded("energy_scenario"))
        else:
            energy_scenario = st.select_slider(energy_scenario_title, options=[SCENARIOS["energy-scenario"][0], SCENARIOS["energy-scenario"][0]], format_func=lambda x: f"{x:.0%}")

    # H2
    if 'is_loaded_h2' not in st.session_state:
        h2 = st.toggle(TEXTS["h2"], value=variables["h2"], disabled=(len(SCENARIOS["h2"]) == 1), on_change=lambda: _is_loaded("h2"))
    else:
       h2 = st.toggle(TEXTS["h2"], disabled=(len(SCENARIOS["h2"]) == 1))
    
    # OFFWIND
    offwind=True
    if 'is_loaded_offwind' not in st.session_state:
        offwind = st.toggle(TEXTS["Offshore"], value=(variables["offwind"]), disabled=(len(SCENARIOS["offwind"]) == 1), on_change=lambda: _is_loaded("offwind"))
    else:
        offwind = st.toggle(TEXTS["Offshore"], disabled=(len(SCENARIOS["offwind"]) == 1))

    # BIOGAS
    if len(SCENARIOS["biogas-limit"]) > 1:
        if 'is_loaded_biogas' not in st.session_state:
            biogas = st.select_slider(TEXTS["Biogas"], options=SCENARIOS["biogas-limit"], value=variables["biogas_limit"] if variables["biogas_limit"] in SCENARIOS["biogas-limit"] else SCENARIOS["biogas-limit"][0], format_func=lambda x: f"{x:.0%}", on_change=lambda: _is_loaded("biogas"))
        else:
            biogas = st.select_slider(TEXTS["Biogas"], options=SCENARIOS["biogas-limit"], format_func=lambda x: f"{x:.0%}")
    else:
        biogas = SCENARIOS["biogas-limit"][0]

    variables["target_year"] = target_year
    variables["self_sufficiency"] = self_sufficiency
    variables["energy_scenario"] = energy_scenario
    variables["h2"] = h2
    variables["offwind"] = offwind
    variables["biogas_limit"] = biogas

    return variables

def controls_readonly_widget(variables):
    # State management
    data_root = set_data_root()

    SCENARIOS = read_dashboard_available_variables(data_root)

    # SELF SUFFICIENCY
    if len(SCENARIOS["self-sufficiency"]) > 1:
        st.select_slider("", options=SCENARIOS["self-sufficiency"], value=variables["self_sufficiency"], disabled=True, label_visibility="hidden", key="readonly_self_sufficiency")
    else:
        st.select_slider("", options=[variables["self_sufficiency"], variables["self_sufficiency"]], value=variables["self_sufficiency"], disabled=True, label_visibility="hidden", key="readonly_self_sufficiency")

    # ENERGY SCENARIO
    if len(SCENARIOS["energy-scenario"]) > 1:
        st.select_slider("", options=SCENARIOS["energy-scenario"], value=variables["energy_scenario"], disabled=True, label_visibility="hidden", key="readonly_energy_scenario")
    else:
        st.select_slider("", options=[variables["energy_scenario"], variables["energy_scenario"]], value=variables["energy_scenario"], disabled=True, label_visibility="hidden", key="readonly_energy_scenario")

    # H2
    st.toggle("", value=(variables["h2"]), disabled=True, label_visibility="hidden", key="readonly_h2")

    # OFFWIND
    st.toggle("", value=(variables["offwind"]), disabled=True, label_visibility="hidden", key="readonly_offwind")

    # BIOGAS
    if len(SCENARIOS["biogas-limit"]) > 1:
        st.select_slider("", options=[variables["biogas_limit"], variables["biogas_limit"]], disabled=True, label_visibility="hidden", key="readonly_biogas")
