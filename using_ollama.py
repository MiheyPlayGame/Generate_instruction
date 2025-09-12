import requests

def ask_ollama(prompt, model="llama2", temperature=0.7):
    """Запрос к локальной модели Ollama"""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "temperature": temperature,
                "options": {
                    "num_predict": 1000
                }
            },
            timeout=120
        )

        return response.json()["response"]

    except Exception as e:
        return f"Ошибка: {e}"


def count_numbered_lines(text):
    """Подсчет пронумерованных пунктов в тексте"""
    lines = text.split('\n')
    numbered_count = 0
    
    for line in lines:
        line = line.strip()
        # Ищем номера вида: "1.", "1)"
        if any(line.startswith(f"{i}.") or line.startswith(f"{i})") 
               for i in range(1, 21)):
            numbered_count += 1
    
    return numbered_count


def main():
    print(" Введите ваш вопрос: ")
    question = input().strip()
    while not question:
        print(" Запрос не может быть пустым! Введите запрос заново: ")
        question = input().strip()

    # Форматируем запрос для лучшего ответа
    formated_quest = f"""
    {question}
    
    Пожалуйста, ответь подробно, структурированно и по пунктам.
    Используй нумерованный список для основных пунктов.
    Пункты нумеруй следующим образом: "1." или "1)".
    Будь максимально информативным и дай ответ на РУССКОМ языке!
    """
    
    print(" Генерирую ответ...")
    answer_ru = ask_ollama(formated_quest)

    # Подсчет пунктов
    lines_count = count_numbered_lines(answer_ru)

    # Проверка метрики шага
    while lines_count <= 3:
        print(" Инструкция получилась слишком короткой. Генерирую ответ заново...")
        answer_ru = ask_ollama(formated_quest)
        lines_count = count_numbered_lines(answer_ru)

    
    print("="*50)
    print(" ОТВЕТ:")
    print(answer_ru)
    print("="*50)
    print(f" Найдено пронумерованных пунктов: {lines_count}")
    print("="*50)

if __name__ == '__main__':
    main()