import pygame
from classes import ClassManager
from students import StudentManager
from subjects import SubjectManager
from database import subjects
from gui_elements import draw_text, Button, InputBox, Dropdown, Prompt, SelectableList, ScrollableTable

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BG_COLOR = (250, 250, 250)
FONT = pygame.font.SysFont(None, 29)
clock = pygame.time.Clock()

# Initialize the prompt
prompt = Prompt(100, 120, 600, 40, FONT)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("School Management System")

# Initialize pages
current_page, previous_page = 'main', 'main'

# Managers
class_manager = ClassManager()
student_manager = StudentManager()
subject_manager = SubjectManager()

# Button definitions
button_width, button_height = 320, 40
button_color = pygame.Color('dodgerblue')
button_hover_color = pygame.Color('lightskyblue')
button_text_color = pygame.Color('black')

# Input box definitions
input_box_width, input_box_height = 320, 40
input_box_color = pygame.Color('dodgerblue')
input_box_hover_color = pygame.Color('lightskyblue')
input_box_text_color = pygame.Color('black')

# Dropdown definitions
dropdown_width, dropdown_height = 320, 40
dropdown_color = pygame.Color('dodgerblue')
dropdown_hover_color = pygame.Color('lightskyblue')
dropdown_text_color = pygame.Color('black')

button_back = Button(50, 50, 100, 50,'Back', FONT, button_color, button_hover_color, button_text_color)

def submit_class():
    global current_page, previous_page
    available_class_names = class_manager.get_all_class_field(1)
    name = input_box_class_name.text
    capacity = input_box_class_capacity.text
    if name=="" or capacity=="":
        prompt.show("All fields are required!")
    elif name in available_class_names:
        prompt.show("This class already exists!") 
    elif not capacity.isdigit() or int(capacity)<1 or int(capacity)>80:
        prompt.show("Class size must be a positive integer of at most 80!")
    else:
        class_manager.add_class(name, capacity)
        current_page = previous_page
        prompt.show("Class successfully created!", pygame.Color("white"), pygame.Color("green"))

def submit_student():
    global current_page, previous_page
    student_name = input_box_student_name.text
    student_class = dropdown_student_class.current_text
    student_subjects = selectable_list.selected_items
    available_class_names = class_manager.get_all_class_field(1)

    if student_name=="" or student_class=="":
        prompt.show("All fields are required!")
    elif student_class not in available_class_names:
        prompt.show("This class does not exist!") 
    else:
        Class_id, Class_name, Class_capacity = class_manager.get_class_record(student_class)
        Class_numStudents = class_manager.find_num_students(Class_name)

        if Class_numStudents==Class_capacity:
            prompt.show("This class is already full!")
        elif len(student_subjects) < 8 or len(student_subjects) > 12:
            prompt.show("Number of subjects must be between 8 and 12")
        else:
            student_manager.add_student(student_name, Class_id)
            student_id = student_manager.get_student_id(student_name, student_class)
            subject_manager.add_subjects(student_id, student_subjects)
            current_page = previous_page
            prompt.show("Student successfully created!", pygame.Color("white"), pygame.Color("green"))
    
