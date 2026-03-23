"""Architecture diagram generator. Run with: make diagram"""

from diagrams import Cluster, Diagram, Edge
from diagrams.programming.language import Python
from diagrams.generic.storage import Storage
from diagrams.generic.compute import Rack


def generate():
    with Diagram(
        "Project Architecture",
        filename="docs/architecture/architecture",
        show=False,
        direction="LR",
    ):
        with Cluster("Source (src/)"):
            core = Python("core/")
            models = Python("models/")
            utils = Python("utils/")

        with Cluster("Data"):
            raw = Storage("raw/")
            processed = Storage("processed/")

        with Cluster("Outputs"):
            artifacts = Rack("artifacts/")

        raw >> Edge(label="load") >> core
        core >> Edge(label="transform") >> models
        models >> Edge(label="persist") >> processed
        models >> Edge(label="export") >> artifacts
        utils >> Edge(style="dashed") >> core
        utils >> Edge(style="dashed") >> models


if __name__ == "__main__":
    generate()
    print("✅  Diagram saved to docs/architecture/architecture.png")