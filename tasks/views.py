import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .scoring import calculate_task_score, detect_cycles


@csrf_exempt
def analyze_tasks(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=405)

    try:
        tasks = json.loads(request.body.decode("utf-8"))
    except:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    if not isinstance(tasks, list):
        return JsonResponse({"error": "Expected a JSON array"}, status=400)

    # Assign IDs if missing
    for i, t in enumerate(tasks):
        t.setdefault("id", f"tmp_{i}")

    # Detect cycles
    cycle_ids = detect_cycles(tasks)

    # Build a map for scoring
    all_map = {t["id"]: t for t in tasks}

    results = []
    for t in tasks:
        score_data = calculate_task_score(t, all_tasks_map=all_map)
        results.append(
            {
                "id": t["id"],
                "title": t.get("title", "Untitled"),
                "due_date": t.get("due_date"),
                "importance": t.get("importance"),
                "estimated_hours": t.get("estimated_hours"),
                "dependencies": t.get("dependencies", []),
                "score": score_data["score"],
                "explanation": score_data["explanation"],
                "circular_dependency": t["id"] in cycle_ids,
            }
        )

    # Sort by score (highest first)
    sorted_tasks = sorted(results, key=lambda x: x["score"], reverse=True)
    return JsonResponse(sorted_tasks, safe=False)


@csrf_exempt
def suggest_tasks(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=405)

    resp = analyze_tasks(request)
    if resp.status_code != 200:
        return resp

    tasks = json.loads(resp.content)
    top3 = tasks[:3]

    # Add a simple explanation
    return JsonResponse(
        {
            "top3": [
                {"task": t, "why": f"Rank {i+1}: Score {t['score']} — {t['title']}"}
                for i, t in enumerate(top3)
            ]
        }
    )
