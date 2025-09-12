from transformers import pipeline
import torch

def generate_instruction(prompt):
    """Генерирует пошаговую инструкцию используя transformers"""
    
    # Используем русскоязычную модель
    generator = pipeline(
        "text-generation",
        model="sberbank-ai/rugpt3large_based_on_gpt2",
        dtype=torch.float32
    )
    
    # Ключевое изменение: Формируем КОРРЕКТНЫЙ промт
    # Мы явно начинаем историю и даем команду, которую модель легко поймет.
    system_message = f"Вопрос: {prompt}\n\nПодробная инструкция:\n1."
    
    results = generator(
        system_message,  # Используем новый, правильный промт
        max_length=400,  # Уменьшил длину, т.к. промт теперь короче
        temperature=1.0,
        do_sample=True,
        num_return_sequences=1,
        truncation=True
    )
    
    generated_text = results[0]['generated_text']
    # Извлекаем только сгенерированную часть, без нашего промта
    instruction = generated_text.replace(system_message, "").strip()
    
    return instruction

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
    print("Введите ваш вопрос: ")
    question = input().strip()
    while not question:
        print("Запрос не может быть пустым! Введите запрос заново: ")
        question = input().strip()
    
    print("Генерирую ответ...")
    # Передаем в функцию ЛИШЬ сам вопрос, без лишних инструкций
    answer_ru = generate_instruction(question)

    # Подсчет пунктов
    lines_count = count_numbered_lines(answer_ru)

    # Проверка метрики шага
    while lines_count < 3: # Изменил на строго меньше 3
        print("Инструкция получилась слишком короткой. Генерирую ответ заново...")
        answer_ru = generate_instruction(question)
        lines_count = count_numbered_lines(answer_ru)

    
    print("="*50)
    print("ОТВЕТ:\n")
    # Красиво выводим ответ, начиная с "1."
    print("1." + answer_ru if not answer_ru.startswith('1') else answer_ru)
    print("="*50)
    print(f"Найдено пронумерованных пунктов: {lines_count+1}")
    print("="*50)

if __name__ == "__main__":
    main()