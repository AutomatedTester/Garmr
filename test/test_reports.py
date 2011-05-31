import os
from garmr import Reporter

class TestReports:

    def setup_method(self, method):
        if os.path.exists("garmr-results.xml"):
            os.remove("garmr-results.xml")

    def test_report_throws_exception_with_no_data(self):
        reporter = Reporter()
        try:
            reporter.write_file()
            raise AssertionError("Exception should have been thrown")
        except AssertionError as e:
            raise
        except Exception:
            pass

    def test_reporter_formats_test_cases_with_no_errors_or_failures(self):
        tests_list = []
        tests_list.append({"name":"good test",
                           "time_taken": 1,
            })
        reporter = Reporter(tests_list)
        result = reporter._format_results()
        assert result["testcase"] == """<testcase classname="" name="%s" time="%s">""" % \
                        (tests_list[0]["name"], tests_list[0]["time_taken"])
        assert result["time_taken"] == 1
        assert result["errors"] == 0
        assert result["failed"] == 0
        assert result["skips"] == 0 

    def test_reporter_formats_2_test_cases_with_no_errors_or_failures(self):
        tests_list = []
        tests_list.append({"name":"good test",
                           "time_taken": 1,
            })
        tests_list.append({"name":"good test 2",
                           "time_taken": 1,
            })
        reporter = Reporter(tests_list)
        result = reporter._format_results()
        expected = """<testcase classname="" name="%s" time="%s">""" % \
                        (tests_list[0]["name"], tests_list[0]["time_taken"])
        expected += """<testcase classname="" name="%s" time="%s">""" % \
                        (tests_list[1]["name"], tests_list[1]["time_taken"]) 
        assert result["testcase"] == expected, result["testcase"]
        assert result["time_taken"] == 2
        assert result["errors"] == 0
        assert result["failed"] == 0
        assert result["skips"] == 0 

    def test_reporter_formats_2_test_cases_with_mix_of_errors_or_failures(self):
        tests_list = []
        tests_list.append({"name":"error test",
                           "time_taken": 1,
                           "errors" : True
            })
        tests_list.append({"name":"failure test",
                           "time_taken": 1,
                           "failed" : True
            })
        reporter = Reporter(tests_list)
        result = reporter._format_results()
        expected = """<testcase classname="" name="%s" time="%s">""" % \
                        (tests_list[0]["name"], tests_list[0]["time_taken"])
        expected += """<testcase classname="" name="%s" time="%s">""" % \
                        (tests_list[1]["name"], tests_list[1]["time_taken"]) 
        assert result["testcase"] == expected, result["testcase"]
        assert result["time_taken"] == 2
        assert result["errors"] == 1
        assert result["failed"] == 1
        assert result["skips"] == 0
     
    def test_reporter_formats_test_case_with_one_failure(self):
        tests_list = []
        tests_list.append({"name":"failedtest",
                           "time_taken": 1,
                           "failed": True,
            })
        reporter = Reporter(tests_list)
        result = reporter._format_results()
        assert result["testcase"] == """<testcase classname="" name="%s" time="%s">""" % \
                        (tests_list[0]["name"], tests_list[0]["time_taken"])
        assert result["time_taken"] == 1
        assert result["errors"] == 0
        assert result["failed"] == 1 
        assert result["skips"] == 0 
    
    def test_reporter_formats_test_case_with_error(self):
        tests_list = []
        tests_list.append({"name":"errorstest",
                           "time_taken": 1,
                           "errors": True,
            })
        reporter = Reporter(tests_list)
        result = reporter._format_results()
        assert result["testcase"] == """<testcase classname="" name="%s" time="%s">""" % \
                        (tests_list[0]["name"], tests_list[0]["time_taken"])
        assert result["time_taken"] == 1
        assert result["errors"] == 1
        assert result["failed"] == 0 
        assert result["skips"] == 0 

    def test_reporter_formats_test_case_with_skip(self):
        tests_list = []
        tests_list.append({"name":"skipstest",
                           "time_taken": 1,
                           "skips": True,
            })
        reporter = Reporter(tests_list)
        result = reporter._format_results()
        assert result["testcase"] == """<testcase classname="" name="%s" time="%s">""" % \
                        (tests_list[0]["name"], tests_list[0]["time_taken"])
        assert result["time_taken"] == 1
        assert result["errors"] == 0
        assert result["failed"] == 0 
        assert result["skips"] == 1 
