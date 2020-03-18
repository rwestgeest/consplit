from hamcrest import assert_that, equal_to
from consplit.files import location_of

def test_location_of_path_is_basename():
  assert_that(location_of('data/bla.svg'), equal_to('data'))
  assert_that(location_of('the/data/bla.svg'), equal_to('the/data'))
  