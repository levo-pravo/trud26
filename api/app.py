import os
from aiohttp import web
import random

CATS_FACTS = [
    "Кошки спят до 16 часов в день.",
    "У кошек гибкий позвоночник, позволяющий им разворачиваться в прыжке.",
    "Кошки могут издавать более 100 различных звуков.",
    "Сердце кошки бьётся быстрее человеческого.",
    "Кошки ходят на кончиках пальцев.",
]


async def get_facts(request: web.Request) -> web.Response:
    try:
        n = int(request.query.get("n", 1))
        n = max(1, min(n, len(CATS_FACTS)))
    except ValueError:
        return web.json_response({"error": "n must be integer"}, status=400)

    facts = random.sample(CATS_FACTS, n)
    return web.json_response({"facts": facts})


def create_app() -> web.Application:
    app = web.Application()
    app.router.add_get("/facts", get_facts)
    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("PORT", 8080))
    web.run_app(app, host="0.0.0.0", port=port)
