import subprocess
import time
import socket
import pytest
from pathlib import Path

LOCALSTACK_PORT = 4566
LOCALSTACK_HOST = "localhost"


def wait_for_port(host: str, port: int, timeout: int = 30):
    """Aguarda até que o LocalStack esteja pronto para conexões."""
    start_time = time.time()
    while True:
        try:
            with socket.create_connection((host, port), timeout=2):
                print(f"✅ LocalStack está respondendo em {host}:{port}")
                return True
        except OSError:
            if time.time() - start_time >= timeout:
                raise TimeoutError(
                    f"⏰ Timeout: LocalStack não respondeu na porta {port} em {timeout}s"
                )
            print("⏳ Aguardando LocalStack iniciar...")
            time.sleep(2)


@pytest.fixture(scope="session", autouse=True)
def setup_localstack_environment():
    """Sobe o LocalStack e prepara o ambiente de testes."""
    # print("\n🚀 Subindo LocalStack via docker compose...")
    subprocess.run(["docker", "compose", "up", "-d"], check=True)

    # Aguarda o LocalStack estar pronto
    wait_for_port(LOCALSTACK_HOST, LOCALSTACK_PORT)

    # Roda o setup de tabelas e seed
    print("⚙️ Configurando tabelas e seed no LocalStack...")
    current_dir = Path(__file__).parent.resolve()
    setup_script = current_dir / "infra" / "setup_localstack.py"
    # infra/setup_localstack.py
    subprocess.run(["python3", str(setup_script)], check=True)

    print("✅ Ambiente LocalStack configurado com sucesso!\n")
    yield

    # Após os testes, encerra o LocalStack
    print("\n🧹 Finalizando LocalStack...")
    subprocess.run(["docker", "compose", "down"], check=True)
