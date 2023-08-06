import logging
import pytest
logger = logging.getLogger(__name__)

from alexber.scrapyitem import GeneralItem

def test_dynamic_field_creation(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')

    exp_id=42
    exp_name='John'

    item= GeneralItem()
    item['id']= exp_id
    item['name'] = exp_name

    pytest.assume(exp_id==item['id'])
    pytest.assume(exp_name == item['name'])


def test_dynamic_field_creation_from_dict(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')

    exp_id=42
    exp_name='John'

    item= GeneralItem({'id':exp_id, 'name':exp_name})


    pytest.assume(exp_id==item['id'])
    pytest.assume(exp_name == item['name'])


class YourItem(GeneralItem):
    pass


def test_dynamic_field_creation(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')

    exp_id=42
    exp_name='John'

    item= YourItem()
    item['id']= exp_id
    item['name'] = exp_name

    pytest.assume(exp_id==item['id'])
    pytest.assume(exp_name == item['name'])


def test_dynamic_field_creation_from_dict(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')

    exp_id=42
    exp_name='John'

    item= YourItem({'id':exp_id, 'name':exp_name})


    pytest.assume(exp_id==item['id'])
    pytest.assume(exp_name == item['name'])

if __name__ == "__main__":
    pytest.main([__file__])

