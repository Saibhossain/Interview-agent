from nodes.manager import manager_node


def test_manager_node_with_plan():
    print("Running test_manager_node_with_plan...")

    # 1. Setup the initial state
    state = {"interview_plan": ["Python", "System Design"]}

    # 2. Execute the node
    result = manager_node(state)

    # 3. Assertions with clear feedback
    try:
        assert result["current_topic"] == "Python", f"Expected 'Python', got {result.get('current_topic')}"
        assert result["interview_plan"] == [
            "System Design"], f"Expected ['System Design'], got {result.get('interview_plan')}"
        assert result["follow_up_count"] == 0, f"Expected 0, got {result.get('follow_up_count')}"

        print("✅ PASSED: Manager correctly assigned the first topic and updated the plan.")
    except AssertionError as e:
        print(f"❌ FAILED: {e}")


def test_manager_node_empty_plan():
    print("Running test_manager_node_empty_plan...")

    # 1. Setup an empty state (end of interview)
    state = {"interview_plan": []}

    # 2. Execute the node
    result = manager_node(state)

    # 3. Assertions
    try:
        assert result["current_topic"] is None, f"Expected None, got {result.get('current_topic')}"
        print("✅ PASSED: Manager correctly identified that the interview is over.")
    except AssertionError as e:
        print(f"❌ FAILED: {e}")


# ==========================================
# MAIN EXECUTION
# ==========================================
if __name__ == "__main__":
    print("\n" + "=" * 40)
    print("🧪 Starting Node Tests...")
    print("=" * 40 + "\n")

    test_manager_node_with_plan()
    print("-" * 40)
    test_manager_node_empty_plan()

    print("\n" + "=" * 40)
    print("🏁 Testing Complete.")
    print("=" * 40 + "\n")