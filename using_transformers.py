from transformers import pipeline
import torch

def generate_instruction(prompt):
    """Генерирует пошаговую инструкцию используя transformers"""
    
    # Используем русскоязычную модель
    generator = pipeline(
        "text-generation",
        model="sberbank-ai/rugpt3small_based_on_gpt2",  # Русскоязычная модель
        dtype=torch.float32,
        device=-1  # Используем CPU
    )
    
    # Генерируем текст
    results = generator(
        prompt,
        max_length=1000,
        temperature=0.8,
        do_sample=True,
        num_return_sequences=1,
        truncation=True
    )
    
    # Извлекаем сгенерированный текст
    generated_text = results[0]['generated_text']
    instruction = generated_text.replace(prompt, "").strip()
    
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
    answer_ru = generate_instruction(formated_quest)

    # Подсчет пунктов
    lines_count = count_numbered_lines(answer_ru)

    # Проверка метрики шага
    while lines_count <= 3:
        print(" Инструкция получилась слишком короткой. Генерирую ответ заново...")
        answer_ru = generate_instruction(formated_quest)
        lines_count = count_numbered_lines(answer_ru)

    
    print("="*50)
    print(" ОТВЕТ:")
    print(answer_ru)
    print("="*50)
    print(f" Найдено пронумерованных пунктов: {lines_count}")
    print("="*50)


if __name__ == "__main__":
    main()