# agents/fusion.py
from collections import defaultdict
import json

async def run(state, tools, llm, config=None):
    """
    Look at last N perception_events and produce merged world_state.
    Uses LLM for a short natural language summary (optional).
    """
    events = state.get('perception_events', [])[-20:]
    zones = defaultdict(lambda: {'water': [], 'garbage': []})
    for ev in events:
        stype = ev.get('sensor_type','').lower()
        if 'water' in stype:
            zones[ev['location']]['water'].append(ev['value'])
        elif 'garbage' in stype:
            zones[ev['location']]['garbage'].append(ev['value'])
    world = {}
    for z, vals in zones.items():
        world[z] = {
            'avg_water': round(sum(vals['water'])/len(vals['water']),2) if vals['water'] else None,
            'avg_garbage': round(sum(vals['garbage'])/len(vals['garbage']),2) if vals['garbage'] else None
        }

    state['world_state'] = world

    # optional LLM short summary
    try:
        prompt = f"fusion\nworld: {json.dumps(world)}\nSummarize in one short sentence."
        llm_out = llm.call(prompt)
        state.setdefault('summaries', []).append({'agent':'fusion','text': llm_out['text']})
    except Exception:
        pass
    return state
