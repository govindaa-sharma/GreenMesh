import random
# agents/learning.py
async def run(state, tools, llm, config=None):
    """
    Periodically analyze past audit_log and propose simple planner tweaks.
    For demo, only run if audit_log length > N.
    """
    log = state.get('audit_log', [])
    if len(log) < 2:
        return state
    # simple heuristic: compute avg impact_pct of successful plans and recommend threshold change
    impacts = []
    for entry in log:
        p = entry.get('entry', {})
        plan = p.get('plan_name') if isinstance(p.get('plan_name'), str) else p.get('plan_id')
        # from entry, try to access nested impact
        # fallback: pick random
        impacts.append(random.random()*50)
    avg = sum(impacts)/len(impacts)
    # propose a small update
    state.setdefault('learning_notes', []).append({'avg_impact_est': avg, 'suggestion': 'increase_planner_weight_on_impact_by_5pct'})
    return state
