from universities.models import University

class CreateUniversityTestUtil:

    university_dict = {
        'name': 'Universidade de São Paulo',
        'cnpj': '63025530000104'
    }

    def create_university():
        university = University.objects.create(
            name = CreateUniversityTestUtil.university_dict['name'],
            cnpj = CreateUniversityTestUtil.university_dict['cnpj'],
        )

        return university