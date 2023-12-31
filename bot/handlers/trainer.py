from aiogram import Router, types
from aiogram import F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db import database
from texts import Texts
from filters.user_type import UserTypeFilter
from handlers.question import QuestionCallbackFactory
from callback_factories import TrainerCallbackFactory, QuestionCallbackFactory


# создаём роутер для дальнешей привязки к нему обработчиков
router = Router()
router.message.filter(
    UserTypeFilter(user_types=['reg', 'admin'])
)


# формируем клавиатуру для выбора экзамена
def select_exam_keyboard(edit=True) -> InlineKeyboardMarkup:
    array_buttons: list[list[InlineKeyboardButton]] = []

    exam_tree = database.exam_tree

    for exam in exam_tree:
        if exam["is_active"]:
            array_buttons.append([
                InlineKeyboardButton(
                    text=exam['title'],
                    callback_data=TrainerCallbackFactory(
                        exam_id=exam["pk"],
                        se_id=0,
                        sen_id=0,
                        tag_id=0,
                        edit=edit
                    ).pack()
                )
            ])
    
    array_buttons.append([
        InlineKeyboardButton(
            text=Texts.BACK_TEXT,
            callback_data="menu"
        )
    ])

    markup: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=array_buttons)
    return markup


# формируем клавиатуру для выбора предмета под экзамен
def select_subject_keyboard(exam_id, edit=True) -> InlineKeyboardMarkup:
    array_buttons: list[list[InlineKeyboardButton]] = []

    exam = database.get_exam(exam_id=exam_id)

    array_buttons.append([
        InlineKeyboardButton(
            text=Texts.BACK_TEXT,
            callback_data=TrainerCallbackFactory(
                exam_id=0,
                se_id=0,
                sen_id=0,
                tag_id=0,
                edit=edit
            ).pack()
        )
    ])

    subject_exams = exam["subject_exams"]

    for se in subject_exams:
        if se["is_active"]:
            array_buttons.append([
                InlineKeyboardButton(
                    text=se['subject']['title'],
                    callback_data=TrainerCallbackFactory(
                        exam_id=exam_id,
                        se_id=se["pk"],
                        sen_id=0,
                        tag_id=0,
                        edit=edit
                    ).pack()
                )
            ])

    markup: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=array_buttons)
    return markup


# формируем клавиатуру для выбора номера в предмета под экзамен
def select_num_keyboard(exam_id, se_id, edit=True) -> InlineKeyboardMarkup:
    se = database.get_subject_exam(exam_id=exam_id, se_id=se_id)

    subject_exam_numbers = se["subject_exam_numbers"]
    subject_exam_numbers_active = [sen for sen in subject_exam_numbers if sen["is_active"]]
    subject_exam_numbers_active.sort(key=lambda sen: sen["num"], reverse=False)

    builder = InlineKeyboardBuilder()

    builder.button(
        text=Texts.BACK_TEXT,
        callback_data=TrainerCallbackFactory(
            exam_id=exam_id,
            se_id=0,
            sen_id=0,
            tag_id=0,
            edit=edit
        ).pack()
    )

    for sen in subject_exam_numbers_active:
        title = f"{sen['num']}. {sen['title']}"
        builder.button(
            text=title,
            callback_data=TrainerCallbackFactory(
                exam_id=exam_id,
                se_id=se_id,
                sen_id=sen["pk"],
                tag_id=0,
                edit=edit
            ).pack()
        )
    
    builder.adjust(1, 2)

    return builder.as_markup()


# формируем клавиатуру для выбора темы в номере в предмета под экзамен
def select_tag_keyboard(exam_id, se_id, sen_id, edit=True) -> InlineKeyboardMarkup:
    sen = database.get_subject_exam_number(exam_id=exam_id, se_id=se_id, sen_id=sen_id)
    exam_tags = sen["exam_tags"]

    exam_tags_active = [tag for tag in exam_tags if tag["is_active"]]

    builder = InlineKeyboardBuilder()

    builder.button(
        text=Texts.BACK_TEXT,
        callback_data=TrainerCallbackFactory(
            exam_id=exam_id,
            se_id=0,
            sen_id=0,
            tag_id=0,
            edit=edit
        ).pack()
    )

    for exam_tag in exam_tags_active:
        builder.button(
            text=exam_tag["title"],
            callback_data=TrainerCallbackFactory(
                exam_id=exam_id,
                se_id=se_id,
                sen_id=sen_id,
                tag_id=exam_tag["pk"],
                edit=edit
            ).pack()
        )
    
    builder.adjust(1, 2)

    return builder.as_markup()


