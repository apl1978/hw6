class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecturer(self, lecturer, course, grade):
        if isinstance(lecturer,
                      Lecturer) and course in lecturer.courses_attached and course in self.courses_in_progress:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def _get_average_grade(self):
        summ = 0
        if len(self.grades) == 0:
            return 0
        for v in self.grades.values():
            summ += sum(v) / len(v)
        return (round(summ / len(self.grades), 2))

    def __str__(self):
        average_grade = self._get_average_grade()
        fin = ','.join(self.finished_courses)
        prg = ','.join(self.courses_in_progress)
        res = f'Имя {self.name}\nФамилия {self.surname}\nСредняя оценка за домашние задания: {average_grade}\nКурсы в процессе изучения: {prg}\nЗавершенные курсы: {fin}'
        return res

    def __lt__(self, other):
        if not isinstance(other, Student):
            print('Not a Student')
            return
        return self._get_average_grade() < other._get_average_grade()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def __str__(self):
        average_grade = Student._get_average_grade(self)
        res = f'Имя {self.name}\nФамилия {self.surname}\nСредняя оценка за лекции: {average_grade}'
        return res

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            print('Not a Lecturer')
            return
        return Student._get_average_grade(self) < Student._get_average_grade(other)


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        res = f'Имя {self.name}\nФамилия {self.surname}'
        return res


def get_avg_ex_std(students, course):
    summ = 0
    cnt = 0
    for student in students:
        for k, v in student.grades.items():
            if k == course:
                summ += sum(v) / len(v)
                cnt += 1
    if cnt == 0:
        return 0
    else:
        return round(summ / cnt, 2)


def get_avg_ex_lect(lecturers, course):
    return get_avg_ex_std(lecturers, course)


def main():
    student1 = Student('Ст1_Имя', 'Ст1_Фамилия', 'your_gender')
    student1.courses_in_progress += ['Python', 'English']
    student1.finished_courses += ['GIT']

    reviewer1 = Reviewer('Р1_Имя', 'Р1_Фамилия')
    reviewer1.courses_attached += ['Python', 'GIT']

    reviewer1.rate_hw(student1, 'Python', 10)
    reviewer1.rate_hw(student1, 'Python', 9)
    reviewer1.rate_hw(student1, 'Python', 10)

    reviewer1.rate_hw(student1, 'GIT', 8)
    reviewer1.rate_hw(student1, 'GIT', 9)

    reviewer2 = Reviewer('Р2_Имя', 'Р2_Фамилия')
    reviewer2.courses_attached += ['English']

    reviewer2.rate_hw(student1, 'English', 8)
    reviewer2.rate_hw(student1, 'English', 9)
    reviewer2.rate_hw(student1, 'English', 10)

    lecturer1 = Lecturer('Л1_Имя', 'Л1_Фамилия')
    lecturer1.courses_attached += ['Python']
    student1.rate_lecturer(lecturer1, 'Python', 10)
    student1.rate_lecturer(lecturer1, 'Python', 8)
    student1.rate_lecturer(lecturer1, 'Python', 9)

    lecturer2 = Lecturer('Л2_Имя', 'Л2_фамилия')
    lecturer2.courses_attached += ['Python', 'GIT']
    student1.rate_lecturer(lecturer2, 'Python', 7)
    student1.rate_lecturer(lecturer2, 'Python', 6)
    student1.rate_lecturer(lecturer2, 'Python', 8)

    student2 = Student('Ст2_Имя', 'Ст2_Фамилия', 'your_gender')
    student2.courses_in_progress += ['Python', 'GIT']
    student2.finished_courses += ['English']

    reviewer1.rate_hw(student2, 'GIT', 5)
    reviewer1.rate_hw(student2, 'GIT', 4)
    reviewer1.rate_hw(student2, 'GIT', 6)

    reviewer1.rate_hw(student2, 'Python', 5)
    reviewer1.rate_hw(student2, 'Python', 4)
    reviewer1.rate_hw(student2, 'Python', 6)

    student2.rate_lecturer(lecturer1, 'Python', 7)
    student2.rate_lecturer(lecturer1, 'Python', 6)
    student2.rate_lecturer(lecturer1, 'Python', 7)

    student2.rate_lecturer(lecturer2, 'GIT', 8)
    student2.rate_lecturer(lecturer2, 'GIT', 9)
    student2.rate_lecturer(lecturer2, 'GIT', 10)

    print("reviewer1")
    print(reviewer1)
    print("reviewer2")
    print(reviewer2)

    print("lecturer1")
    print(lecturer1)
    print("lecturer2")
    print(lecturer2)
    print("lecturer1 > lecturer2")
    print(lecturer1 > lecturer2)

    print("student1")
    print(student1)
    print("student2")
    print(student2)
    print("student1 > student2")
    print(student1 > student2)

    students_list = [student1, student2]
    lecturers_list = [lecturer1, lecturer2]
    course = 'Python'
    avg_ex_std = get_avg_ex_std(students_list, course)
    print(f'Cредняя оценка за домашние задания по всем студентам в рамках курса {course}: {avg_ex_std}')
    avg_ex_lect = get_avg_ex_lect(lecturers_list, course)
    print(f'Средняя оценка за лекции всех лекторов в рамках курса {course}: {avg_ex_lect}')


main()
