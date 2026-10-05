import sys
import json

from orchestrator.investigation import run as run_local
from orchestrator.intelligence import investigate

def main():
    if len(sys.argv) < 2:
        print(
            'Usage: python main.py '
            '"Tell me about our market" '
            '[data.csv] [--web]'
        )
        return

    question = sys.argv[1]
    data_path = None
    use_web = "--web" in sys.argv

    for argument in sys.argv[2:]:
        if not argument.startswith("--"):
            data_path = argument

    local_result = run_local(
        question,
        data_path
    )

    web_result = None

    if use_web:
        web_result = investigate(question)

    output = {
        "local_investigation": local_result,
        "web_investigation": web_result
    }

    print(
        json.dumps(
            output,
            indent=2,
            default=str
        )
    )

if __name__ == "__main__":
    main()
