# agents/planner.py
import json, uuid

async def run(state, tools, llm, config=None):
    """
    Produce ranked plans using LLM + optimizer + digital twin.
    Output: state['plans'] = [ {id,name,steps,cost,time,confidence,explain_card}... ]
    """
    if state is None:
        state = {}

    incidents = state.get('situation_assessment', [])
    world = state.get('verified_world_state', {})
    plans = []

    print("   [Planner] Calling Gemini for planning...")

    # If no incidents detected, still generate a monitoring plan
    if not incidents:
        print("   [Planner] No incidents detected → creating monitor-only plan.")
        monitor_plan = {
            "id": f"p_monitor_{uuid.uuid4().hex[:6]}",
            "name": "monitor_environment",
            "steps": [{"actor": "Monitoring", "action": "observe"}],
            "confidence": 0.5,
            "rationale": ["no high-risk events detected"]
        }
        plans.append(monitor_plan)
    else:
        for inc in incidents:
            zone = inc.get('zone', 'unknown')
            # build a prompt for the LLM to create candidate plans
            prompt = (
                f"Planner: world={json.dumps(world)}\n"
                f"Incident={json.dumps(inc)}\n"
                f"Produce up to 3 plans with steps, required roles, and a short rationale. Output JSON."
            )
            planner_out = llm.call(prompt)

            # parse planner_out loosely using simulate fallback or try json
            try:
                parsed = json.loads(planner_out['text'])
                candidates = parsed.get('plans', []) if isinstance(parsed, dict) else []
            except Exception:
                # fallback: create two canned plans
                candidates = [
                    {'id': str(uuid.uuid4()), 'name': 'alert_and_dispatch',
                     'steps': [{'actor': 'Executor', 'action': 'dispatch_truck', 'count': 2}],
                     'confidence': 0.9},
                    {'id': str(uuid.uuid4()), 'name': 'monitor_only',
                     'steps': [{'actor': 'Monitoring', 'action': 'monitor'}],
                     'confidence': 0.6}
                ]

            # evaluate each candidate using digital twin
            ranked = []
            for c in candidates:
                name = c.get('name', c.get('id', 'plan'))
                print(f"   [Planner] Simulating plan '{name}' using digital_twin_simulate...")

                twin = tools['digital_twin_simulate'](c, world)
                entry = {
                    'id': c.get('id', str(uuid.uuid4())),
                    'name': name,
                    'steps': c.get('steps', []),
                    'cost': twin.get('cost', 0),
                    'time_min': twin.get('time_saved_min', 0),
                    'impact_pct': twin.get('damage_reduced_pct', 0),
                    'confidence': c.get('confidence', 0.7),
                    'rationale': c.get('rationale', ["No rationale provided"])
                }

                # attach explainability card via LLM
                try:
                    explain_prompt = f"Explainability for plan {name}: world={json.dumps(world)} plan={json.dumps(entry)}"
                    eout = llm.call(explain_prompt)
                    entry['explain_card'] = eout['text']
                except Exception:
                    entry['explain_card'] = "Simulated explanation"

                ranked.append(entry)

            # sort by confidence * impact
            ranked = sorted(ranked, key=lambda x: (x['confidence'] * x['impact_pct']), reverse=True)
            plans.extend(ranked[:3])

    state['plans'] = plans
    return state
