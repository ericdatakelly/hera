from hera.shared.global_config import GlobalConfig
from hera.workflows.container import Container
from hera.workflows.workflow import Workflow


def test_container_pre_build_hooks():
    def set_container_default_image(container: Container) -> None:
        container.image = "test_image"

    GlobalConfig.container_pre_build_hooks = (set_container_default_image,)

    with Workflow(name="t") as w:
        c = Container()

    assert c.image == "python:3.7"
    w.build()
    assert c.image == "test_image"
    GlobalConfig.reset()

    def set_container_label(container: Container) -> None:
        container.labels = {"test": "test"}

    GlobalConfig.container_pre_build_hooks = (
        set_container_default_image,
        set_container_label,
    )

    with Workflow(name="t") as w:
        c = Container()

    assert c.image == "python:3.7"
    assert c.labels is None
    w.build()
    assert c.image == "test_image"
    assert c.labels["test"] == "test"
    GlobalConfig.reset()


def test_workflow_pre_build_hooks():
    def set_workflow_default_node_selector(workflow: Workflow) -> None:
        workflow.node_selector = {
            "domain": "test",
            "team": "ABC",
        }

    GlobalConfig.workflow_pre_build_hooks = (set_workflow_default_node_selector,)

    with Workflow(name="t") as w:
        pass

    assert w.node_selector is None
    w.build()
    assert w.node_selector["domain"] == "test"
    assert w.node_selector["team"] == "ABC"
    GlobalConfig.reset()

    def set_workflow_default_labels(workflow: Workflow) -> None:
        workflow.labels = {
            "label": "test",
        }

    GlobalConfig.workflow_pre_build_hooks = (set_workflow_default_node_selector, set_workflow_default_labels)

    with Workflow(name="t") as w:
        pass

    assert w.node_selector is None
    assert w.labels is None
    w.build()
    assert w.node_selector["domain"] == "test"
    assert w.node_selector["team"] == "ABC"
    assert w.labels["label"] == "test"
    GlobalConfig.reset()