def tag_keyboard(exam_id, se_id, sen_id, tag_id, edit=True):
    kb = [
        [types.InlineKeyboardButton(text=Texts.BACK_TEXT, callback_data=TrainerCallbackFactory(
            exam_id=exam_id,
            se_id=se_id,
            sen_id=sen_id,
            tag_id=0,
            edit=edit
        ).pack())],
        [types.InlineKeyboardButton(text="Решить случайную задачу", callback_data=QuestionCallbackFactory(
            exam_tag_id=tag_id,
            question_id=0
        ).pack())]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


# прилет коллбека в меню тренажера
@router.callback_query(TrainerCallbackFactory.filter())
async def trainer_menu_handler(callback: types.CallbackQuery, callback_data: TrainerCallbackFactory, state: FSMContext):
    # callback_data содержит указатели на экзамен, предмет, номер и тему

    # state хранит состояние, показывается меню на момент нажатия, или нет
    # это поможет принять решение, перерисовывать сообщение или писать с нуля

    # а еще state содержит сохраненный выбор пользователя, на случай возврата

    # Первый шаг - апдейт сохраненного выбора на основе данных коллбека
    callback_exam_id, callback_se_id, callback_sen_id, callback_tag_id, callback_edit = callback_data.exam_id, callback_data.se_id, callback_data.sen_id, callback_data.tag_id, callback_data.edit
    await state.update_data(chosen_exam_id=callback_exam_id, chosen_se_id=callback_se_id, chosen_sen_id=callback_sen_id, chosen_exam_tag_id=callback_tag_id)
    # и сбросить выбранный вопрос
    await state.update_data(chosen_question_id=0)
    
    # Второй шаг - формирование текста и клавиатуры ответа
    msg_text = ''
    msg_keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[]])

    # если экзамен не выбран - даем его выбрать
    if callback_exam_id == 0:
        msg_text="Выбирай экзамен"
        msg_keyboard=select_exam_keyboard(edit=True)
    # если экзамен выбран - думаем дальше
    else:
        # если предмет не выбран - даем выбирать его
        if callback_se_id == 0:
            msg_text=f"Выбирай предмет:"
            msg_keyboard=select_subject_keyboard(exam_id=callback_exam_id, edit=True)
        # если предмет выбран - думаем дальше
        else:
            # загружаем данные по предмету для отображения
            se = database.get_subject_exam(exam_id=callback_exam_id, se_id=callback_se_id)
            # если номер не выбран - даем его выбрать
            if callback_sen_id == 0:
                msg_text=f"{se['exam']['title']} по предмету <b>{se['subject']['title']}</b> (<i>Доступно задач: {se['questions_exist']}</i>)"
                msg_keyboard=select_num_keyboard(exam_id=callback_exam_id, se_id=callback_se_id, edit=True)
            # если номер выбран - думаем дальше
            else:
                # загружаем данные номера для отображения
                sen = database.get_subject_exam_number(exam_id=callback_exam_id, se_id=callback_se_id, sen_id=callback_sen_id)
                # если тема не выбрана - даем ее выбрать
                if callback_tag_id == 0:
                    msg_text=f"Номер {sen['num']} из {se['exam']['title']} по предмету {se['subject']['title']}\nТема: <b>{sen['title']}</b> (<i>Доступно задач: {sen['questions_exist']}</i>)"
                    msg_keyboard=select_tag_keyboard(exam_id=callback_exam_id, se_id=callback_se_id, sen_id=callback_sen_id, edit=True)
                # если тема выбрана - это конец меню
                else:
                    # загружаем данные тега для отображения
                    tag = database.get_subject_exam_number_tag(exam_id=callback_exam_id, se_id=callback_se_id, sen_id=callback_sen_id, tag_id=callback_tag_id)
                    msg_text=f"Номер {sen['num']} из {se['exam']['title']} по предмету {se['subject']['title']}\nТема: <b>{sen['title']}</b>\nПодтема:<b>{tag['title']}</b>\n<i>Доступно задач: {tag['questions_exist']}</i>"
                    msg_keyboard=tag_keyboard(exam_id=callback_exam_id, se_id=callback_se_id, sen_id=callback_sen_id, tag_id=callback_tag_id, edit=True)

    # Последний шаг - понимание как отвечать
    # если меню сейчас показывается, то надо редактировать
    if callback_edit == True:
        await callback.message.edit_text(text=msg_text, reply_markup=msg_keyboard)
    else:
        await callback.message.answer(text=msg_text, reply_markup=msg_keyboard)
