import unittest
import os
from app import app, db, forms, views
from collections import namedtuple

class FormTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False

        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_remove_company_btn(self):
        with app.app_context():
            form = forms.FinanceForm()
            form.add_company()
            form.add_company()
            form.remove_company()
            self.assertEqual(len(form.company_lst), 1)

    def test_remove_company_btn_empty_list(self):
        with app.app_context():
            form = forms.FinanceForm()
            form.remove_company()
            self.assertEqual(len(form.company_lst), 0)

    def test_add_company_btn(self):
        with app.app_context():
            form = forms.FinanceForm()
            form.add_company()
            form.add_company()
            self.assertEqual(len(form.company_lst), 2)

    def test_clear_btn(self):
        with app.app_context():
            form = forms.FinanceForm()
            form.add_company()
            form.add_company()
            form.data_clear()
            self.assertEqual(len(form.company_lst), 0)

    def test_paint_btn(self):
        with app.app_context():
            form = forms.FinanceForm()
            form.add_company()
            url = views.generate_plot(form)
            self.assertIsNotNone(url)


if __name__ == "__main__":
    unittest.main()

