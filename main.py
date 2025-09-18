import requests, torch
from transformers import pipeline


def generate_instruction(prompt):
    """
    Генерирует пошаговую инструкцию используя модель transformers.
    
    Parameters:
    prompt : str - Вопрос пользователя, для которого нужно сгенерировать инструкцию
        
    Returns:
    str - Сгенерированная пошаговая инструкция на русском языке
    """
    
    # Используем русскоязычную модель
    generator = pipeline(
        "text-generation",
        model="sberbank-ai/rugpt3large_based_on_gpt2",
        dtype=torch.float32
    )
    

    system_message = f"Вопрос: {prompt}\n\nПодробная инструкция:\n1."
    
    results = generator(
        system_message,  # Используем новый, правильный промт
        max_length=400, 
        temperature=1.0,
        do_sample=True,
        num_return_sequences=1,
        truncation=True
    )
    
    generated_text = results[0]['generated_text']
    # Извлекаем только сгенерированную часть, без нашего промта
    instruction = generated_text.replace(system_message, "").strip()
    
    return instruction


def ask_ollama(prompt, model="llama2", temperature=0.7):
    """
    Отправляет запрос к локальной модели Ollama через API.
    
    Parameters:
    prompt : str - Текст запроса для модели
    model : str, optional - Название модели Ollama (по умолчанию "llama2")
    temperature : float, optional - Параметр температуры для генерации (по умолчанию 0.7)
        
    Returns:
    str - Ответ от модели Ollama или сообщение об ошибке
    """

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
    """
    Подсчитывает количество пронумерованных пунктов в тексте.
    
    Parameters:
    text(str) Текст для анализа
      
    Returns:
    int - Количество найденных пронумерованных пунктов (вида "1.", "1)", "2.", и т.д.)
    """

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
    """
    Основная функция программы для генерации инструкций.
    
    Запрашивает у пользователя технологию генерации и вопрос,
    генерирует инструкцию и выводит результат с метриками качества.
    """

    technology = input("Выберите технологию генерации инструкции: Ollama/transformers - ")
    while technology != "Ollama" and technology != "transformers":
        technology = input("Некорректный выбор. Ollama/transformers - ")
    
    print(f"Выбрана технология {technology}")

    print(" Введите ваш вопрос: ")
    question = input().strip()
    while not question:
        print(" Запрос не может быть пустым! Введите запрос заново: ")
        question = input().strip()

    print("Генерирую ответ...")

    if technology == "Ollama":
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

    elif technology == "transformers":
        # Передаем в функцию ЛИШЬ сам вопрос, без лишних инструкций
        answer_ru = generate_instruction(question)

        # Подсчет пунктов
        lines_count = count_numbered_lines(answer_ru)
        # Проверка метрики шага
        while lines_count < 3:
            print("Инструкция получилась слишком короткой. Генерирую ответ заново...")
            answer_ru = generate_instruction(question)
            lines_count = count_numbered_lines(answer_ru)


    print("="*50)
    print("ОТВЕТ:\n")
    print(answer_ru)
    print("="*50)
    print(f"Найдено пронумерованных пунктов: {lines_count+1}")
    print("="*50)


if __name__ == '__main__':
    main()