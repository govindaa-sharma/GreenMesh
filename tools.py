# tools.py
import csv, time, json, os, hashlib
from collections import deque
import random
import math

# --- CSV reader (simple generator) ---
def csv_stream(path="data/simulated_sensors.csv"):
    if not os.path.exists(path):
        return
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # normalize numeric
            if 'value' in row:
                try:
                    row['value'] = float(row['value'])
                except:
                    pass
            yield row

# --- Simple optimizer (greedy) ---
def simple_optimizer(requirements, resources):
    """
    requirements: list of dicts e.g. [{'zone':'zoneA','need':2}, ...]
    resources: int (number of trucks)
    returns allocation dict {zone: n}
    """
    alloc = {r['zone']: 0 for r in requirements}
    needs = sorted(requirements, key=lambda x: x['need'], reverse=True)
    rem = resources
    for n in needs:
        if rem <= 0: break
        take = min(n['need'], rem)
        alloc[n['zone']] = take
        rem -= take
    return alloc

# --- Digital twin simulator (fast heuristic) ---
def digital_twin_simulate(plan, world_state):
    """
    plan: dict steps
    world_state: dict
    Returns estimated outcome dict (time_saved_min, damage_reduced_pct, cost)
    Heuristics: more steps -> more cost, 'dispatch' reduces time
    """
    base = {'time_saved_min': 0, 'damage_reduced_pct': 0, 'cost': 0}
    p = plan.get('name','').lower()
    if 'dispatch' in p or 'alert' in p:
        base['time_saved_min'] = 20
        base['damage_reduced_pct'] = 40
        base['cost'] = 100
    if 'monitor' in p:
        base['time_saved_min'] = 5
        base['damage_reduced_pct'] = 5
        base['cost'] = 10
    # tweak based on world_state
    if any(zone.get('avg_water',0) and zone['avg_water']>3 for zone in world_state.values()):
        base['damage_reduced_pct'] += 10
        base['time_saved_min'] += 10
    return base

# --- Adversarial detector (stat rule + noise) ---
def detect_adversarial(observations, threshold_factor=3.0):
    """
    observations: list of dicts with keys sensor_id,value
    returns flags: list of (sensor_id, reason)
    """
    flags = []
    # compute last values per sensor
    last = {}
    for o in observations:
        sid = o.get('sensor_id')
        val = o.get('value')
        if sid in last and isinstance(val, (int,float)):
            if abs(val - last[sid]) / max(1e-6, last[sid]) > threshold_factor:
                flags.append({'sensor_id': sid, 'reason': 'sudden_spike'})
        last[sid] = val
    # random small prob of false positive for demo
    if random.random() < 0.02:
        flags.append({'sensor_id': 'sim_random', 'reason':'random_noise'})
    return flags

# --- Simple ledger (append-only file) with basic ECDSA-like signature (mock) ---
LEDGER_PATH = "data/ledger.jsonl"
def append_ledger(entry):
    """
    entry: dict -> will be appended with timestamp+hash
    """
    os.makedirs(os.path.dirname(LEDGER_PATH), exist_ok=True)
    now = time.time()
    payload = {'ts': now, 'entry': entry}
    # compute prev hash
    prev = ""
    if os.path.exists(LEDGER_PATH):
        with open(LEDGER_PATH, "r") as f:
            lines = f.readlines()
            if lines:
                last = json.loads(lines[-1])
                prev = last.get("hash","")
    payload['prev'] = prev
    h = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
    payload['hash'] = h
    with open(LEDGER_PATH, "a") as f:
        f.write(json.dumps(payload)+"\n")
    return payload
