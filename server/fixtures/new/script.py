import os
import json

os.chdir('fixtures/new')

q = open('questions.json')

data_q = json.load(q)

new_questions = [] 
new_options = []

# float questions
q_float = open('float_questions.json')
data_q_float = json.load(q_float)

for q_f in data_q_float:
    new_question = {
        'model': 'questions.question',
        'fields': {

        }
    }

    # забираем данные из родительского вопроса
    for q in data_q:
        if q['pk'] == q_f['pk']:
            q_fields = q['fields']
            new_question['pk'] = q['pk']
            new_question['fields']['question_text'] = q['fields']['question_text']
            new_question['fields']['explanation_text'] = q['fields']['explanation_text']
            new_question['fields']['nodes'] = q['fields']['nodes']
            new_question['fields']['trainer_tags'] = q['fields']['themes']
    
    fields = q_f['fields']

    new_question['fields']['max_score'] = 1
    new_question['fields']['checking_policy'] = 1
    new_question['fields']['type'] = 1
    new_question['fields']['image'] = fields['image']
    new_question['fields']['explanation_image'] = fields['explanation_image']

    new_questions.append(new_question)

    new_option = {
        'model': 'questions.questionoption',
        'pk': len(new_options)+1,
        'fields': {
            'question': q_f['pk'],
            'is_true': True,
            'option_text': fields['right_answer']
        }
    }

    new_options.append(new_option)


# string questions
q_string = open('string_questions.json')
data_q_string = json.load(q_string)

for q_f in data_q_string:
    new_question = {
        'model': 'questions.question',
        'fields': {

        }
    }

    # забираем данные из родительского вопроса
    for q in data_q:
        if q['pk'] == q_f['pk']:
            q_fields = q['fields']
            new_question['pk'] = q['pk']
            new_question['fields']['question_text'] = q['fields']['question_text']
            new_question['fields']['explanation_text'] = q['fields']['explanation_text']
            new_question['fields']['nodes'] = q['fields']['nodes']
            new_question['fields']['trainer_tags'] = q['fields']['themes']
    
    fields = q_f['fields']

    new_question['fields']['max_score'] = 1
    new_question['fields']['checking_policy'] = 1
    new_question['fields']['type'] = 1
    new_question['fields']['image'] = fields['image']
    new_question['fields']['explanation_image'] = fields['explanation_image']

    new_questions.append(new_question)

    new_option = {
        'model': 'questions.questionoption',
        'pk': len(new_options)+1,
        'fields': {
            'question': q_f['pk'],
            'is_true': True,
            'option_text': fields['right_answer']
        }
    }

    new_options.append(new_option)


# # exam questions
q_exam = open('exam_questions.json')
data_q_exam = json.load(q_exam)

pk = 6100

for q_f in data_q_exam:
    new_question = {
        'model': 'questions.question',
        'fields': {

        }
    }

    # забираем данные из родительского вопроса
    for q in data_q:
        if q['pk'] == q_f['pk']:
            q_fields = q['fields']
            new_question['pk'] = q['pk']
            new_question['fields']['question_text'] = q['fields']['question_text']
            new_question['fields']['explanation_text'] = q['fields']['explanation_text']
            new_question['fields']['nodes'] = q['fields']['nodes']
            new_question['fields']['trainer_tags'] = q['fields']['themes']
    
    fields = q_f['fields']

    new_question['fields']['max_score'] = fields['maximum']
    if fields['order_importance']:
        new_question['fields']['type'] = 2
    else:
        new_question['fields']['type'] = 3
    new_question['fields']['checking_policy'] = 1
    new_question['fields']['image'] = fields['image']
    new_question['fields']['explanation_image'] = fields['explanation_image']

    new_questions.append(new_question)

    new_option = {
        'model': 'questions.questionoption',
        'pk': len(new_options)+1,
        'fields': {
            'question': q_f['pk'],
            'is_true': True,
            'option_text': fields['right_answer']
        }
    }

    new_options.append(new_option)


# choice questions
q_exam = open('choice_questions.json')
data_q_exam = json.load(q_exam)

for q_f in data_q_exam:
    new_question = {
        'model': 'questions.question',
        'fields': {

        }
    }

    # забираем данные из родительского вопроса
    for q in data_q:
        if q['pk'] == q_f['pk']:
            q_fields = q['fields']
            new_question['pk'] = q['pk']
            new_question['fields']['question_text'] = q['fields']['question_text']
            new_question['fields']['explanation_text'] = q['fields']['explanation_text']
            new_question['fields']['nodes'] = q['fields']['nodes']
            new_question['fields']['trainer_tags'] = q['fields']['themes']
    
    fields = q_f['fields']


    new_question['fields']['type'] = 5
    new_question['fields']['checking_policy'] = 1
    new_question['fields']['image'] = fields['image']
    new_question['fields']['explanation_image'] = fields['explanation_image']

    new_questions.append(new_question)


k = len(new_options)
new_options = []

q_opt = open('choice_options.json')
data_q_opt = json.load(q_opt)

for q_op in data_q_opt:
    new_option = {
        'model': 'questions.questionoption',
        'pk': k+1,
        'fields': {
            'question': q_op['fields']['question'],
            'is_true': q_op['fields']['is_true'],
            'option_text': q_op['fields']['option_text'],
            'option_image': q_op['fields']['option_image'],
            'help_text': q_op['fields']['help_text'],
        }
    }

    k+=1

    new_options.append(new_option)


print(new_questions[0])
print(new_options[0])


json_string = json.dumps(new_questions)

with open('questions_new.json', 'w') as outfile:
    outfile.write(json_string)

json_string = json.dumps(new_options)

with open('options_new.json', 'w') as outfile:
    outfile.write(json_string)
