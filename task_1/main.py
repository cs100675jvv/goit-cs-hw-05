import argparse
import asyncio
import logging
from aiopath import AsyncPath
from aioshutil import copyfile


# Асинхронна функція для рекурсивного читання всіх файлів у вихідній папці
async def read_folder(source: AsyncPath, output: AsyncPath) -> None:
    try:
        # Перевірка, чи є вихідний шлях директорією
        if not await source.is_dir():
            raise NotADirectoryError(f"{source} не є директорією")

        # Рекурсивно ітеруємо всі файли та папки
        async for item in source.rglob('*'):
            if await item.is_file():
                await copy_file(item, output)
    except Exception as e:
        logging.error(f"Помилка під час читання папки {source}: {e}")


# Асинхронна функція для копіювання файлу на основі його розширення
async def copy_file(file: AsyncPath, output: AsyncPath) -> None:
    try:
        # Отримуємо розширення файлу
        extension_name = file.suffix[1:] if file.suffix else 'no_extension'
        extension_folder = output / extension_name

        # Створюємо папку на основі розширення, якщо її ще немає
        await extension_folder.mkdir(exist_ok=True, parents=True)

        # Копіюємо файл у відповідну папку
        await copyfile(file, extension_folder / file.name)
        logging.info(f"Файл {file} скопійовано до {extension_folder / file.name}")
    except Exception as e:
        logging.error(f"Помилка під час копіювання файлу {file}: {e}")


if __name__ == "__main__":
    # Налаштування логування
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    # Створюємо об'єкт ArgumentParser для обробки аргументів командного рядка
    parser = argparse.ArgumentParser(description="Асинхронне сортування файлів за розширенням.")
    parser.add_argument('source', type=str, help="Шлях до вихідної папки.")
    parser.add_argument('output', type=str, help="Шлях до папки для відсортованих файлів.")

    args = parser.parse_args()

    # Ініціалізуємо шляхи до вихідної та цільової папок
    source = AsyncPath(args.source)
    output = AsyncPath(args.output)

    # Запускаємо асинхронне сортування файлів
    asyncio.run(read_folder(source, output))