
import main
import json
# from zeep import helpers

ut = main.UnitTest("config.ini")

def test_operation():
    # need know name operation
    # need know input external required by operation
    # invoke webservice, that invoke opeeration test
    r = ut.post_webservice(
            _operation = "TEST_PY",
            _inputs = { "EmployeeNo": "jonas" }
        )

    # check http status code return
    assert r.status_code == 200
    # check if success execute operation
    Outputs = r.json()["Outputs"]
    assert Outputs["__Routing__"] == True
    # need know outputs extenal if exist, by other verfication
    EncodedParameters = json.loads(Outputs['EncodedParameters'])
    assert EncodedParameters["OperationIsError"] == False


# to run from this file, uncomment this call function
# to run from pytest, this call function must be commented 
# test_operation()
