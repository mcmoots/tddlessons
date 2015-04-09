from unittest import skip

from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.html import escape

from lists.views import home_page
from lists.models import Item, List
from lists.forms import (
    ExistingListItemForm, ItemForm, 
    DUPLICATE_ITEM_ERROR, EMPTY_ITEM_ERROR,
)

class HomePageTest(TestCase):

    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)



class ListViewTest(TestCase):

    def post_invalid_input(self):
        the_list = List.objects.create()
        return self.client.post(
            '/lists/%d/' % (the_list.id,),
            data={'text': ''}
        )

    def test_view_uses_list_template(self):
        test_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (test_list.id,))
        self.assertTemplateUsed(response, 'list.html')


    def test_passes_correct_list_to_template(self):
        wrong_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        self.assertEqual(response.context['list'], correct_list)


    def test_displays_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='Thing 1', list=correct_list)
        Item.objects.create(text='Thing 2', list=correct_list)
        wrong_list = List.objects.create()
        Item.objects.create(text='wrong wrong wrong', list=wrong_list)
        Item.objects.create(text='wronggity wrong', list=wrong_list)

        response = self.client.get('/lists/%d/' % (correct_list.id,))

        self.assertContains(response, 'Thing 1')
        self.assertContains(response, 'Thing 2')
        self.assertNotContains(response, 'wrong wrong wrong')
        self.assertNotContains(response, 'wronggity wrong')


    def test_can_save_a_POST_request_to_an_existing_list(self):
        wrong_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            '/lists/%d/' % (correct_list.id,),
            data={'text': 'Same list, different item'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'Same list, different item')
        self.assertEqual(new_item.list, correct_list)


    def test_POST_redirects_to_list_view(self):
        wrong_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            '/lists/%d/' % (correct_list.id,),
            data={'text': 'Same list, different item'}
        )

        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))


    def test_invalid_input_not_saved(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)


    def test_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')


    def test_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ExistingListItemForm)


    def test_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))


    def test_displays_item_form(self):
        the_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (the_list.id,))
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')


    def test_duplicate_item_validation_errors_appear_on_lists_page(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='foo')
        response = self.client.post(
            '/lists/%d/' % (list1.id,),
            data={'text': 'foo'}
        )

        expected_error = escape(DUPLICATE_ITEM_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(Item.objects.all().count(), 1)




class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        self.client.post(
            '/lists/new',
            data={'text': 'A new list item'}
        )

        # new item appears in database
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')


    def test_redirects_after_POST(self):
        response = self.client.post(
            '/lists/new',
            data={'text': 'A new list item'}
        )
        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % (new_list.id,))


    def test_invalid_input_renders_home_page_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    
    def test_validation_errors_shown_on_home_page(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    
    def test_invalid_input_passes_form_to_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)
        

    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)


