# agents/perception.py
import asyncio, time
from pydantic import BaseModel

# Simple Pydantic model for strong typing (optional)
class Observation(BaseModel):
    ts: str
    sensor_id: str
    sensor_type: str
    location: str
    value: float
    source: str = "simulator"

async def run(state, tools, llm, config=None):
    """
    Reads next simulated event (CSV stream) and appends a structured observation to state['perception_events'].
    In a streaming run, this is called repeatedly.
    """
    if 'perception_cursor' not in state:
        state['perception_cursor'] = getattr(state, 'perception_cursor', 0)

    # read one item from CSV stream generator stored in tools
    try:
        gen = tools['csv_gen']
        raw = next(gen)
    except StopIteration:
        return state
    except Exception:
        # fallback: no generator, or direct injection
        raw = state.get('manual_inject')
        if raw is None:
            return state

    obs = Observation(
        ts=raw.get('timestamp', str(time.time())),
        sensor_id=raw.get('sensor_id'),
        sensor_type=raw.get('sensor_type'),
        location=raw.get('location'),
        value=float(raw.get('value', 0.0)),
        source=raw.get('source','sim')
    ).dict()

    state.setdefault('perception_events', []).append(obs)
    # small provenance
    state.setdefault('provenance', []).append({'agent':'perception','obs_id':len(state['perception_events'])-1})
    return state
