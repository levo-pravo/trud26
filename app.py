from aiohttp import web
import random

# Список фактов о котах (можно расширить)
CATS_FACTS = [
    "Кошки спят 12–16 часов в сутки.",
    "У кошек 230 костей в теле.",
    "Кошки могут прыгать в 6 раз выше своего роста.",
    "Кошки не чувствуют вкус сладкого.",
    "Сердце кошки бьётся 110–140 раз в минуту.",
    "Кошки ходят на кончиках пальцев.",
    "Домашние кошки генетически близки к тиграм.",
    "Кошки издают более 100 разных звуков.",
    "Котята рождаются слепыми и глухими.",
    "Кошки имеют отличный слух."
]

async def get_cats(request):
    try:
        n = int(request.query.get('n', 1))
        n = max(1, min(n, 10))  # Ограничение 1-10
        facts = random.sample(CATS_FACTS, n)
        return web.json_response({'facts': facts})
    except ValueError:
        return web.json_response({'error': 'n must be integer'}, status=400)

async def get_index(request):
    return web.json_response({'a': 'b'})

app = web.Application()
app.router.add_get('/', get_index)
app.router.add_get('/facts', get_cats)

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=8080)
