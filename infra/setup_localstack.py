import os
from create_table import create_table

if __name__ == "__main__":
    create_table()
    print(os.getenv("CI"))
    print(os.getenv("GITHUB_ACTIONS"))