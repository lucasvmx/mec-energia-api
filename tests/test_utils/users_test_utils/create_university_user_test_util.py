from users.models import UniversityUser

class CreateUniversityUserTestUtil:
    login_university_user_dict = {
        'email': 'admin@admin.com',
        'password': 'password'
    }
    
    def create_university_user(university):
        university_user = UniversityUser.objects.create_user(
            email = CreateUniversityUserTestUtil.login_university_user_dict['email'],
            password = CreateUniversityUserTestUtil.login_university_user_dict['password'],
            university = university)

        return university_user