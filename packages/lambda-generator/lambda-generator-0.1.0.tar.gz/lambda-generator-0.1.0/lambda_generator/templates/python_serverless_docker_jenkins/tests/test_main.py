from python_serverless_docker_jenkins.main import example


def test_example_function():
    assert 3 == example(1, 2)
