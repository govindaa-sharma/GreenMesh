# agents/negotiation.py
async def run(state, tools, llm, config=None):
    """
    Presents plans and accepts a human-approved plan.
    For CLI demo, auto-approve top plan unless 'manual_approve' in state is True.
    """
    plans = state.get('plans', [])
    if not plans:
        state['approved_plan'] = None
        return state
    if state.get('manual_approve', False):
        # in demo, this would be replaced with UI
        # here we keep system paused for human action (simulate by expecting external change)
        return state
    # auto-approve top plan
    state['approved_plan'] = plans[0]
    return state
