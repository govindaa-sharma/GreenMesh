# agents/coalition.py
async def run(state, tools, llm, config=None):
    """
    Decide which agent roles to involve for each incident.
    Simple mapping: severity->roles
    """
    incidents = state.get('situation_assessment', [])
    coalitions = []
    for inc in incidents:
        sev = inc['severity']
        roles = ['Planner','Executor','Audit']
        if sev>=3:
            roles += ['PublicComm','Traffic']
        if sev>=4:
            roles += ['EmergencyResponse']
        coalitions.append({'zone': inc['zone'], 'roles': roles})
    state['coalitions'] = coalitions
    return state
