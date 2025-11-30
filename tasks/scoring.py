from datetime import date
from dateutil import parser
from collections import defaultdict

DEFAULT_WEIGHTS = {
    "urgency": 6.0,
    "importance": 5.0,
    "effort": -1.5,
    "quick_win_bonus": 8,
    "dependency_boost": 7,
}


def _parse_date(d):
    if d is None:
        return None
    if isinstance(d, date):
        return d
    try:
        return parser.parse(d).date()
    except Exception:
        return None


def detect_cycles(tasks):
    """
    Detects cycles in the dependency graph.
    tasks: list of dicts each having 'id' and 'dependencies' (list)
    Returns: set of task ids that are part of a cycle.
    """
    graph = defaultdict(list)
    ids = set()
    for t in tasks:
        tid = t.get("id")
        ids.add(tid)
        for dep in t.get("dependencies") or []:
            # edge: dep -> tid (dep must be done before tid)
            graph[dep].append(tid)

    WHITE, GREY, BLACK = 0, 1, 2
    color = {tid: WHITE for tid in ids}
    cycles = set()

    def dfs(u, stack):
        color[u] = GREY
        stack.append(u)
        for v in graph.get(u, []):
            if color.get(v, WHITE) == WHITE:
                dfs(v, stack)
            elif color.get(v) == GREY:
                # back-edge found, nodes from v..end of stack are in cycle
                if v in stack:
                    idx = stack.index(v)
                    for node in stack[idx:]:
                        cycles.add(node)
        color[u] = BLACK
        stack.pop()

    for node in list(ids):
        if color[node] == WHITE:
            dfs(node, [])
    return cycles


def calculate_task_score(task, all_tasks_map=None, weights=None):
    """
    Calculate a numerical priority score for a single task.
    - task: dict with keys id,title,due_date,importance,estimated_hours,dependencies
    - all_tasks_map: optional dict id -> task dict, used to count how many tasks this one blocks
    - weights: optional dict to override DEFAULT_WEIGHTS
    Returns: dict { 'score': float, 'explanation': str, 'meta': {...} }
    """
    w = DEFAULT_WEIGHTS.copy()
    if weights:
        w.update(weights)

    today = date.today()
    due = _parse_date(task.get("due_date"))
    importance = int(task.get("importance") or 5)
    estimated_hours = int(task.get("estimated_hours") or 1)

    score = 0.0
    reasons = []

    # 1) Urgency
    if due is None:
        reasons.append("No due date -> low urgency")
    else:
        days_until_due = (due - today).days
        if days_until_due < 0:
            score += 100 * w["urgency"]
            reasons.append(f"Overdue by {-days_until_due} days -> huge urgency boost")
        else:
            if days_until_due <= 3:
                score += 50 * w["urgency"]
                reasons.append(f"Due in {days_until_due} days -> high urgency")
            elif days_until_due <= 7:
                score += 20 * w["urgency"]
                reasons.append(f"Due in {days_until_due} days -> medium urgency")
            else:
                score += max(0, (10 / (days_until_due + 1))) * w["urgency"]
                reasons.append(f"Due in {days_until_due} days -> low urgency")

    # 2) Importance
    score += importance * w["importance"]
    reasons.append(
        f"Importance {importance} contributes {importance * w['importance']}"
    )

    # 3) Effort / Quick wins
    if estimated_hours <= 0:
        estimated_hours = 1
    if estimated_hours < 2:
        score += w["quick_win_bonus"]
        reasons.append(f"Quick win ({estimated_hours}h) -> +{w['quick_win_bonus']}")
    else:
        # penalize larger tasks slightly (so quick tasks bubble up)
        score += (1.0 / estimated_hours) * w["effort"] * 10
        reasons.append(f"Estimated hours {estimated_hours} affects score")

    # 4) Dependencies: how many tasks does this one block?
    deps = task.get("dependencies") or []
    if all_tasks_map is not None:
        blocking_count = 0
        for other in all_tasks_map.values():
            if task.get("id") in (other.get("dependencies") or []):
                blocking_count += 1
        if blocking_count > 0:
            score += blocking_count * w["dependency_boost"]
            reasons.append(
                f"Blocks {blocking_count} other task(s) -> +{blocking_count * w['dependency_boost']}"
            )

    return {
        "score": round(score, 2),
        "explanation": "; ".join(reasons),
        "meta": {
            "due_date_parsed": due.isoformat() if due else None,
            "importance": importance,
            "estimated_hours": estimated_hours,
            "dependencies": deps,
        },
    }
