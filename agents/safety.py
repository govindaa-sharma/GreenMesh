# agents/safety.py
async def run(state, tools, llm, config=None):
    """
    Verify fused world state vs perception provenance. Use tools.detect_adversarial.
    Adds 'verified_world_state' and 'quarantine_list' to state.
    """
    events = state.get('perception_events', [])[-50:]
    flags = tools['detect_adversarial'](events)
    state['quarantine_list'] = flags
    if flags:
        # mark suspicious: remove suspicious sensors from world state for now
        state['verified_world_state'] = state.get('world_state', {}).copy()
        # simple removal: if sensor in flags, zero out affected zones (demo logic)
        for f in flags:
            sid = f.get('sensor_id')
            # naive: if sensor_id contains zone or map to zone (demo)
            # For demo we simply set 'verified' False
        state['safety_report'] = {'verified': False, 'flags': flags}
    else:
        state['verified_world_state'] = state.get('world_state', {})
        state['safety_report'] = {'verified': True, 'flags': []}

    # Also ask the LLM for a short human explanation (optional)
    try:
        prompt = f"safety check\nworld_state:{state.get('world_state')}\nflags:{flags}\nExplain."
        resp = llm.call(prompt)
        state.setdefault('safety_notes', []).append(resp['text'])
    except Exception:
        pass

    return state
