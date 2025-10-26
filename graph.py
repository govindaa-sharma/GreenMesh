# graph.py
import asyncio, time, json
from llm_wrapper import LLM
import tools
from importlib import import_module

# ANSI colors for prettier terminal logs
class Colors:
    AGENT = "\033[96m"
    TOOL = "\033[92m"
    RESULT = "\033[93m"
    RESET = "\033[0m"
    ERROR = "\033[91m"

AGENTS = [
    'agents.perception',
    'agents.fusion',
    'agents.safety',
    'agents.assessor',
    'agents.coalition',
    'agents.planner',
    'agents.negotiation',
    'agents.executor',
    'agents.audit',
    'agents.learning'
]

def log_agent(name, message):
    print(f"{Colors.AGENT}[Agent: {name}] {Colors.RESET}{message}")

def log_tool(name, message):
    print(f"   {Colors.TOOL}[Tool: {name}] {Colors.RESET}{message}")

def log_result(message):
    print(f"      {Colors.RESULT}→ {message}{Colors.RESET}")

async def run_graph(iterations=10, manual_approve=False):
    state = {
        'manual_approve': manual_approve,
        'perception_events': [],
        'audit_log': [],
    }

    csv_gen = tools.csv_stream("data/simulated_sensors.csv")
    toolset = {
        'csv_gen': csv_gen,
        'digital_twin_simulate': tools.digital_twin_simulate,
        'detect_adversarial': tools.detect_adversarial,
        'simple_optimizer': tools.simple_optimizer,
        'append_ledger': tools.append_ledger,
        'dispatch_tool': lambda payload: {'ok': True, 'payload': payload}
    }

    llm = LLM()
    agent_funcs = [(a.split('.')[-1], import_module(a).run) for a in AGENTS]

    for tick in range(iterations):
        print(f"\n{Colors.RESULT}=== TICK {tick+1} START ==={Colors.RESET}")
        for agent_name, func in agent_funcs:
            try:
                log_agent(agent_name, "Running...")
                before = json.dumps(state.get("world_state", {}))
                state = await func(state, toolset, llm)
                after = json.dumps(state.get("world_state", {}))
                if before != after and 'world_state' in state:
                    log_result(f"Updated world_state: {after}")
                if agent_name == "planner" and "plans" in state:
                    top_plan = state["plans"][0]
                    log_result(f"Best Plan: {top_plan['name']} (Conf={top_plan['confidence']})")
                if agent_name == "executor" and "execution_results" in state:
                    log_result(f"Executed {len(state['execution_results'])} actions.")
                if agent_name == "audit" and "last_ledger_hash" in state:
                    log_result(f"Ledger hash: {state['last_ledger_hash'][:12]}...")
            except Exception as e:
                print(f"{Colors.ERROR}[ERROR in {agent_name}]: {e}{Colors.RESET}")
        print(f"{Colors.RESULT}=== TICK {tick+1} END ==={Colors.RESET}\n")
        await asyncio.sleep(0.3)

    print(f"\n✅ Run complete — Total ledger entries: {len(state.get('audit_log', []))}")
    return state

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_graph(iterations=5))
