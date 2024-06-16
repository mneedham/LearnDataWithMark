import pytest
import os
import re
import json


def check_function_call(output, expected_result):
  function_call_present = "[TOOL_CALLS]" in output
  output_rows = output.split("\n")
  extra_output_present = len(output_rows) > 1

  pattern = r'\[TOOL_CALLS\] (\[.*?\])'
  match = re.search(pattern, output_rows[0])
  if match:
    function_call_json = match.group(1)
  else:
    function_call_json = None

  if function_call_json:
    try:
      function_call_data = json.loads(function_call_json)
      signature_valid = True
      signature_exact_match = function_call_data == expected_result
    except json.decoder.JSONDecodeError:
      signature_valid = False
      signature_exact_match = False
  else:
    signature_valid = False
    signature_exact_match = False

  return {
    "function_call_present": function_call_present,
    "signature_exact_match": signature_exact_match,
    "signature_valid": signature_valid,
    "extra_output_present": extra_output_present
  }


def get_test_name():
  pattern = r"(.*)\[\d+\]"
  current_test = os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]
  matches = re.search(pattern, current_test)
  return matches.group(1)


def collect_results(results_summary, result, output):
  if result['function_call_present']:
    results_summary['function_call_present'] += 1
  if result['signature_valid']:
    results_summary['signature_valid'] += 1
  if result['signature_exact_match']:
    results_summary['signature_exact_match'] += 1
  if result['extra_output_present']:
    results_summary['extra_output_present'] += 1
  results_summary['total_runs'] += 1
  results_summary["output"].append(output)


def get_result_template():
  return {
    "total_runs": 0,
    "signature_exact_match": 0,
    "function_call_present": 0,
    "signature_valid": 0,
    "extra_output_present": 0,
    "output": []
  }
