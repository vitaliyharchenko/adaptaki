# Приложение для создания вопросов и задач

## Необходимый функционал:

-   создание задачи разных типов в админке
-   редактирование задач в админке со сменой типа
-   копирование задач
-   выдача задачи в виде картинки
-   проверка ответов

## Какие есть типы заданий

-   на экзамене
    -   ответ строкой
        -   последовательность цифр с важным порядком (сопоставление)
        -   последовательность цифр с неважным порядком (выбор верных)
        -   число
        -   строка
    -   ответ файлом
        -   сочинения и задания второй части
-   не на экзамене
    -   число с заданной точностью
    -   выбор правильных радиокнопками
    -   сопоставление
    -   заполнение пропусков

Они отличаются политикой снятия баллов и критериями оценки

## Модель Question содержит:

-   текст вопроса
-   картинки к заданию
-   текст пояснения
-   картинки к пояснению

-   тип задания

    -   простая проверка (несколько верных вариантов ответа)
    -   набор символов в нужном порядке (один верный вариант ответа)
    -   набор символов в произвольном порядке (один верный вариант ответа)
    -   выбор верных вариантов (влияет на интерфейс) (несколько варинтов ответа)
    -   самостоятельное решение (без вариантов ответа)

-   максимальный балл
-   политика проверки

    -   отнимать 1 балл за каждую ошибку
    -   отнимать все баллы за любую ошибку

-   варианты ответа

Привязано к:

-   nodes графа
-   themes рубрикатора экзамена

## Модель QuestionOption

-   текст варианта
-   каринка варианта
-   текст пояснения
-   правильный?

Привязано к:

-   question
