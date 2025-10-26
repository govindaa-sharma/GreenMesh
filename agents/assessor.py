# agents/assessor.py
async def run(state, tools, llm, config=None):
    """
    From verified_world_state, produce situation_assessment:
    a list of incidents with severity, est_population, legal_flags.
    """
    world = state.get('verified_world_state', {})
    incidents = []
    for zone, vals in world.items():
        sev = 0
        if vals.get('avg_water') and vals['avg_water'] >= 2.5: sev = max(sev, 3)
        if vals.get('avg_garbage') and vals['avg_garbage'] >= 90: sev = max(sev, 2)
        if sev>0:
            incidents.append({
                'zone': zone,
                'severity': sev,
                'estimated_people': 1000*sev,  # demo heuristic
                'notes': []
            })
    state['situation_assessment'] = incidents

    # LLM add: short assessment
    try:
        prompt = f"assess\nincidents:{incidents}\nReturn 1-line summary."
        resp = llm.call(prompt)
        state.setdefault('assessor_notes',[]).append(resp['text'])
    except Exception:
        pass

    return state
