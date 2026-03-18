from graph.builder import build_graph
import os



def test_graph_builds():
    print("Building the LangGraph...")
    graph = build_graph()
    assert graph is not None, "Graph failed to compile."
    print("Generating graph visualization...")
    try:
        png_bytes = graph.get_graph().draw_mermaid_png()
        output_path = "interview_test_graph_architecture.png"
        with open(output_path, "wb") as f:
            f.write(png_bytes)

        print(f"Success! Graph image saved to: {output_path}")

    except Exception as e:
        print(f"Graph built, but failed to save image. Error: {e}")


if __name__ == "__main__":
    test_graph_builds()