import time
import requests
import validators

def check_url_exists_requests(url):
  """Checks if the given URL exists using the requests library.

  Args:
    url: The URL to check.

  Returns:
    True if the URL exists, False otherwise.
  """

  start_time = time.time()
  response = requests.head(url)
  end_time = time.time()
  return response.status_code == 200 and (end_time - start_time) < 1

def check_url_exists_validators(url):
  """Checks if the given URL exists using the validators library.

  Args:
    url: The URL to check.

  Returns:
    True if the URL exists, False otherwise.
  """

  start_time = time.time()
  valid = validators.url(url)
  end_time = time.time()
  return valid and (end_time - start_time) < 1

# Example usage:

url = "https://www.gocomics.com/peanuts/2023/09/15"

num_iterations = 200

requests_time = 0
validators_time = 0

for i in range(num_iterations):
  requests_time += check_url_exists_requests(url)
  validators_time += check_url_exists_validators(url)

requests_time /= num_iterations
validators_time /= num_iterations

print("requests_time:", requests_time)
print("validators_time:", validators_time)
