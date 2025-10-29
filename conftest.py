import subprocess
import time
import socket
import pytest
import os
from pathlib import Path

LOCALSTACK_PORT = 4566
LOCALSTACK_HOST = "localhost"


def wait_for_port(host: str, port: int, timeout: int = 30):
    """Waiting for LocalStack to be ready on the specified port."""
    start_time = time.time()
    while True:
        try:
            with socket.create_connection((host, port), timeout=2):
                print(f"✅ LocalStack is ready on {host}:{port}")
                return True
        except OSError:
            if time.time() - start_time >= timeout:
                raise TimeoutError(
                    f"⏰ Timeout: LocalStack ins't ready on port {port} in {timeout}s"
                )
            print("⏳ Waiting for LocalStack to be ready...")
            time.sleep(2)


@pytest.fixture(scope="session", autouse=True)
def setup_localstack_environment():
    if(os.getenv("GITHUB_ACTIONS") is True):
        return
    print("\n🚀 Starting LocalStack with docker compose")
    subprocess.run(["docker", "compose", "up", "-d"], check=True)

    wait_for_port(LOCALSTACK_HOST, LOCALSTACK_PORT)

    print("⚙️ Creating DynamoDB table...")
    current_dir = Path(__file__).parent.resolve()
    setup_script = current_dir / "infra" / "setup_localstack.py"
    subprocess.run(["python3", str(setup_script)], check=True)

    print("✅ LocalStack is ready!\n")
    yield

    # Após os testes, encerra o LocalStack
    print("\n🧹 Teardown LocalStack...")
    subprocess.run(["docker", "compose", "down"], check=True)
