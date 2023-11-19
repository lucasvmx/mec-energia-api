import pytest
from utils.cnpj_validator_util import CnpjValidator

valid_cnpjs_as_params = pytest.mark.parametrize('cnpj', [
    ('58577114000189'),
    ('11222333000181'),
    ('00038174000143'),  # UnB
])

invalid_cnpjs_as_params = pytest.mark.parametrize('cnpj', [
    ('11111111111111'),
])

invalid_null_cnpjs_as_params = pytest.mark.parametrize('cnpj', [
    ('00000000000000'),
])

wrong_length_or_non_numeric_cnpjs_as_params = pytest.mark.parametrize('cnpj', [
    # wrong length
    (''),
    ('1234567890123'),
    ('123456789012345'),
    # non numeric
    ('0003817400014_'),
    ('F0038174000143'),
    ('00!38174000143'),
])

sut = CnpjValidator.validate

@valid_cnpjs_as_params
def test_accepts_valid_cnpj(cnpj: str):
    sut(cnpj)

@wrong_length_or_non_numeric_cnpjs_as_params
def test_rejects_cnpj_with_non_numeric_digits(cnpj: str):
    with pytest.raises(Exception) as e:
        sut(cnpj)
    assert 'must contain exactly 14 numerical digits' in str(e.value)

@invalid_cnpjs_as_params
def test_rejects_invalid_cnpjs(cnpj: str):
    with pytest.raises(Exception) as e:
        sut(cnpj)
    assert 'Invalid' in str(e.value)

@invalid_null_cnpjs_as_params
def test_rejects_invalid_cnpjs(cnpj: str):
    with pytest.raises(Exception) as e:
        sut(cnpj)
    assert 'Invalid' in str(e.value)