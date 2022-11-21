from universities.models import ConsumerUnit

class CreateConsumerUnitTestUtil:
    consumer_unit_dicts = [
        {
            'name': 'Darcy Ribeiro',
            'code': '000000000',
            'is_active': True,
        },
        {
            'name': 'Faculdade do Gama',
            'code': '111111111',
            'is_active': True,
        }
    ]
    
    def create_consumer_unit(index, university):
        consumer_unit_dict = CreateConsumerUnitTestUtil.consumer_unit_dicts[index]
        
        consumer_unit = ConsumerUnit.objects.create(
            name = consumer_unit_dict['name'],
            code = consumer_unit_dict['code'],
            is_active = consumer_unit_dict['is_active'],
            university = university
        )

        return (consumer_unit_dict, consumer_unit)
