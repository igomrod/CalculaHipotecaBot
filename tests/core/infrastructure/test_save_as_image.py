import os.path

from core.infrastructure.save_as_image import save_as_image
from tests.core.domain.loan_builder import LoanMother


def test_should_store_table_as_image():
    image_path = '/tmp/mortgage_image_test.png'

    loan = LoanMother().build()

    save_as_image(mortgage_table=loan.table, max_periods=12, image_path=image_path)

    assert os.path.exists(image_path), "image file exists"

    # clean up
    os.remove(image_path)
