from tariffs.models import Distributor

class CreateDistributorTestUtil:
    distributor_dict = {
        'name': 'Distribuidora de Energia',
        'cnpj': '63025530000104'
    }
    
    def create_distributor(university):
        distributor = Distributor.objects.create(
            name = CreateDistributorTestUtil.distributor_dict['name'],
            cnpj = CreateDistributorTestUtil.distributor_dict['cnpj'],
            university = university
        )

        return distributor