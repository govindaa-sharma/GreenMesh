# agents/audit.py
import json
print("   [Audit] Appending plan decision to ledger...")

async def run(state, tools, llm, config=None):
    """
    Produce a signed explainability card for the approved plan and append to ledger.
    """
    plan = state.get('approved_plan')
    exec_res = state.get('execution_results', [])
    if not plan:
        return state
    card = {
        'plan_id': plan.get('id'),
        'plan_name': plan.get('name'),
        'rationale': plan.get('rationale'),
        'explain_card': plan.get('explain_card'),
        'execution': exec_res
    }
    # sign/append via tool
    ledger_entry = tools['append_ledger'](card)
    state.setdefault('audit_log', []).append(ledger_entry)
    state.setdefault('last_ledger_hash', ledger_entry.get('hash'))
    return state