def create_class_page():
    global current_page, previous_page, button_back
    global input_box_class_name, input_box_class_capacity
    previous_page = 'manage_classes'
    
    button_back.rect.x, button_back.rect.y = WIDTH//2-135, 400
    
    button_submit_class = Button(WIDTH//2-235+input_box_width, 400, 100, 50, 'Submit', FONT, button_color, 
                                 button_hover_color, button_text_color, action=submit_class)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif current_page == 'create_class':
            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_button_click(event.pos)
            input_box_class_name.handle_event(event)
            input_box_class_capacity.handle_event(event)
            button_submit_class.handle_event(event)

    prompt.update()
    input_box_class_name.update()
    input_box_class_capacity.update()
    screen.fill(BG_COLOR)

    prompt.draw(screen)
    input_box_class_name.draw(screen)
    input_box_class_capacity.draw(screen)
    button_back.draw(screen)
    button_submit_class.draw(screen)
    draw_text('Create New Class', FONT, (0, 0, 0), screen, (WIDTH - FONT.size('Create New Class')[0]) // 2, 75)

    pygame.display.flip()
    return True

def view_classes_page():
    global current_page, previous_page, button_back
    global data, class_table
    previous_page = 'manage_classes'

    button_back.rect.x, button_back.rect.y = WIDTH//2-button_back.width//2, 500

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif current_page == 'view_classes':
            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_button_click(event.pos)
            class_table.handle_event(event)

    prompt.update()
    screen.fill(BG_COLOR)

    prompt.draw(screen)
    button_back.draw(screen)
    class_table.draw(screen)
    draw_text('View all Classes', FONT, (0, 0, 0), screen, (WIDTH - FONT.size('View all Classes')[0]) // 2, 75)

    pygame.display.flip()
    return True

def register_student_page():
    global current_page, previous_page, button_back
    previous_page = 'manage_students'

    button_back.rect.x, button_back.rect.y = 200, 500
    button_submit_student = Button(WIDTH//2-235+input_box_width, 500, 100, 50, 'Submit', FONT, button_color, 
                                 button_hover_color, button_text_color, action=submit_student)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif current_page == "register_student":
            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_button_click(event.pos)
            input_box_student_name.handle_event(event)
            dropdown_student_class.handle_event(event)
            selectable_list.handle_event(event)
            button_submit_student.handle_event(event)

    input_box_student_name.update()
    dropdown_student_class.update()
    screen.fill(BG_COLOR)
    prompt.update()

    draw_text('Register New Student', FONT, (0, 0, 0), screen, (WIDTH - FONT.size('Register New Student')[0]) // 2, 75)
    prompt.draw(screen)
    input_box_student_name.draw(screen)
    dropdown_student_class.draw(screen)
    button_back.draw(screen)
    selectable_list.draw(screen)
    button_submit_student.draw(screen)
    pygame.display.flip()
    return True

def submit_subject_score_edit():
    global current_page, previous_page
    student_name = edit_student_dropdown_student_name.current_text
    student_class = edit_student_dropdown_student_class.current_text
    student_subject = edit_student_dropdown_student_subject.current_text
    new_score = edit_student_input_box_new_score.text

    available_class_names = class_manager.get_all_class_field(1)
    available_students = student_manager.get_students_by_class(student_class)
    available_student_names = []
    for _,name,_ in available_students:
        available_student_names.append(name)

    student_id = student_manager.get_student_id(student_name,student_class)
    subject_id = 0
    available_subjects = subject_manager.get_student_subjects(student_id)
    available_subject_names = []
    for id,name,_,_ in available_subjects:
        available_subject_names.append(name)
        if name==student_subject:
            subject_id = id
    if student_name=="" or student_class=="" or student_subject=="" or new_score=="":
        prompt.show("All fields are required!")
    elif student_class not in available_class_names:
        prompt.show("This class does not exist!")
    elif student_name not in available_student_names:
        prompt.show("This student does not exist!")
    elif student_subject not in available_subject_names:
        prompt.show("This subject does not exist!")
    elif not new_score.isdigit() or int(new_score)<0 or int(new_score)>100:
        prompt.show("Score must be an integer from 0 to 100!")
    else:
        subject_manager.update_subject_score(student_id,subject_id, new_score)
        current_page = previous_page
        prompt.show("Student score successfully updated!", pygame.Color("white"), pygame.Color("green"))            

def edit_student_page():    
    global current_page, previous_page, button_back
    global edit_student_dropdown_student_class
    global edit_student_dropdown_student_name
    global edit_student_dropdown_student_subject
    global edit_student_input_box_new_score
    previous_page = 'manage_students'

    button_back.rect.x, button_back.rect.y = 200, 525

    button_submit_subject_score_edit = Button(WIDTH//2-235+input_box_width, 525, 100, 50, 'Submit', FONT, button_color, 
                                 button_hover_color, button_text_color, action=submit_subject_score_edit)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif current_page == "edit_student":
            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_button_click(event.pos)
            edit_student_dropdown_student_class.handle_event(event)
            edit_student_dropdown_student_name.handle_event(event)
            edit_student_dropdown_student_subject.handle_event(event)
            edit_student_input_box_new_score.handle_event(event)
            button_submit_subject_score_edit.handle_event(event)

    screen.fill(BG_COLOR)
    prompt.update()
    edit_student_dropdown_student_class.update()
    edit_student_dropdown_student_name.update()
    edit_student_dropdown_student_subject.update()
    edit_student_input_box_new_score.update()

    draw_text('Edit Student', FONT, (0, 0, 0), screen, (WIDTH - FONT.size('Edit Student')[0]) // 2, 75)
    prompt.draw(screen)
    button_back.draw(screen)
    button_submit_subject_score_edit.draw(screen)
    edit_student_dropdown_student_class.draw(screen)
    edit_student_dropdown_student_name.draw(screen)
    edit_student_dropdown_student_subject.draw(screen)
    edit_student_input_box_new_score.draw(screen)
    pygame.display.flip()
    return True

def submit_subject_student_delete():
    global current_page, previous_page
    student_name = edit_student_dropdown_student_name.current_text
    student_class = edit_student_dropdown_student_class.current_text

    available_class_names = class_manager.get_all_class_field(1)
    available_students = student_manager.get_students_by_class(student_class)
    available_student_names = []
    for _,name,_ in available_students:
        available_student_names.append(name)

    student_id = student_manager.get_student_id(student_name,student_class)

    if student_name=="" or student_class=="":
        prompt.show("All fields are required!")
    elif student_class not in available_class_names:
        prompt.show("This class does not exist!")
    elif student_name not in available_student_names:
        prompt.show("This student does not exist!")
    else:
        student_manager.delete_student(student_id)
        current_page = previous_page
        prompt.show("Student successfully deleted!", pygame.Color("white"), pygame.Color("green"))

def delete_student_page():
    global current_page, previous_page, button_back
    global edit_student_dropdown_student_class
    global edit_student_dropdown_student_name
    previous_page = 'manage_students'

    button_back.rect.x, button_back.rect.y = 200, 500

    button_submit_student_delete = Button(WIDTH//2-235+input_box_width, 500, 100, 50, 'Submit', FONT, button_color, 
                                 button_hover_color, button_text_color, action=submit_subject_student_delete)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif current_page == 'delete_student':
            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_button_click(event.pos)
            edit_student_dropdown_student_class.handle_event(event)
            edit_student_dropdown_student_name.handle_event(event)
            button_submit_student_delete.handle_event(event)

    screen.fill(BG_COLOR)
    prompt.update()
    edit_student_dropdown_student_class.update()
    edit_student_dropdown_student_name.update()

    draw_text('Delete Student', FONT, (0, 0, 0), screen, (WIDTH - FONT.size('Delete Student')[0]) // 2, 75)
    prompt.draw(screen)
    button_back.draw(screen)
    edit_student_dropdown_student_class.draw(screen)
    edit_student_dropdown_student_name.draw(screen)
    button_submit_student_delete.draw(screen)
    pygame.display.flip()
    return True

def submit_subject_student_reallocate():
    global current_page, previous_page
    student_name = edit_student_dropdown_student_name.current_text
    student_class = edit_student_dropdown_student_class.current_text
    new_class = reallocate_student_dropdown_new_student_class.current_text

    available_class_names = class_manager.get_all_class_field(1)
    available_students = student_manager.get_students_by_class(student_class)
    available_student_names = []
    for _,name,_ in available_students:
        available_student_names.append(name)

    student_id = student_manager.get_student_id(student_name,student_class)

    if student_name=="" or student_class=="":
        prompt.show("All fields are required!")
    elif student_class not in available_class_names:
        prompt.show("This old class does not exist!")
    elif student_name not in available_student_names:
        prompt.show("This student does not exist!")
    elif new_class not in available_class_names:
        prompt.show("This new class does not exist!")
    elif new_class == student_class:
        prompt.show("You can't reallocate to the same class!")
    else:
        new_class_id,_,_ = class_manager.get_class_record(new_class)
        student_manager.transfer_student(student_id,new_class_id)
        current_page = previous_page
        prompt.show("Student successfully reallocated!", pygame.Color("white"), pygame.Color("green"))

def reallocate_student_page():
    global current_page, previous_page, button_back
    global edit_student_dropdown_student_class
    global edit_student_dropdown_student_name
    global reallocate_student_dropdown_new_student_class

    previous_page = 'manage_students'

    button_back.rect.x, button_back.rect.y = 200, 525
    button_submit_student_reallocate = Button(WIDTH//2-235+input_box_width, 525, 100, 50, 'Submit', FONT, button_color, 
                                 button_hover_color, button_text_color, action=submit_subject_student_reallocate)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif current_page == 'reallocate_student':
            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_button_click(event.pos)
            edit_student_dropdown_student_class.handle_event(event)
            edit_student_dropdown_student_name.handle_event(event)
            reallocate_student_dropdown_new_student_class.handle_event(event)
            button_submit_student_reallocate.handle_event(event)

    screen.fill(BG_COLOR)
    prompt.update()
    edit_student_dropdown_student_class.update()
    edit_student_dropdown_student_name.update()
    reallocate_student_dropdown_new_student_class.update()

    draw_text('Reallocate Student', FONT, (0, 0, 0), screen, (WIDTH - FONT.size('Reallocate Student')[0]) // 2, 75)
    prompt.draw(screen)
    button_back.draw(screen)
    button_submit_student_reallocate.draw(screen)
    edit_student_dropdown_student_class.draw(screen)
    edit_student_dropdown_student_name.draw(screen)
    reallocate_student_dropdown_new_student_class.draw(screen)
    pygame.display.flip()
    return True

def manage_classes_page():
    global current_page, previous_page, button_back
    global button_create_class, button_view_classes
    global input_box_class_name, input_box_class_capacity
    global data, class_table
    previous_page = 'main'
    
    button_create_class = Button((WIDTH-button_width)//2, HEIGHT//2-100, button_width, button_height,
                                'Create Class', FONT, button_color, button_hover_color, button_text_color,
                                action=create_class_page)
    
    button_view_classes = Button((WIDTH-button_width)//2, HEIGHT//2, button_width, button_height,
                                'View Classes', FONT, button_color, button_hover_color, button_text_color,
                                action=view_classes_page)
    
    button_back.rect.x, button_back.rect.y = WIDTH//2-button_back.rect.width//2, HEIGHT//2+100

    input_box_class_name = InputBox(WIDTH//2-135, HEIGHT//2-100, input_box_width, input_box_height, 
                            FONT, input_box_text_color, input_box_color, input_box_hover_color, label_text='Name:')

    input_box_class_capacity = InputBox(WIDTH//2-135, HEIGHT//2, input_box_width, input_box_height, 
                            FONT, input_box_text_color, input_box_color, input_box_hover_color, label_text='Capacity:')
    
    data = [["Name", "Size", "Capacity"]]
    for id,class_name,class_capacity in class_manager.get_all_class_record():
        data.append([class_name, class_manager.find_num_students(class_name), class_capacity])

    class_table = ScrollableTable(50, 170, data, 300, FONT)
    class_table.set_position(WIDTH//2-class_table.table_width//2, 170)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif current_page == 'manage_classes':
            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_button_click(event.pos)

    prompt.update()
    screen.fill(BG_COLOR)

    prompt.draw(screen)
    button_back.draw(screen)
    button_create_class.draw(screen)
    button_view_classes.draw(screen)
    draw_text('Manage Classes', FONT, (0, 0, 0), screen, (WIDTH - FONT.size('Manage Classes')[0]) // 2, 75)
    
    pygame.display.flip()
    return True

def update_edit_student_dropdown_student_name(selected_option):
    global edit_student_dropdown_student_name
    global reallocate_student_dropdown_new_student_class

    available_students_in_class = student_manager.get_students_by_class(selected_option)
    names, class_names = [],[]
    for _,name,_ in available_students_in_class:
        names.append(name)

    class_names = class_manager.get_all_class_field(1)
    class_names.remove(selected_option)

    edit_student_dropdown_student_name.options = names
    edit_student_dropdown_student_name.filtered_options = edit_student_dropdown_student_name.options
    edit_student_dropdown_student_name.current_text = ''

    reallocate_student_dropdown_new_student_class.options = class_names
    reallocate_student_dropdown_new_student_class.filtered_options = reallocate_student_dropdown_new_student_class.options
    reallocate_student_dropdown_new_student_class.current_text = ''

def update_edit_student_dropdown_student_subject(selected_option):
    global edit_student_dropdown_student_class
    global edit_student_dropdown_student_subject
    class_name = edit_student_dropdown_student_class.current_text
    student_id = student_manager.get_student_id(selected_option,class_name)

    available_subjects_for_student = subject_manager.get_student_subjects(student_id)

    names = []
    for _,name,_,_ in available_subjects_for_student:
        names.append(name)

    edit_student_dropdown_student_subject.options = names
    edit_student_dropdown_student_subject.filtered_options = edit_student_dropdown_student_subject.options
    edit_student_dropdown_student_subject.current_text = ''

def manage_students_page():
    global current_page, previous_page, button_back
    global input_box_student_name, dropdown_student_class, selectable_list
    global button_register_student, button_edit_student, button_delete_student, button_reallocate_student

    global edit_student_dropdown_student_class
    global edit_student_dropdown_student_name
    global edit_student_dropdown_student_subject
    global edit_student_input_box_new_score

    global reallocate_student_dropdown_new_student_class

    previous_page = 'main'
    available_class_names = class_manager.get_all_class_field(1) # get class names

    button_back.rect.x, button_back.rect.y = WIDTH//2-button_back.rect.width//2, HEIGHT//2+100

    button_register_student = Button((WIDTH-button_width)//2, HEIGHT//2-100, button_width, button_height,
                                'Register Student', FONT, button_color, button_hover_color, button_text_color,
                                action=register_student_page)
    button_edit_student = Button((WIDTH-button_width)//2, HEIGHT//2-50, button_width, button_height,
                                'Edit Student', FONT, button_color, button_hover_color, button_text_color,
                                action=edit_student_page)
    button_delete_student = Button((WIDTH-button_width)//2, HEIGHT//2, button_width, button_height,
                                'Delete Student', FONT, button_color, button_hover_color, button_text_color,
                                action=delete_student_page)
    button_reallocate_student = Button((WIDTH-button_width)//2, HEIGHT//2+50, button_width, button_height,
                                'Reallocate Student', FONT, button_color, button_hover_color, button_text_color,
                                action=reallocate_student_page)
    
    input_box_student_name = InputBox(75, HEIGHT//2-130, input_box_width, input_box_height, 
                            FONT, input_box_text_color, input_box_color, input_box_hover_color, label_text='Name:')

    dropdown_student_class = Dropdown(75, HEIGHT//2-70, dropdown_width, dropdown_height, 
                            FONT, dropdown_text_color, dropdown_color, dropdown_hover_color, 
                            options=available_class_names, label_text="Class:")

    selectable_list = SelectableList(400, HEIGHT//2-130, 380, 300, pygame.font.SysFont(None, 22), subjects, 2)

    edit_student_dropdown_student_class = Dropdown(75, HEIGHT//2-130, dropdown_width, dropdown_height, 
                            FONT, dropdown_text_color, dropdown_color, dropdown_hover_color, 
                            options=available_class_names, label_text="Class:")
    
    edit_student_dropdown_student_class.on_select = update_edit_student_dropdown_student_name
    
    edit_student_dropdown_student_name = Dropdown(475, HEIGHT//2-130, dropdown_width, dropdown_height, 
                            FONT, dropdown_text_color, dropdown_color, dropdown_hover_color, 
                            options=[], label_text="Name:")
    edit_student_dropdown_student_name.on_select = update_edit_student_dropdown_student_subject

    edit_student_dropdown_student_subject = Dropdown(75, HEIGHT//2+50, dropdown_width, dropdown_height, 
                            FONT, dropdown_text_color, dropdown_color, dropdown_hover_color, 
                            options=[], label_text="Subject:")
    
    edit_student_input_box_new_score = InputBox(475, HEIGHT//2+50, input_box_width, input_box_height, 
                            FONT, input_box_text_color, input_box_color, input_box_hover_color, label_text='Score:')
    
    reallocate_student_dropdown_new_student_class = Dropdown(WIDTH//2-dropdown_width//2+20, HEIGHT//2+50, dropdown_width, dropdown_height, 
                            FONT, dropdown_text_color, dropdown_color, dropdown_hover_color, 
                            options=[], label_text="New Class:")
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_button_click(event.pos)

    screen.fill(BG_COLOR)
    prompt.update()

    draw_text('Manage Students', FONT, (0, 0, 0), screen, (WIDTH - FONT.size('Manage Students')[0]) // 2, 75)
    prompt.draw(screen)
    button_back.draw(screen)
    button_register_student.draw(screen)
    button_edit_student.draw(screen)
    button_delete_student.draw(screen)
    button_reallocate_student.draw(screen)
    pygame.display.flip()
    return True

def calculate_grade(score):
    if score < 60:
        return 'F'
    elif score < 70:
        return 'C'
    elif score < 80:
        return 'B'
    else:
        return 'A'
    
def submit_student_grades_view():
    student_name = edit_student_dropdown_student_name.current_text
    student_class = edit_student_dropdown_student_class.current_text

    available_class_names = class_manager.get_all_class_field(1)
    available_students = student_manager.get_students_by_class(student_class)
    available_student_names = []
    for _,name,_ in available_students:
        available_student_names.append(name)

    student_id = student_manager.get_student_id(student_name,student_class)

    if student_name=="" or student_class=="":
        prompt.show("All fields are required!")
    elif student_class not in available_class_names:
        prompt.show("This class does not exist!")
    elif student_name not in available_student_names:
        prompt.show("This student does not exist!")
    else:
        data = [["Subject", "Score", "Grade"]]
        subjects = subject_manager.get_student_subjects(student_id)
        for id,name,_,score in subjects:
            if score is not None and score!=-1:
                data.append([name,score,calculate_grade(score)])
            else:
                data.append([name,'None','None'])
        student_subjects_table.set_data(data)
        student_subjects_table.set_position(WIDTH//2-student_subjects_table.table_width//2, 230)
        prompt.show("Student data retrieved successfully!", pygame.Color("white"), pygame.Color("green"))

def student_grades_page():
    global current_page, previous_page, button_back
    global edit_student_dropdown_student_class
    global edit_student_dropdown_student_name
    global student_subjects_table
    previous_page = 'view_reports'
    
    button_back.rect.x, button_back.rect.y = 200, 525
    
    button_submit_student_grades_view = Button(WIDTH//2-235+input_box_width, 525, 100, 50, 'Submit', FONT, button_color, 
                                 button_hover_color, button_text_color, action=submit_student_grades_view)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif current_page == 'student_grades':
            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_button_click(event.pos)
            edit_student_dropdown_student_class.handle_event(event)
            edit_student_dropdown_student_name.handle_event(event)
            student_subjects_table.handle_event(event)
            button_submit_student_grades_view.handle_event(event)

    prompt.update()
    edit_student_dropdown_student_class.update()
    edit_student_dropdown_student_name.update()

    screen.fill(BG_COLOR)

    prompt.draw(screen)
    button_back.draw(screen)
    button_submit_student_grades_view.draw(screen)
    edit_student_dropdown_student_class.draw(screen)
    edit_student_dropdown_student_name.draw(screen)
    student_subjects_table.draw(screen)
    draw_text('View Student Grades', FONT, (0, 0, 0), screen, (WIDTH - FONT.size('View Student Grades')[0]) // 2, 75)

    pygame.display.flip()
    return True

def submit_average_class_grades_view():
    student_class = edit_student_dropdown_student_class.current_text
    class_id,_,_ = class_manager.get_class_record(student_class)
    available_class_names = class_manager.get_all_class_field(1)
    available_students = student_manager.get_students_by_class(student_class)
    available_student_names = []
    for _,name,_ in available_students:
        available_student_names.append(name)
        
    if student_class=="":
        prompt.show("Class field is required!")
    elif student_class not in available_class_names:
        prompt.show("This class does not exist!")
    else:
        data = [["Subject", "Average Score", "Grade"]]
    
        for name in subjects:
            avg_score = subject_manager.get_average_score(name,class_id)
            if avg_score is not None and avg_score!=-1:
                data.append([name,avg_score,calculate_grade(avg_score)])

        class_average_table.set_data(data)
        class_average_table.set_position(WIDTH//2-class_average_table.table_width//2, 230)
        prompt.show("Class data retrieved successfully!", pygame.Color("white"), pygame.Color("green"))

def average_subject_grades_page():
    global current_page, previous_page, button_back
    global edit_student_dropdown_student_class
    global class_average_table
    previous_page = 'view_reports'
    
    button_back.rect.x, button_back.rect.y = 200, 525
    button_submit_average_class_grades_view = Button(WIDTH//2-235+input_box_width, 525, 100, 50, 'Submit', FONT, button_color, 
                                 button_hover_color, button_text_color, action=submit_average_class_grades_view)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif current_page == 'average_subject_grades':
            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_button_click(event.pos)
            edit_student_dropdown_student_class.handle_event(event)
            button_submit_average_class_grades_view.handle_event(event)
            class_average_table.handle_event(event)

    prompt.update()
    edit_student_dropdown_student_class.update()
    screen.fill(BG_COLOR)

    prompt.draw(screen)
    button_back.draw(screen)
    button_submit_average_class_grades_view.draw(screen)
    edit_student_dropdown_student_class.draw(screen)
    class_average_table.draw(screen)
    draw_text('View Average Grades Per Class', FONT, (0, 0, 0), screen, (WIDTH - FONT.size('View Average Grades Per Class')[0]) // 2, 75)

    pygame.display.flip()
    return True

def view_reports_page():
    global current_page, previous_page, button_back
    global button_student_grades, button_average_subject_grades
    global edit_student_dropdown_student_class
    global edit_student_dropdown_student_name
    global student_subjects_table, class_average_table
    global reallocate_student_dropdown_new_student_class

    previous_page = 'main'
    button_back.rect.x, button_back.rect.y = WIDTH//2-button_back.width//2, 435
    available_class_names = class_manager.get_all_class_field(1)

    button_student_grades = Button((WIDTH-button_width)//2, HEIGHT//2-100, button_width, button_height,
                                'Student Grades', FONT, button_color, button_hover_color, button_text_color,
                                action=student_grades_page)
    
    button_average_subject_grades = Button((WIDTH-button_width)//2, HEIGHT//2, button_width, button_height,
                                'Average Subject Grades', FONT, button_color, button_hover_color, button_text_color,
                                action=average_subject_grades_page)
    
    edit_student_dropdown_student_class = Dropdown(75, HEIGHT//2-130, dropdown_width, dropdown_height, 
                            FONT, dropdown_text_color, dropdown_color, dropdown_hover_color, 
                            options=available_class_names, label_text="Class:")
    
    edit_student_dropdown_student_class.on_select = update_edit_student_dropdown_student_name
    
    edit_student_dropdown_student_name = Dropdown(475, HEIGHT//2-130, dropdown_width, dropdown_height, 
                            FONT, dropdown_text_color, dropdown_color, dropdown_hover_color, 
                            options=[], label_text="Name:")

    reallocate_student_dropdown_new_student_class = Dropdown(WIDTH//2-dropdown_width//2+20, HEIGHT//2+50, dropdown_width, dropdown_height, 
                            FONT, dropdown_text_color, dropdown_color, dropdown_hover_color, 
                            options=[], label_text="New Class:")
    student_subjects_table = ScrollableTable(50, 170, [], 270, FONT)
    student_subjects_table.set_position(WIDTH//2-student_subjects_table.table_width//2, 170)

    class_average_table = ScrollableTable(50, 170, [], 270, FONT)
    class_average_table.set_position(WIDTH//2-class_average_table.table_width//2, 170)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif current_page=="view_reports":
            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_button_click(event.pos)

    screen.fill(BG_COLOR)
    prompt.update()

    draw_text('View Reports', FONT, (0, 0, 0), screen, (WIDTH - FONT.size('View Reports')[0]) // 2, 75)
    prompt.draw(screen)
    button_back.draw(screen)    
    button_student_grades.draw(screen)
    button_average_subject_grades.draw(screen)
    pygame.display.flip()
    return True

def handle_button_click(pos):
    global current_page, previous_page
    
    if current_page!='main' and button_back.collides(pos):
        current_page = previous_page
    elif current_page == 'main':
        if button_manage_classes.collides(pos):
            current_page = 'manage_classes'
        elif button_manage_students.collides(pos):
            current_page = 'manage_students'
        elif button_view_reports.collides(pos):
            current_page = 'view_reports'
    elif current_page == 'manage_classes':
        if button_create_class.collides(pos):
            current_page = 'create_class'
        elif button_view_classes.collides(pos):
            current_page = 'view_classes'
    elif current_page == 'manage_students':
        if button_register_student.collides(pos):
            current_page = 'register_student'
        elif button_edit_student.collides(pos):
            current_page = 'edit_student'
        elif button_delete_student.collides(pos):
            current_page = 'delete_student'
        elif button_reallocate_student.collides(pos):
            current_page = 'reallocate_student'
    elif current_page == 'view_reports':
        if button_student_grades.collides(pos):
            current_page = 'student_grades'
        elif button_average_subject_grades.collides(pos):
            current_page = 'average_subject_grades'
    
def main_page():
    global button_manage_classes, button_manage_students, button_view_reports
    global current_page, previous_page
    
    current_page, previous_page = 'main', 'main'

    button_manage_classes = Button((WIDTH-button_width)//2, HEIGHT//2-110, button_width, button_height,
                             'Manage Classes', FONT, button_color, button_hover_color, button_text_color,
                             action=manage_classes_page)
    
    button_manage_students = Button((WIDTH-button_width)//2, HEIGHT//2-10, button_width, button_height,
                             'Manage Students', FONT, button_color, button_hover_color, button_text_color,
                             action=manage_students_page)
    
    button_view_reports = Button((WIDTH-button_width)//2, HEIGHT//2+90, button_width, button_height,
                             'View Reports', FONT, button_color, button_hover_color, button_text_color,
                             action=view_reports_page)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif current_page == 'main':
            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_button_click(event.pos)

    prompt.update()
    screen.fill(BG_COLOR)
    button_manage_classes.draw(screen)
    button_manage_students.draw(screen)
    button_view_reports.draw(screen)
    prompt.draw(screen)

    draw_text('School Management System', FONT, (0,0,0), screen, (WIDTH-FONT.size('School Management System')[0])//2, 75)
    pygame.display.flip()
    return True

running = True
while running:
    if current_page == 'main':
        running = main_page()
    elif current_page == 'manage_classes':
        running = manage_classes_page()
    elif current_page == 'manage_students':
        running = manage_students_page()
    elif current_page == 'view_reports':
        running = view_reports_page()
    elif current_page == 'create_class':
        running = create_class_page()
    elif current_page == 'view_classes':
        running = view_classes_page()
    elif current_page == 'register_student':
        running = register_student_page()
    elif current_page == 'edit_student':
        running = edit_student_page()
    elif current_page == 'delete_student':
        running = delete_student_page()
    elif current_page == 'reallocate_student':
        running = reallocate_student_page()
    elif current_page == 'student_grades':
        running = student_grades_page()
    elif current_page == 'average_subject_grades':
        running = average_subject_grades_page()

pygame.quit()