def plan_structure(state):
    print("🔧 [PLAN_STRUCTURE] Planning folder layout from spec...")
    json_spec = state.get("json_spec")

    plan = {
        "screens": json_spec.get("screens", []),
        "folders": ["Views", "ViewModels", "Models", "Services", "Resources", "Utils"],
        "language": "swift",
        "architecture": "MVVM"
    }

    print("✅ [PLAN_STRUCTURE] Generated structure plan:", plan)
    return {"structure_plan": plan}