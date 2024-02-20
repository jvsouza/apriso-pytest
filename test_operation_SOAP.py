
import main
import json
from zeep import helpers

ut = main.UnitTest("config.ini")

def test_operation():
    # need know name operation
    # need know input external required by operation
    # invoke webservice, that invoke opeeration test
    r = ut.post_webservice(
            _operation = "TEST_PY",
            _inputs = { "EmployeeNo": "jonas" }
        )

    r_dict = helpers.serialize_object(r)
    assert r_dict['IsSuccess'] == True
    EncodedParameters = json.loads(r_dict['Output_EncodedParameters'])
    assert EncodedParameters["OperationIsError"] == False


# to run from this file, uncomment this call function
# to run from pytest, this call function must be commented 
# test_operation()
