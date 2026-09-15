from dotenv import load_dotenv
load_dotenv()
from src.graph import build_graph

from src.graph import build_graph

if __name__ == "__main__":
    app = build_graph()
    result = app.invoke({
        "raw_ticket": "Hi, I was charged twice this month.   My email is jane@example.com"
        # "raw_ticket": "Hi, I want to report bug on windows software,And a later the bug cost me four hundred dollars.   My email is rohan@test.com"
        # "raw_ticket": "nothing works and I don't know why, fix it"

    })
    print(result)