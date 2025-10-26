# agents/executor.py
async def run(state, tools, llm, config=None):
    """
    Execute approved plan by calling executor tools (dispatch, sms).
    Execution results appended to state['execution_results'].
    """
    plan = state.get('approved_plan')
    if not plan:
        return state
    results = []
    # sandbox check: if high-risk, run digital twin simulation (already done in planner)
    if (plan.get('impact_pct',0) > 50) and state.get('safety_report', {}).get('verified') is False:
        # don't execute; require human
        state['execution_results'] = [{'status':'blocked_by_safety','plan_id':plan.get('id')}]
        return state

    # iterate steps
    for s in plan.get('steps', []):
        actor = s.get('actor')
        action = s.get('action', 'noop')
        # map to tool calls
        print(f"   [Executor] Executing action: {action} (Actor: {actor})")

        if action == 'dispatch_truck':
            num = s.get('count',1)
            res = tools.get('dispatch_tool', lambda *a,**k: {'ok':True})({'zone': plan.get('name'), 'count': num})
            results.append({'step':s,'result':res})
        else:
            # generic call
            res = {'ok':True, 'note':'simulated action'}
            results.append({'step':s,'result':res})
    state.setdefault('execution_results', []).extend(results)
    return state
